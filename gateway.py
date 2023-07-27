#!/usr/bin/env python

import asyncio
import json

import websockets

from lobby import Lobby
from player import Player

"""
New player

{
    "event": "new_player",
    "payload": {
        "nickname": "Nagibator"
    }
} -> OK




Create lobby

{
    "event": "create_lobby",
    "payload": {}
} 
-> 
{
    "status: "ok",
    "payload":
    {
        "lobby": {
            "id": 123123123
            "players": [
                "Nagibator",
            ]
        }
    }
}

Join lobby

{
    "event": "join_lobby",
    "payload: {
        "id": 123123123
    }
}
->
{
    "status: "ok",
    "payload":
    {
        "lobby": {
            "id": 123123123
            "players": [
                "Nagibator",
                "Pogger"
            ]
        }
    }
}



"""

class WebsocketHandler:
    async def handle(self, websocket, path):
        try:
            while True:
                message = await websocket.recv()
                asyncio.create_task(self.proceed_message(websocket, message))
                
        except websockets.ConnectionClosed:
            print("WebSocket connection closed.")
        except Exception as e:
            print(f"WebSocket error: {e}")

    async def proceed_message(self, ws, message):
        raise NotImplementedError


class EventHandler(WebsocketHandler):
    players = {}
    lobbies = {}

    async def new_player(self, websocket, payload):
        player = Player(payload["nickname"])
        player.websocket = websocket
        self.players[websocket] = player

    async def update_users_lobbies(self, lobby):
        response = {
            "event": "lobby_update",
            "payload": {
                "id": lobby.id,
                "players": [player.nickname for player in lobby.players],
                "is_admin": False,
                "game_started": lobby.game_started,
                "question": lobby.quiz.current_question.text if lobby.game_started else "",
                "scoreboard": [(player.nickname, player.score) for player in lobby.players]
            }
        }

        for player in lobby.players:
            response["payload"]["is_admin"] = player == lobby.players[0]
            await player.websocket.send(json.dumps(response))

    async def start_game(self, websocket, payload):
        player = self.players[websocket]
        lobby = self.lobbies[payload["id"]]
        lobby.start()
        lobby.next_question(just_started=True)
        await self.update_users_lobbies(lobby)

    async def create_lobby(self, websocket, payload):
        print("New lobby")
        lobby = Lobby(self.players[websocket])
        self.lobbies[lobby.id] = lobby
        await self.update_users_lobbies(lobby)

    async def join_lobby(self, websocket, payload):
        player = self.players.get(websocket)
        if not player:
            return
        lobby = self.lobbies.get(payload["id"])
        lobby.add_player(player)

        await self.update_users_lobbies(lobby)

    async def answer(self, websocket, payload):
        player = self.players[websocket]
        player.answer(payload["value"])
        await self.update_users_lobbies(player.lobby)
        if player.lobby.all_players_answered():
            player.lobby.next_question()
            await self.update_users_lobbies(player.lobby)

    async def proceed_message(self, ws, message):
        print(f'Proceed message from ws: {ws}, message: {message}')
        try:
            event = json.loads(message)
            func = getattr(self, event["event"])
            asyncio.create_task(func(ws, event["payload"]))

        except Exception as exc:
            print(exc)


async def main():
    handler = EventHandler()
    server = await websockets.serve(handler.handle, "0.0.0.0", 8001)

    print("WebSocket server started.")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())