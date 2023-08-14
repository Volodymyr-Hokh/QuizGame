import asyncio
from dataclasses import dataclass
import json
import signal

import http
import websockets

from lobby import Lobby
from player import Player
from quiz_brain import GameOver


@dataclass
class Context:
    websocket: object
    player: Player
    lobby: Lobby


class WebsocketHandler:
    connections = []

    async def handle(self, websocket, path):
        self.connections.append(websocket)
        asyncio.create_task(self.on_connect(websocket))

        try:
            while True:
                message = await websocket.recv()
                asyncio.create_task(self.proceed_message(websocket, message))
                
        except websockets.ConnectionClosed:
            self.connections.remove(websocket)
            asyncio.create_task(self.on_disconnect(websocket))
        except Exception as e:
            print(f"WebSocket error: {e}")

    async def proceed_message(self, ws, message):
        raise NotImplementedError
    
    async def on_disconnect(self, ws):
        raise NotImplementedError
    
    async def on_connect(self, ws):
        raise NotImplementedError
    


class SanicWebsocketHandler(WebsocketHandler):
    active_connections = []

    async def handle(self, request, websocket):
        self.active_connections.append(websocket)
        print(self.active_connections)
        asyncio.create_task(self.on_connect(websocket))

        try:
            while True:
                message = await websocket.recv()
                asyncio.create_task(self.proceed_message(websocket, message))

        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            asyncio.create_task(self.on_disconnect(websocket))
            self.active_connections.remove(websocket)
    

class EventHandler(SanicWebsocketHandler):
    players = {}
    lobbies = {}
    allowed_events = ["new_player",
                      "start_game",
                      "create_lobby",
                      "join_lobby",
                      "answer"]

    async def proceed_message(self, ws, message):
        print(f'Proceed message from ws: {ws}, message: {message}')
        try:
            event = json.loads(message)
            if event["event"] not in self.allowed_events:
                return
            func = getattr(self, event["event"])
            asyncio.create_task(func(self._get_context(ws), **event["payload"]))

        except Exception as exc:
            print(exc)

    async def on_disconnect(self, ws):
        if ws not in self.players:
            return
        player = self.players.pop(ws)
        lobby = player.lobby
        if lobby:
            lobby.players.remove(player)
            if len(lobby.players) == 0:
                self.lobbies.pop(lobby.id)
        await lobby.send_updates()


    async def on_connect(self, ws):
        pass

    async def new_player(self, context, nickname):
        context.new_player(nickname)
   

    def _get_context(self, websocket):
        player = self.players.get(websocket)
        lobby = player.lobby if player and player.lobby else None

        context = Context(websocket, player, lobby)
        context.new_player = lambda nickname: self._new_player(websocket, nickname)
        context.create_lobby = lambda: self._create_lobby(player)
        context.join_lobby = lambda id: self._join_lobby(id, player)
        return context
    
    def _new_player(self, websocket, nickname):
        self.players[websocket] = Player(nickname)
        self.players[websocket].websocket = websocket

    async def create_lobby(self, context):
        lobby = context.create_lobby()
        await lobby.send_updates()

    async def join_lobby(self, context, id):
        lobby = context.join_lobby(id)
        await lobby.send_updates()
        
    def _create_lobby(self, admin):
        lobby = Lobby(admin)
        admin.lobby = lobby
        self.lobbies[lobby.id] = lobby
        return lobby
    
    def _join_lobby(self, id, player):
        lobby = self.lobbies.get(id)
        if not lobby or lobby.game_started:
            return
        lobby.add_player(player)
        return lobby
    
    async def start_game(self, context, id):
        context.lobby.start()
        context.lobby.next_question(just_started=True)
        context.lobby.reset_scores()
        await context.lobby.send_updates()

    async def answer(self, context: Context, value):
        context.player.answer(value)
        # await context.lobby.send_updates()
        if context.lobby.all_players_answered():
            try:
                context.lobby.next_question()
                await context.lobby.send_updates()
            except GameOver:
                context.lobby.game_over()
                await context.lobby.send_updates(msg="Game over")


async def handle_request(path, headers):
    response = None
    with open(f"frontend/{path}", "rb") as file:
        response = file.read()
    print(path, headers)
    return http.HTTPStatus.OK, [], response + b"\n"

                

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    handler = EventHandler()

    async with websockets.serve(
        handler.handle,
        host="",
        port=8080,
        process_request=handle_request,
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())