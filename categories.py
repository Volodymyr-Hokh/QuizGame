from enum import Enum
# import requests
# import re

class Category(Enum):
    GENERAL_KNOWLEDGE = 9
    ENTERTAINMENT_BOOKS = 10
    ENTERTAINMENT_FILM = 11
    ENTERTAINMENT_MUSIC = 12
    ENTERTAINMENT_MUSICALS__THEATRES = 13
    ENTERTAINMENT_TELEVISION = 14
    ENTERTAINMENT_VIDEO_GAMES = 15
    ENTERTAINMENT_BOARD_GAMES = 16
    SCIENCE__NATURE = 17
    SCIENCE_COMPUTERS = 18
    SCIENCE_MATHEMATICS = 19
    MYTHOLOGY = 20
    SPORTS = 21
    GEOGRAPHY = 22
    HISTORY = 23
    POLITICS = 24
    ART = 25
    CELEBRITIES = 26
    ANIMALS = 27
    VEHICLES = 28
    ENTERTAINMENT_COMICS = 29
    SCIENCE_GADGETS = 30
    ENTERTAINMENT_JAPANESE_ANIME__MANGA = 31
    ENTERTAINMENT_CARTOON__ANIMATIONS = 32



# response = requests.get(url="https://opentdb.com/api_category.php")
# data = response.json()["trivia_categories"]

# print(data)

# for i in data:
#     print(re.sub(r"\W", "_", i["name"]).upper().replace("__", "_")+" = "+f"{i['id']}")