import uuid

from data import question_data
from player import Player
from quiz_brain import QuizBrain
from question_model import Question

class Lobby:
    def __init__(self, admin: Player):
        admin.lobby = self
        self.players = [admin]
        self.id = str(uuid.uuid4())
        self.game_started = False
        self.amount_answers = 0

        question_bank = []
        for question in question_data:
            question_text = question["question"]
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            question_bank.append(new_question)
        self.quiz = QuizBrain(question_bank)

    def add_player(self, player):
        player.lobby = self
        self.players.append(player)

    def all_players_answered(self):
        return self.amount_answers == len(self.players)
    
    def next_question(self, just_started=False):
        if self.all_players_answered() or just_started:
            self.amount_answers = 0
            return self.quiz.next_question()
        raise Exception("Not all players answered")

    def start(self):
        self.game_started = True

