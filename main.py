from requests_html import HTMLSession
import time
import keyboard as keyboard
import win32api
import win32con
from bs4 import BeautifulSoup


session = HTMLSession()


def click(pair):
    win32api.SetCursorPos(pair)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def get_soup(game_id):
    url = "https://lichess.org/" + game_id
    r = session.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def get_last_move(game_id):
    soup = get_soup(game_id)
    tables = soup.find("cg-board").find_all("square")
    if not tables:
        soup = get_soup(game_id)
        for elem in soup.find_all("script"):
            if "lastMove" in str(elem):
                script_with_last_move = str(elem)
                break

        script_with_last_move = script_with_last_move[script_with_last_move.find("lastMove"):]
        script_with_last_move = script_with_last_move[:script_with_last_move.find(',')]
        last_move = script_with_last_move[script_with_last_move.find(':') + 2: -1]
        last_move = [last_move[:2], last_move[2:]]
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        last_move = [(8 - int(last_move[0][1]), letters.index(last_move[0][0])),
                     (8 - int(last_move[1][1]), letters.index(last_move[1][0]))]
        return last_move

    last_move_pos = []
    for elem in tables:
        last_move_pos.append(elem.get("style"))
    for i in range(2):
        split_move = last_move_pos[i].split(';')
        split_move[0] = split_move[0][split_move[0].index(':') + 1: -1]
        split_move[1] = split_move[1][split_move[1].index(':') + 1: -1]
        last_move_pos[i] = (int(float(split_move[0]) * 0.08), int(float(split_move[1]) * 0.08))

    return last_move_pos


def get_reverse_last_move(game_id):
    last_move_pos = get_last_move(game_id)
    last_move_pos[0] = (7 - last_move_pos[0][0], 7 - last_move_pos[0][1])
    last_move_pos[1] = (7 - last_move_pos[1][0], 7 - last_move_pos[1][1])
    return last_move_pos


def color_of_move(game_id):
    soup = get_soup(game_id)
    if "\"white\",\"turns\"" in str(soup):
        return "white"
    return "black"


def is_the_game_over(game_id):
    soup = get_soup(game_id)
    return "[Result" in soup.text


real_game_id = "2GCkXI9v"
ai_game_id = "l8uzrRTv"

li_chess_real_pos = [[0] * 8 for i in range(8)]
li_chess_ai_pos = [[0] * 8 for i in range(8)]

for i in range(8):
    for j in range(8):
        li_chess_real_pos[i][j] = (52 + j * 75 + 30, 164 + i * 75 + 30)

# # AI
# for i in range(8):
#     for j in range(8):
#         li_chess_real_pos[i][j] = (59 + j*74 + 30, 172 + i*74 + 30)

for i in range(8):
    for j in range(8):
        li_chess_ai_pos[i][j] = (1019 + j * 74 + 30, 172 + i * 74 + 30)

while True:
    if keyboard.is_pressed('b'):
        color = "black"
        break
    if keyboard.is_pressed('w'):
        color = "white"
        break

while not is_the_game_over(real_game_id):
    if color == "white":
        time.sleep(0.1)
        while color_of_move(ai_game_id) == "white":
            time.sleep(2)
        last_ai_move = get_last_move(ai_game_id)
        click(li_chess_real_pos[last_ai_move[0][0]][last_ai_move[0][1]])
        click(li_chess_real_pos[last_ai_move[1][0]][last_ai_move[1][1]])

        time.sleep(0.1)
        while color_of_move(real_game_id) == "black":
            time.sleep(2)
        last_real_move = get_reverse_last_move(real_game_id)
        click(li_chess_ai_pos[last_real_move[0][0]][last_real_move[0][1]])
        click(li_chess_ai_pos[last_real_move[1][0]][last_real_move[1][1]])

    else:
        time.sleep(0.1)
        while color_of_move(real_game_id) == "white":
            time.sleep(2)
        last_real_move = get_last_move(real_game_id)
        click(li_chess_ai_pos[last_real_move[0][0]][last_real_move[0][1]])
        click(li_chess_ai_pos[last_real_move[1][0]][last_real_move[1][1]])

        time.sleep(0.1)
        while color_of_move(ai_game_id) == "black":
            time.sleep(2)
        last_ai_move = get_reverse_last_move(ai_game_id)
        click(li_chess_real_pos[last_ai_move[0][0]][last_ai_move[0][1]])
        click(li_chess_real_pos[last_ai_move[1][0]][last_ai_move[1][1]])

