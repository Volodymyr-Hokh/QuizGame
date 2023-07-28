import html

from data import question_data
from question_model import Question

class GameOver(Exception):
    pass


class QuizBrain:

    def __init__(self):
        self.question_number = 0
        self.question_list = []
        self.current_question = None

        for question in question_data:
            question_text = question["question"]
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            self.question_list.append(new_question)

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        try:
            self.current_question = self.question_list[self.question_number]
            self.question_number += 1
            question_text = html.unescape(self.current_question.text)
            return f"Q.{self.question_number}: {question_text} (True/False): "
        except IndexError:
            raise GameOver()

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            return True
        else:
            return False


class Answer:
    def __init__(self, question, user_answer):
        self.question = question
        self.user_answer = user_answer

    @property
    def is_correct(self):
        return self.question.answer == self.user_answer
