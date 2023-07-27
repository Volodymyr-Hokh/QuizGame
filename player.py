import uuid

from quiz_brain import Answer

class Player:

    def __init__(self, nickname, lobby=None):
        self.nickname = nickname
        self.answers = []
        self.score = 0
        self.id = str(uuid.uuid4())
        self.lobby = lobby
        self.websocket = None

    def add_answer(self, answer):
        self.answers.append(answer)
        if answer.is_correct:
            self.score += 1

    def answer(self, user_answer):
        self.lobby.amount_answers += 1
        question = self.lobby.quiz.current_question
        answer = Answer(question, user_answer)
        self.add_answer(answer)

    

        


