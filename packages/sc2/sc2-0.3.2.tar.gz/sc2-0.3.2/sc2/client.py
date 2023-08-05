from s2clientprotocol import (
    sc2api_pb2 as sc_pb,
    common_pb2 as common_pb,
    query_pb2 as query_pb,
    debug_pb2 as debug_pb
)

from .cache import method_cache_forever

from .protocol import Protocol
from .game_info import GameInfo
from .game_data import GameData, AbilityData
from .data import Race, ActionResult, ChatChannel
from .action import combine_actions
from .position import Point2
from .unit import Unit

class Client(Protocol):
    def __init__(self, ws):
        super().__init__(ws)

    async def join_game(self, race=None, observed_player_id=None, portconfig=None):
        ifopts = sc_pb.InterfaceOptions(raw=True)

        if race is None:
            assert isinstance(observed_player_id, int)
            # join as observer
            req = sc_pb.RequestJoinGame(
                observed_player_id=observed_player_id,
                options=ifopts
            )
        else:
            assert isinstance(race, Race)
            req = sc_pb.RequestJoinGame(
                race=race.value,
                options=ifopts
            )

        if portconfig:
            req.shared_port = portconfig.shared
            req.server_ports.game_port = portconfig.server[0]
            req.server_ports.base_port = portconfig.server[1]

            for ppc in portconfig.players:
                p = req.client_ports.add()
                p.game_port = ppc[0]
                p.base_port = ppc[1]

        result = await self._execute(join_game=req)
        return result.join_game.player_id

    async def save_replay(self, path):
        result = await self._execute(save_replay=sc_pb.RequestSaveReplay())
        with open(path, "wb") as f:
            f.write(result.save_replay.data)

    async def observation(self):
        result = await self._execute(observation=sc_pb.RequestObservation())
        return result

    async def step(self):
        result = await self._execute(step=sc_pb.RequestStep(count=8))
        return result

    async def get_game_data(self):
        result = await self._execute(data=sc_pb.RequestData(
            ability_id=True,
            unit_type_id=True,
            upgrade_id=True
        ))
        return GameData(result.data)

    async def get_game_info(self):
        result = await self._execute(game_info=sc_pb.RequestGameInfo())
        return GameInfo(result.game_info)

    async def actions(self, actions, game_data, return_successes=False):
        if not isinstance(actions, list):
            res = await self.actions([actions], game_data, return_successes)
            if res:
                return res[0]
            else:
                return None
        else:
            actions = combine_actions(actions, game_data)

            res = await self._execute(action=sc_pb.RequestAction(
                actions=[sc_pb.Action(action_raw=a) for a in actions]
            ))

            res = [ActionResult(r) for r in res.action.result]
            if return_successes:
                return res
            else:
                return [r for r in res if r != ActionResult.Success]

    async def query_pathing(self, start, end):
        assert isinstance(start, (Point2, Unit))
        assert isinstance(end, Point2)
        if isinstance(start, Point2):
            result = await self._execute(query=query_pb.RequestQuery(
                pathing=[query_pb.RequestQueryPathing(
                    start_pos=common_pb.Point2D(x=start.x, y=start.y),
                    end_pos=common_pb.Point2D(x=end.x, y=end.y)
                )]
            ))
        else:
            result = await self._execute(query=query_pb.RequestQuery(
                pathing=[query_pb.RequestQueryPathing(
                    unit_tag=start.tag,
                    end_pos=common_pb.Point2D(x=end.x, y=end.y)
                )]
            ))
        distance = float(result.query.pathing[0].distance)
        if distance <= 0.0:
            return None
        return distance

    async def query_building_placement(self, ability, positions, ignore_resources=True):
        assert isinstance(ability, AbilityData)
        result = await self._execute(query=query_pb.RequestQuery(
            placements=[query_pb.RequestQueryBuildingPlacement(
                ability_id=ability.id.value,
                target_pos=common_pb.Point2D(x=position.x, y=position.y)
            ) for position in positions],
            ignore_resource_requirements=ignore_resources
        ))
        return [ActionResult(p.result) for p in result.query.placements]

    async def chat_send(self, message, team_only):
        ch = ChatChannel.Team if team_only else ChatChannel.Broadcast
        r = await self._execute(action=sc_pb.RequestAction(
            actions=[sc_pb.Action(action_chat=sc_pb.ActionChat(
                channel=ch.value,
                message=message
            ))]
        ))

    async def debug_text(self, texts, positions, color=(0, 255, 0)):
        if isinstance(positions, list):
            if not positions:
                return

            if isinstance(texts, str):
                texts = [texts] * len(positions)
            assert len(texts) == len(positions)

            await self._execute(debug=sc_pb.RequestDebug(
                debug=[debug_pb.DebugCommand(draw=debug_pb.DebugDraw(
                    text=[debug_pb.DebugText(
                        text=t,
                        color=debug_pb.Color(r=color[0], g=color[1], b=color[2]),
                        world_pos=common_pb.Point(x=p.x, y=p.y, z=p.z)
                    ) for t, p in zip(texts, positions)]
                ))]
            ))
        else:
            await self.debug_text([texts], [positions], color)
