from player import Player
from lobby import Lobby

player1 = Player("Nagibator")
player2 = Player("Killer")
player3 = Player("Destroyer")

lobby = Lobby(player1)
lobby.add_player(player2)
lobby.add_player(player3)

# print(lobby.quiz.question_list)

lobby.start()
print("Game started")
q1 = lobby.next_question(just_started=True)

player1.answer(True)
player2.answer(False)
player3.answer(False)

print(lobby.all_players_answered())

q2 = lobby.next_question()
player1.answer(True)
player2.answer(False)
player3.answer(False)

print(lobby.all_players_answered())
print(player1.score, player2.score, player3.score)