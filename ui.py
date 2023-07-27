from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
FONT = ("Arial", 20, "italic")


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("QuizApp")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.canvas = Canvas(width=300, height=250)
        self.question_text = self.canvas.create_text(150, 125, text="Some question text", font=FONT, width=280)
        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)

        self.score_text = Label(text=f"Score: {0}", font=("Arial", 12, "italic"))
        self.score_text.config(bg=THEME_COLOR, fg="White")
        self.score_text.grid(column=1, row=0)

        true_img = PhotoImage(file="./images/true.png")
        self.true_button = Button(image=true_img, command=self.user_answer_true, highlightthickness=0)
        self.true_button.grid(column=0, row=3)

        false_img = PhotoImage(file="./images/false.png")
        self.false_button = Button(image=false_img, command=self.user_answer_false, highlightthickness=0)
        self.false_button.grid(column=1, row=3)

        self.get_next_question()

        self.window.mainloop()

    def user_answer_true(self):
        is_correct = self.quiz.check_answer("true")
        self.give_feedback(is_correct)

    def user_answer_false(self):
        is_correct = self.quiz.check_answer("false")
        self.give_feedback(is_correct)

    def get_next_question(self):
        self.canvas.configure(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You reached the end of the quiz")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def give_feedback(self, is_correct):
        if is_correct:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.score_text.config(text=f"Score: {self.quiz.score}")
        self.window.after(1000, self.get_next_question)

