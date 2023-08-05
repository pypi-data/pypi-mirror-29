import sys
import signal
import time
import asyncio
import os.path
import shutil
import tempfile
import subprocess
import portpicker
import websockets

from .paths import Paths
from .protocol import Protocol
from .controller import Controller

class kill_switch(object):
    _to_kill = []

    @classmethod
    def add(cls, value):
        cls._to_kill.append(value)

    @classmethod
    def kill_all(cls):
        for p in cls._to_kill:
            p._clean()

class SC2Process(object):
    def __init__(self, fullscreen=False):
        self._fullscreen = fullscreen
        self._port = portpicker.pick_unused_port()
        self._tmp_dir = tempfile.mkdtemp(prefix="SC2_")
        self._process = None
        self._ws = None

    async def __aenter__(self):
        kill_switch.add(self)

        def signal_handler(signal, frame):
            kill_switch.kill_all()

        signal.signal(signal.SIGINT, signal_handler)

        try:
            self._process = self._launch()
            self._ws = await self._connect()
        except:
            self._clean()
            raise

        return Controller(self._ws)

    async def __aexit__(self, *args):
        kill_switch.kill_all()
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    @property
    def ws_url(self):
        return f"ws://127.0.0.1:{self._port}/sc2api"

    def _launch(self):
        return subprocess.Popen([
                Paths.EXECUTABLE,
                "-listen", "127.0.0.1",
                "-port", str(self._port),
                "-displayMode", "1" if self._fullscreen else "0",
                "-dataDir", Paths.BASE,
                "-tempDir", self._tmp_dir
            ],
            cwd=Paths.CWD,
            #, env=run_config.env
        )

    async def _connect(self):
        for _ in range(30):
            await asyncio.sleep(1)
            try:
                ws = await websockets.connect(self.ws_url, timeout=120)
                return ws
            except ConnectionRefusedError:
                pass

        raise TimeoutError("Websocket")

    def _clean(self):
        print("Cleanup")
        if self._ws is not None:
            self._ws.close()

        if self._process is not None:
            if self._process.poll() is None:
                for _ in range(3):
                    self._process.terminate()
                    time.sleep(2)
                    if self._process.poll() is not None:
                        break
                else:
                    self._process.kill()
                    self._process.wait()
                    print("KILLED")

        if os.path.exists(self._tmp_dir):
            shutil.rmtree(self._tmp_dir)

        self._process = None
        self._ws = None
        print("Cleanup complete")
