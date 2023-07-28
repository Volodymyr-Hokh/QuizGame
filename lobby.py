import json
import uuid


from player import Player
from quiz_brain import QuizBrain


class Lobby:
    def __init__(self, admin: Player):
        admin.lobby = self
        self.players = [admin]
        self.id = str(uuid.uuid4())
        self.game_started = False
        self.amount_answers = 0
        self.answered = []

        
        self.quiz = QuizBrain()

    def add_player(self, player):
        if player in self.players:
            return
        player.lobby = self
        self.players.append(player)

    def all_players_answered(self):
        return len(self.answered) == len(self.players)
    
    def next_question(self, just_started=False):
        if self.all_players_answered() or just_started:
            self.answered = []
            return self.quiz.next_question()
        raise Exception("Not all players answered")

    def start(self):
        self.game_started = True

    async def broadcast(self, data):
        for player in self.players:
            await player.websocket.send(data)

    async def send_updates(self, msg=""):
        response = {
            "event": "lobby_update",
            "payload": {
                "id": self.id,
                "players": [player.nickname for player in self.players],
                "is_admin": False,
                "game_started": self.game_started,
                "question": self.quiz.current_question.text if self.game_started else "",
                "scoreboard": [(player.nickname, player.score) for player in self.players],
                "msg": msg
            }
        }
        for player in self.players:
            response["payload"]["is_admin"] = self.players[0] == player
            await player.websocket.send(json.dumps(response))

    def game_over(self):
        self.game_started = False
        self.quiz = QuizBrain()

    def reset_scores(self):
        for player in self.players:
            player.score = 0

