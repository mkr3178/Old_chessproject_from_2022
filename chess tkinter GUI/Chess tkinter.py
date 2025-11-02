import pyautogui
import subprocess
import pyperclip
import time
from tkinter import *
import random
import math
import os
import atexit
from PIL import Image, ImageTk, ImageOps
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt='%m/%d/%Y %H:%M:%S')
handler = RotatingFileHandler('debug.log', maxBytes=2000000, backupCount=0)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False
game_log = logging.getLogger("Move_Record")
game_log.setLevel(logging.DEBUG)
game_handler = RotatingFileHandler('game.log', maxBytes=2000000, backupCount=0)
game_formatter = logging.Formatter('%(message)s')
game_handler.setFormatter(game_formatter)
game_log.addHandler(game_handler)
game_log.propagate = True
logger.debug("Application start-up")
window = Tk()
window.title("Chess")
logo = ImageTk.PhotoImage(Image.open("wp.png").resize((60, 60)))
window.iconphoto(True, logo)
clearer = ImageTk.PhotoImage(Image.open("clear.png").resize((60, 60)))
p = ImageTk.PhotoImage(Image.open("bp.png").resize((60, 60)))
P = ImageTk.PhotoImage(Image.open("wp.png").resize((60, 60)))
n = ImageTk.PhotoImage(Image.open("bn.png").resize((60, 60)))
N = ImageTk.PhotoImage(Image.open("wn.png").resize((60, 60)))
b = ImageTk.PhotoImage(Image.open("bb.png").resize((60, 60)))
B = ImageTk.PhotoImage(Image.open("wb.png").resize((60, 60)))
r = ImageTk.PhotoImage(Image.open("br.png").resize((60, 60)))
R = ImageTk.PhotoImage(Image.open("wr.png").resize((60, 60)))
k = ImageTk.PhotoImage(Image.open("bk.png").resize((60, 60)))
K = ImageTk.PhotoImage(Image.open("wk.png").resize((60, 60)))
q = ImageTk.PhotoImage(Image.open("bq.png").resize((60, 60)))
Q = ImageTk.PhotoImage(Image.open("wq.png").resize((60, 60)))
save_game = []
starboard = [
    "r", "n", "b", "q", "k", "b", "n", "r",
    "p", "p", "p", "p", "p", "p", "p", "p",
    "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "",
    "P", "P", "P", "P", "P", "P", "P", "P",
    "R", "N", "B", "Q", "K", "B", "N", "R",
]
looking = 0
loss = False
draw = False
blackface = [q, r, b, n]
white_piece = [Q, R, B, N]
promotable_piece = ["q", "r", "b", "n"]
buttons = []
board = [""] * 64
AtoH = ["A", "B", "C", "D", "E", "F", "G", "H"]
promoter = [Button(window)]
promoter[0].config(state=DISABLED, image=Q)
promoter.append(Button(window, state=DISABLED, image=R))
promoter.append(Button(window, state=DISABLED, image=B))
promoter.append(Button(window, state=DISABLED, image=N))
for i in range(len(promoter)):
    promoter[i].grid(row=i // 2 + 5, column=i % 2 + 9)
    promoter[i].grid_remove()
blackmailer = Label(window)
whitewater = Label(window)


def promote(piece, index, starburst_internal):
    if starburst_internal:
        for i in range(len(promotable_piece)):
            promotable_piece[i] = promotable_piece[i].lower()

    elif not starburst_internal:
        for i in range(len(promotable_piece)):
            promotable_piece[i] = promotable_piece[i].upper()
    board[index] = promotable_piece[piece]
    board_to_button()
    for i in range(len(promoter)):
        promoter[i].grid(row=i // 2 + 5, column=i % 2 + 9)
        promoter[i].grid_remove()


def activate_square(index):
    global buttons
    global board
    if tursvart:
        if board[index].isupper() or board[index] == "":
            buttons[index].config(state=ACTIVE)
            return True
        else:
            return False
    elif not tursvart:
        if board[index].islower() or board[index] == "":
            buttons[index].config(state=ACTIVE)
            return True
        else:
            return False
    # print("i did my thing")


def start_mode():
    if not tursvart:
        if board[0].isupper():
            buttons[0].config(state=ACTIVE)
            window.update()
        else:
            buttons[0].config(state=DISABLED)
        for i in range(len(board)):
            if board[i].isupper():
                buttons[i].config(state=ACTIVE)
            else:
                buttons[i].config(state=DISABLED)
                window.update()
    elif tursvart:
        if board[0].islower():
            buttons[0].config(state=ACTIVE)
            window.update()
        else:
            buttons[0].config(state=DISABLED)
        for i in range(len(board)):
            if board[i].islower():
                buttons[i].config(state=ACTIVE)
                window.update()
            else:
                buttons[i].config(state=DISABLED)
    window.update()


def is_enemy(index):
    if tursvart:
        if board[index].isupper():
            return True
        elif board[index].islower():
            return False
        else:
            pass
    elif not tursvart:
        if board[index].islower():
            return True
        elif board[index].isupper():
            return False
        else:
            pass


class Queen:
    @staticmethod
    def activate(index):
        start_mode()

        def right(step):
            right = index + step
            return right

        def up(step):
            up = index - (step * 8)
            return up

        def down(step):
            down = index + (step * 8)
            return down

        def left(step):
            left = index - step
            return left

        def leftup(step):
            value = index - (step * 9)
            return value

        def leftdown(step):
            value = index + (step * 7)
            return value

        def rightup(step):
            value = index - (step * 7)
            return value

        def rightdown(step):
            value = index + (step * 9)
            return value

        if index // 8 != 0 and index % 8 != 0:
            step = 1
            endpoint = False
            while leftup(step) >= 0 and not endpoint and board[leftup(step)] == "":
                if not King.causecheck(leftup(step), index): activate_square(leftup(step))
                if leftup(step) % 8 == 0:
                    endpoint = True
                step += 1
            if leftup(step) < 0 or endpoint:
                pass
            elif is_enemy(leftup(step)):
                if not King.causecheck(leftup(step), index): activate_square(leftup(step))
        if index // 8 != 0 and index % 8 != 7:
            step = 1
            endpoint = False
            while not endpoint and board[rightup(step)] == "":
                if not King.causecheck(rightup(step), index): activate_square(rightup(step))
                if rightup(step) % 8 == 7 or rightup(step) // 8 == 0:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif is_enemy(rightup(step)):
                if not King.causecheck(rightup(step), index): activate_square(rightup(step))
        if index // 8 != 7 and index % 8 != 0:
            step = 1
            endpoint = False
            while not endpoint and board[leftdown(step)] == "":
                if not King.causecheck(leftdown(step), index): activate_square(leftdown(step))
                if leftdown(step) % 8 == 0 or leftdown(step) // 8 == 7:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif is_enemy(leftdown(step)):
                if not King.causecheck(leftdown(step), index): activate_square(leftdown(step))
        if index // 8 != 7 and index % 8 != 7:
            step = 1
            endpoint = False
            while not endpoint and board[rightdown(step)] == "":
                if not King.causecheck(rightdown(step), index): activate_square(rightdown(step))
                if rightdown(step) % 8 == 7 or rightdown(step) // 8 == 7:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif is_enemy(rightdown(step)):
                if not King.causecheck(rightdown(step), index): activate_square(rightdown(step))
        if index % 8 != 0:
            steg = 1
            while index // 8 == left(steg) // 8 and board[left(steg)] == "":
                if not King.causecheck(left(steg), index): activate_square(left(steg))
                steg += 1
            if left(steg) // 8 != index // 8:
                pass
            if is_enemy(left(steg)):
                if not King.causecheck(left(steg), index): activate_square(left(steg))
        if index % 8 != 7:
            steg = 1
            while index // 8 == right(steg) // 8 and board[right(steg)] == "":
                if not King.causecheck(right(steg), index): activate_square(right(steg))
                steg += 1
            if right(steg) // 8 != index // 8:
                pass
            elif is_enemy(right(steg)):
                if not King.causecheck(right(steg), index): activate_square(right(steg))
        if index // 8 + 1 != 1:
            steg = 1
            while up(steg) >= 0 and board[up(steg)] == "":
                if not King.causecheck(up(steg), index): activate_square(up(steg))
                steg += 1
            if up(steg) < 0:
                pass
            elif is_enemy(up(steg)):
                if not King.causecheck(up(steg), index): activate_square(up(steg))
        if index // 8 + 1 != 8:
            steg = 1
            while down(steg) <= 63 and board[down(steg)] == "":
                if not King.causecheck(down(steg), index): activate_square(down(steg))
                steg += 1
            if down(steg) > 63:
                pass
            elif is_enemy(down(steg)):
                if not King.causecheck(down(steg), index): activate_square(down(steg))


class Rook:
    @staticmethod
    def activate(index):
        start_mode()

        def right(step):
            right = index + step
            return right

        def up(step):
            up = index - (step * 8)
            return up

        def down(step):
            down = index + (step * 8)
            return down

        def left(step):
            left = index - step
            return left

        if index % 8 != 0:
            steg = 1
            while index // 8 == left(steg) // 8 and board[left(steg)] == "":
                if not King.causecheck(left(steg), index): activate_square(left(steg))
                steg += 1
            if left(steg) // 8 != index // 8:
                pass
            if is_enemy(left(steg)):
                if not King.causecheck(left(steg), index): activate_square(left(steg))
        if index % 8 != 7:
            steg = 1
            while index // 8 == right(steg) // 8 and board[right(steg)] == "":
                if not King.causecheck(right(steg), index): activate_square(right(steg))
                steg += 1
            if right(steg) // 8 != index // 8:
                pass
            elif is_enemy(right(steg)):
                if not King.causecheck(right(steg), index): activate_square(right(steg))
        if index // 8 + 1 != 1:
            steg = 1
            while up(steg) >= 0 and board[up(steg)] == "":
                if not King.causecheck(up(steg), index): activate_square(up(steg))
                steg += 1
            if up(steg) < 0:
                pass
            elif is_enemy(up(steg)):
                if not King.causecheck(up(steg), index): activate_square(up(steg))
        if index // 8 + 1 != 8:
            steg = 1
            while down(steg) <= 63 and board[down(steg)] == "":
                if not King.causecheck(down(steg), index): activate_square(down(steg))
                steg += 1
            if down(steg) > 63:
                pass
            elif is_enemy(down(steg)):
                if not King.causecheck(down(steg), index): activate_square(down(steg))


class Bishop:
    @staticmethod
    def activate(index):
        start_mode()

        def left_up(step_1):
            value = index - (step_1 * 9)
            return value

        def left_down(step_2):
            value = index + (step_2 * 7)
            return value

        def right_up(step_3):
            value = index - (step_3 * 7)
            return value

        def right_down(step_4):
            value = index + (step_4 * 9)
            return value

        if index // 8 != 0 and index % 8 != 0:
            step = 1
            endpoint = False
            while left_up(step) >= 0 and not endpoint and board[left_up(step)] == "":
                if not King.causecheck(left_up(step), index):
                    activate_square(left_up(step))
                if left_up(step) % 8 == 0:
                    endpoint = True
                step += 1
            if left_up(step) < 0 or endpoint:
                pass
            elif is_enemy(left_up(step)):
                if not King.causecheck(left_up(step), index):
                    activate_square(left_up(step))
        if index // 8 != 0 and index % 8 != 7:
            step = 1
            endpoint = False
            while not endpoint and board[right_up(step)] == "":
                if not King.causecheck(right_up(step), index):
                    activate_square(right_up(step))
                if right_up(step) % 8 == 7 or right_up(step) // 8 == 0:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif is_enemy(right_up(step)):
                if not King.causecheck(right_up(step), index):
                    activate_square(right_up(step))
        if index // 8 != 7 and index % 8 != 0:
            step = 1
            endpoint = False
            while not endpoint and board[left_down(step)] == "":
                if not King.causecheck(left_down(step), index):
                    activate_square(left_down(step))
                if left_down(step) % 8 == 0 or left_down(step) // 8 == 7:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif is_enemy(left_down(step)):
                if not King.causecheck(left_down(step), index):
                    activate_square(left_down(step))
        if index // 8 != 7 and index % 8 != 7:
            step = 1
            endpoint = False
            while not endpoint and board[right_down(step)] == "":
                if not King.causecheck(right_down(step), index):
                    activate_square(right_down(step))
                if right_down(step) % 8 == 7 or right_down(step) // 8 == 7:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif is_enemy(right_down(step)):
                if not King.causecheck(right_down(step), index):
                    activate_square(right_down(step))


class Knight:
    @staticmethod
    def activate(index):
        start_mode()
        rightup = index - 6
        rightdown = index + 10
        leftup = index - 10
        leftdown = index + 6
        topright = index - 15
        topleft = index - 17
        bottomright = index + 17
        bottomleft = index + 15
        start_mode()
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 7 and not King.causecheck(topright, index):
            activate_square(topright)
            # print(topright)
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 0 and not King.causecheck(topleft, index):
            activate_square(topleft)
            # print(topleft)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 7 and not King.causecheck(bottomright, index):
            activate_square(bottomright)
            # print(bottomright)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 0 and not King.causecheck(bottomleft, index):
            activate_square(bottomleft)
            # print(bottomleft)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 1 and not King.causecheck(rightup, index):
            activate_square(rightup)
            # print(rightup)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 8 and not King.causecheck(rightdown, index):
            activate_square(rightdown)
            # print(rightdown)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 1 and not King.causecheck(leftup, index):
            activate_square(leftup)
            # print(leftup)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 8 and not King.causecheck(leftdown, index):
            activate_square(leftdown)
            # print(leftdown)


class Promotion:
    file = 64
    stoppare = True

    @classmethod
    def white(cls, index):
        cls.file = index

    @classmethod
    def black(cls, index):
        cls.file = index

    @classmethod
    def promotion(cls, index):
        global tursvart
        if index == cls.file:
            for i in range(len(buttons)):
                buttons[i].config(state=DISABLED)
            for i in range(len(promoter)):
                promoter[i].config(state=ACTIVE)
            if tursvart:
                for i in range(len(promoter)):
                    promoter[i].config(image=blackface[i])
            elif not tursvart:
                for i in range(len(promoter)):
                    promoter[i].config(image=white_piece[i])
            for i in range(len(promoter)):
                promoter[i].config(command=lambda tal=i, req=tursvart: promote(tal, index, req))
                promoter[i].grid(row=i // 2 + 5, column=i % 2 + 9)
            window.update()
            cls.file = 64


class Enpassent:
    index = 64

    @classmethod
    def insertsindex(cls, index):
        cls.index = index

    @classmethod
    def twostep(cls, index):
        spawner = "p"
        if tursvart:
            spawner = spawner.title()
        elif not tursvart:
            spawner = spawner.lower()
        if board[index - 1] == spawner and index % 8 != 0 or board[index + 1] == spawner and index % 8 != 7:
            if tursvart:
                cls.index = index - 8
            elif not tursvart:
                cls.index = index + 8
        if board[index + 1] == spawner and board[index - 1] == spawner and index % 8 != 7 and index % 8 != 0:
            if not tursvart:
                cls.index = index + 8
            elif tursvart:
                cls.index = index - 8

    @classmethod
    def resetvar(cls):
        cls.index = 64


class Bpawn:
    @staticmethod
    def activate(index):
        ones = index + 8
        twos = index + 16
        diagonalleft = index + 7
        diagonalright = index + 9
        for i in range(64):
            if board[i].islower():
                buttons[i].config(state=ACTIVE)
                window.update()
            else:
                buttons[i].config(state=DISABLED)
                window.update()

        if index % 8 == 7:
            if board[diagonalleft].isupper() and not King.causecheck(diagonalleft, index):
                buttons[diagonalleft].config(state=ACTIVE)
        elif index % 8 == 0:
            if board[diagonalright].isupper() and not King.causecheck(diagonalright, index):
                buttons[diagonalright].config(state=ACTIVE)
        else:
            if board[diagonalleft].isupper() and not King.causecheck(diagonalleft, index):
                buttons[diagonalleft].config(state=ACTIVE)
            if board[diagonalright].isupper() and not King.causecheck(diagonalright, index):
                buttons[diagonalright].config(state=ACTIVE)
        if board[ones] == "":
            if not King.causecheck(ones, index):
                buttons[ones].config(state=ACTIVE)
            if index // 8 + 1 == 2 and board[twos] == "" and not King.causecheck(twos, index):
                buttons[twos].config(state=ACTIVE)
        if Enpassent.index == diagonalleft and index // 8 == 4 and not King.causecheckenpassent(diagonalleft, index):
            buttons[diagonalleft].config(state=ACTIVE)
        if Enpassent.index == diagonalright and index // 8 == 4 and not King.causecheckenpassent(diagonalright, index):
            buttons[diagonalright].config(state=ACTIVE)


class WPawn:
    @staticmethod
    def activate(index):
        ones = index - 8
        twos = index - 16
        diagonalleft = index - 7
        diagonalright = index - 9
        for i in range(64):
            if board[i].isupper():
                buttons[i].config(state=ACTIVE)
                window.update()
            else:
                buttons[i].config(state=DISABLED)
                window.update()
        if index % 8 == 7:
            if board[diagonalright].islower() and not King.causecheck(diagonalright, index):
                buttons[diagonalright].config(state=ACTIVE)
        elif index % 8 == 0:
            if board[diagonalleft].islower() and not King.causecheck(diagonalleft, index):
                buttons[diagonalleft].config(state=ACTIVE)
        else:
            if board[diagonalleft].islower() and not King.causecheck(diagonalleft, index):
                buttons[diagonalleft].config(state=ACTIVE)
            if board[diagonalright].islower() and not King.causecheck(diagonalright, index):
                buttons[diagonalright].config(state=ACTIVE)
        if board[ones] == "":
            if not King.causecheck(ones, index):
                buttons[ones].config(state=ACTIVE)
            if index // 8 + 1 == 7 and board[twos] == "" and not King.causecheck(twos, index):
                buttons[twos].config(state=ACTIVE)
        if Enpassent.index == diagonalleft and index // 8 == 3 and not King.causecheckenpassent(diagonalleft, index):
            buttons[diagonalleft].config(state=ACTIVE)
        if Enpassent.index == diagonalright and index // 8 == 3 and not King.causecheckenpassent(diagonalright, index):
            buttons[diagonalright].config(state=ACTIVE)


class King:
    blackkingmoved = False
    whitekingmoved = False
    blackrookqueenside = False
    whiterookqueenside = False
    blackrookkingside = False
    whiterookkingside = False
    numberofattackers = 0

    @staticmethod
    def cantgoanywhere(index):
        out = True
        up = index - 8
        down = index + 8
        left = index - 1
        right = index + 1
        leftup = index - 9
        leftdown = index + 7
        rightup = index - 7
        rightdown = index + 9
        if index // 8 + 1 != 1 and King.isattacked(up) == False and not King.causecheck(up, index):
            if activate_square(up):
                out = False
        if index // 8 + 1 != 8 and King.isattacked(down) == False and not King.causecheck(down, index):
            if activate_square(down):
                out = False
        if index % 8 != 0 and King.isattacked(left) == False and not King.causecheck(left, index):
            if activate_square(left):
                out = False
        if index % 8 != 7 and King.isattacked(right) == False and not King.causecheck(right, index):
            if activate_square(right):
                out = False
        if index // 8 != 0 and index % 8 != 0 and King.isattacked(leftup) == False and not King.causecheck(leftup,
                                                                                                           index):
            if activate_square(leftup):
                out = False
        if index // 8 != 7 and index % 8 != 0 and King.isattacked(leftdown) == False and not King.causecheck(leftdown,
                                                                                                             index):
            if activate_square(leftdown):
                out = False
        if index // 8 != 0 and index % 8 != 7 and King.isattacked(rightup) == False and not King.causecheck(rightup,
                                                                                                            index):
            if activate_square(rightup):
                out = False
        if index // 8 != 7 and index % 8 != 7 and King.isattacked(rightdown) == False and not King.causecheck(rightdown,
                                                                                                              index):
            if activate_square(rightdown):
                out = False
        return out

    @staticmethod
    def losscheck():
        global loss
        global stoppedwhite
        global stoppedblack
        p = "P"
        b = "B"
        n = "N"
        r = "R"
        q = "Q"
        k = "K"
        loss = False
        if tursvart:
            p = p.lower()
            b = b.lower()
            n = n.lower()
            r = r.lower()
            q = q.lower()
            k = k.lower()
        elif not tursvart:
            p = p.title()
            b = b.title()
            n = n.title()
            r = r.title()
            q = q.title()
            k = k.title()
        if King.isattacked(board.index(k)):
            if King.cantgoanywhere(board.index(k)):
                if King.countattacker(board.index(k)) < 2:
                    # logger.debug("only one attacker")
                    interfearens = King.interfearingsqr(board.index(k))
                    loss = True
                    # textat = str(interfearens)
                    # logger.debug(textat)
                    for i in interfearens:
                        # txtt = "checking" + str(i)
                        # logger.debug(txtt)
                        if King.isprotected(i):
                            # logger.debug("square was protected")
                            loss = False
                elif King.countattacker(board.index(k)) >= 2:
                    loss = True
        if loss:
            color = "White"
            if tursvart:
                color = "Black"
                blackmailer.config(bg="red")
            else:
                whitewater.config(bg="red")
            stoppedwhite = True
            stoppedblack = True
            for i in range(len(buttons)):
                buttons[i].config(state=DISABLED)
            # print(color, "lost the game")

    @staticmethod
    def isprotected(index):
        out = False
        global tursvart
        pawn = "P"
        bee = "B"
        night = "N"
        rookie = "R"
        queens = "Q"
        kings = "K"
        if tursvart:
            pawn = pawn.lower()
            bee = bee.lower()
            night = night.lower()
            rookie = rookie.lower()
            queens = queens.lower()
            kings = kings.lower()
        elif not tursvart:
            pawn = pawn.upper()
            bee = bee.upper()
            night = night.upper()
            rookie = rookie.upper()
            queens = queens.upper()
            kings = kings.upper()

        def right(step):
            right = index + step
            return right

        def up(step):
            up = index - (step * 8)
            return up

        def down(step):
            down = index + (step * 8)
            return down

        def left(step):
            left = index - step
            return left

        def leftup(step):
            value = index - (step * 9)
            return value

        def leftdown(step):
            value = index + (step * 7)
            return value

        def rightup(step):
            value = index - (step * 7)
            return value

        def rightdown(step):
            value = index + (step * 9)
            return value

        nrightup = index - 6
        nrightdown = index + 10
        nleftup = index - 10
        nleftdown = index + 6
        ntopright = index - 15
        ntopleft = index - 17
        nbottomright = index + 17
        nbottomleft = index + 15
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 7:
            if board[ntopright] == night and not King.causecheck(index, ntopright):
                # print(ntopright, "ntopright", board[ntopright])
                out = True
            # print(topright)
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 0:
            if board[ntopleft] == night and not King.causecheck(index, ntopleft):
                # print(ntopleft, "ntopleft", board[ntopleft])
                out = True
            # print(topleft)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 7:
            if board[nbottomright] == night and not King.causecheck(index, nbottomright):
                # print(nbottomright, "nbottomright", board[nbottomright])
                out = True
            # print(bottomright)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 0:
            if board[nbottomleft] == night and not King.causecheck(index, nbottomleft):
                # print(nbottomleft, "nbottomleft", board[nbottomleft])
                out = True
            # print(bottomleft)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 1:
            if board[nrightup] == night and not King.causecheck(index, nrightup):
                # print(nrightup, "nrightup", board[nrightup])
                out = True
            # print(rightup)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 8:
            if board[nrightdown] == night and not King.causecheck(index, nrightdown):
                # print(nrightdown, "nrightdown", board[nrightdown])
                out = True
            # print(rightdown)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 1:
            if board[nleftup] == night and not King.causecheck(index, nleftup):
                # print(nleftup, "nleftup", board[nleftup])
                out = True
            # print(leftup)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 8:
            if board[nleftdown] == night and not King.causecheck(index, nleftdown):
                # print(nleftdown, "nleftdown", board[nleftdown])
                out = True
            # print(leftdown)
        if index // 8 != 0 and index % 8 != 0:
            step = 1
            endpoint = False
            if board[leftup(step)] == kings and not King.causecheck(index, leftup(step)):
                # print("kingattak", leftup(step))
                out = True
            while leftup(step) >= 0 and not endpoint and board[leftup(step)] == "":
                step += 1
                if leftup(step) % 8 == 0 or leftup(step) // 8 == 0:
                    endpoint = True
            if (board[leftup(step)] == bee or board[leftup(step)] == queens) and not King.causecheck(index,
                                                                                                     leftup(step)):
                # print(leftup(step), "leftup", step, board[leftup(step)])
                out = True
        if index // 8 != 0 and index % 8 != 7:
            step = 1
            endpoint = False
            if board[rightup(step)] == kings and not King.causecheck(index, rightup(step)):
                # print("kingattack", rightup(step))
                out = True
            while not endpoint and board[rightup(step)] == "":
                if rightup(step) % 8 == 7 or rightup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if is_enemy(rightup(step)):
                pass
            elif (board[rightup(step)] == bee or board[rightup(step)] == queens) and not King.causecheck(index,
                                                                                                         rightup(step)):
                # print(rightup(step), "rightup", step, board[rightup(step)])
                out = True
        if index // 8 != 7 and index % 8 != 0:
            step = 1
            endpoint = False
            if board[leftdown(step)] == kings and not King.causecheck(index, leftdown(step)):
                # print("kingattack", leftdown(step))
                out = True
            while not endpoint and board[leftdown(step)] == "":
                if leftdown(step) % 8 == 0 or leftdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if is_enemy(leftdown(step)):
                pass
            elif (board[leftdown(step)] == bee or board[leftdown(step)] == queens) and not King.causecheck(index,
                                                                                                           leftdown(
                                                                                                               step)):
                # print(leftdown(step), "leftdown", step, board[leftdown(step)])
                out = True
        if index // 8 != 7 and index % 8 != 7:
            step = 1
            endpoint = False
            if board[rightdown(step)] == kings and not King.causecheck(index, rightdown(step)):
                # print("kingattack", rightdown(step))
                out = True
            while not endpoint and board[rightdown(step)] == "":
                if rightdown(step) % 8 == 7 or rightdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if is_enemy(rightdown(step)):
                pass
            elif (board[rightdown(step)] == bee or board[rightdown(step)] == queens) and not King.causecheck(index,
                                                                                                             rightdown(
                                                                                                                 step)):
                # print(rightdown(step), "rightdown", step, board[rightdown(step)])
                out = True
        if index % 8 != 0:
            steg = 1
            if board[left(steg)] == kings and not King.causecheck(index, left(steg)):
                # print("kingattack", left(steg))
                out = True
            while index // 8 == left(steg) // 8 and board[left(steg)] == "":
                steg += 1
            if left(steg) // 8 != index // 8:
                pass
            elif is_enemy(left(steg)):
                pass
            elif (board[left(steg)] == rookie or board[left(steg)] == queens) and not King.causecheck(index,
                                                                                                      left(steg)):
                # print(left(steg), "left", steg, board[left(steg)])
                out = True
        if index % 8 != 7:
            steg = 1
            if board[right(steg)] == kings and not King.causecheck(index, right(steg)):
                # print("kingattack", right(steg))
                out = True
            while index // 8 == right(steg) // 8 and board[right(steg)] == "":
                steg += 1
            if right(steg) // 8 != index // 8:
                pass
            elif is_enemy(right(steg)):
                pass
            elif (board[right(steg)] == rookie or board[right(steg)] == queens) and not King.causecheck(index,
                                                                                                        right(steg)):
                # print(right(steg), "right", steg, board[right(steg)])
                out = True
        if index // 8 + 1 != 1:
            steg = 1
            if board[up(steg)] == kings and not King.causecheck(index, up(steg)):
                # print("kingattack", up(steg))
                out = True
            while up(steg) >= 0 and board[up(steg)] == "":
                steg += 1
            if up(steg) < 0:
                pass
            elif is_enemy(up(steg)):
                pass
            elif (board[up(steg)] == rookie or board[up(steg)] == queens) and not King.causecheck(index, up(steg)):
                # print(up(steg), "up", steg, board[up(steg)])
                out = True
        if index // 8 + 1 != 8:
            steg = 1
            if board[down(steg)] == kings and not King.causecheck(index, down(steg)):
                # print("kingattack", down(steg))
                out = True
            while down(steg) <= 63 and board[down(steg)] == "":
                steg += 1
            if down(steg) > 63:
                pass
            elif (board[down(steg)] == rookie or board[down(steg)] == queens) and not King.causecheck(index,
                                                                                                      down(steg)):
                # print(down(steg), "down", steg, board[down(steg)])
                out = True
        if tursvart:
            if index // 8 != 0 and index % 8 != 0:
                if board[leftup(1)] == pawn and not King.causecheck(index, leftup(1)) and is_enemy(index) \
                        or index + 8 == Enpassent. \
                        index and board[index - 1] == pawn and not King.causecheckenpassent(Enpassent.index, index - 1):
                    # print("pawnattack", leftup(1))
                    out = True
            if index // 8 != 0 and index % 8 != 7:
                if board[rightup(1)] == pawn and not King.causecheck(index, rightup(1)) and is_enemy(index) \
                        or index + 8 == Enpassent. \
                        index and board[index + 1] == pawn and not King.causecheckenpassent(Enpassent.index, index + 1):
                    # print("pawnattack", rightup(1))
                    out = True
            if board[index] == "" and index // 8 != 0:
                if board[index - 8] == pawn and not King.causecheck(index, index - 8):
                    out = True
            if board[index] == "" and index // 8 == 3:
                if board[index - 16] == pawn and not King.causecheck(index, index - 16):
                    out = True
        if not tursvart:
            if index // 8 != 7 and index % 8 != 0:
                if board[leftdown(1)] == pawn and not King.causecheck(index, leftdown(1)) and is_enemy(index) \
                        or index - 8 == Enpassent.index and board[index - 1] == pawn and \
                        not King.causecheckenpassent(Enpassent.index, index - 1):
                    # print("pawnattack", leftdown(1))
                    out = True
            if index // 8 != 7 and index % 8 != 7:
                if board[rightdown(1)] == pawn and not King.causecheck(index, rightdown(1)) and is_enemy(index) \
                        or index - 8 == Enpassent. \
                        index and board[index + 1] == pawn and not King.causecheckenpassent(Enpassent.index, index + 1):
                    # print("pawnattack", rightdown(1))
                    out = True
            if board[index] == "" and index // 8 != 7:
                if board[index + 8] == pawn and not King.causecheck(index, index + 8):
                    out = True
            if board[index] == "" and index // 8 == 4:
                if board[index + 16] == pawn and not King.causecheck(index, index + 16):
                    out = True
        return out

    @staticmethod
    def interfearingsqr(index):
        out = []
        global tursvart
        pawn = "P"
        bee = "B"
        night = "N"
        rookie = "R"
        queens = "Q"
        kings = "K"
        if not tursvart:
            pawn = pawn.lower()
            bee = bee.lower()
            night = night.lower()
            rookie = rookie.lower()
            queens = queens.lower()
            kings = kings.lower()
        elif tursvart:
            pawn = pawn.upper()
            bee = bee.upper()
            night = night.upper()
            rookie = rookie.upper()
            queens = queens.upper()
            kings = kings.upper()

        def right(movements):
            right = index + movements
            return right

        def up(movements):
            up = index - (movements * 8)
            return up

        def down(movements):
            down = index + (movements * 8)
            return down

        def left(movements):
            left = index - movements
            return left

        def leftup(movements):
            value = index - (movements * 9)
            return value

        def leftdown(movements):
            value = index + (movements * 7)
            return value

        def rightup(movements):
            value = index - (movements * 7)
            return value

        def rightdown(movements):
            value = index + (movements * 9)
            return value

        nrightup = index - 6
        nrightdown = index + 10
        nleftup = index - 10
        nleftdown = index + 6
        ntopright = index - 15
        ntopleft = index - 17
        nbottomright = index + 17
        nbottomleft = index + 15
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 7:
            if board[ntopright] == night:
                # print(ntopright, "ntopright", board[ntopright])
                out.append(ntopright)
            # print(topright)
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 0:
            if board[ntopleft] == night:
                # print(ntopleft, "ntopleft", board[ntopleft])
                out.append(ntopleft)
            # print(topleft)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 7:
            if board[nbottomright] == night:
                # print(nbottomright, "nbottomright", board[nbottomright])
                out.append(nbottomright)
            # print(bottomright)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 0:
            if board[nbottomleft] == night:
                # print(nbottomleft, "nbottomleft", board[nbottomleft])
                out.append(nbottomleft)
            # print(bottomleft)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 1:
            if board[nrightup] == night:
                # print(nrightup, "nrightup", board[nrightup])
                out.append(nrightup)
            # print(rightup)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 8:
            if board[nrightdown] == night:
                # print(nrightdown, "nrightdown", board[nrightdown])
                out.append(nrightdown)
            # print(rightdown)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 1:
            if board[nleftup] == night:
                # print(nleftup, "nleftup", board[nleftup])
                out.append(nleftup)
            # print(leftup)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 8:
            if board[nleftdown] == night:
                # print(nleftdown, "nleftdown", board[nleftdown])
                out.append(nleftdown)
            # print(leftdown)
        if index // 8 != 0 and index % 8 != 0:
            step = 1
            endpoint = False
            if board[leftup(step)] == kings:
                # print("kingattak", leftup(step))
                out.append(leftup(step))
            while leftup(step) >= 0 and not endpoint and board[leftup(step)] == "":
                if leftup(step) % 8 == 0 or leftup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if board[leftup(step)] == bee or board[leftup(step)] == queens:
                # print(leftup(step), "leftup", step, board[leftup(step)])
                for i in range(step):
                    out.append(leftup(i + 1))
        if index // 8 != 0 and index % 8 != 7:
            step = 1
            endpoint = False
            if board[rightup(step)] == kings:
                # print("kingattack", rightup(step))
                out.append(rightup(step))
            while not endpoint and board[rightup(step)] == "":
                if rightup(step) % 8 == 7 or rightup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if not is_enemy(rightup(step)):
                pass
            elif board[rightup(step)] == bee or board[rightup(step)] == queens:
                # print(rightup(step), "rightup", step, board[rightup(step)])
                for i in range(step):
                    out.append(rightup(i + 1))
        if index // 8 != 7 and index % 8 != 0:
            step = 1
            endpoint = False
            if board[leftdown(step)] == kings:
                # print("kingattack", leftdown(step))
                out.append(leftdown(step))
            while not endpoint and board[leftdown(step)] == "":
                if leftdown(step) % 8 == 0 or leftdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if not is_enemy(leftdown(step)):
                pass
            elif board[leftdown(step)] == bee or board[leftdown(step)] == queens:
                # print(leftdown(step), "leftdown", step, board[leftdown(step)])
                for i in range(step):
                    out.append(leftdown(i + 1))
        if index // 8 != 7 and index % 8 != 7:
            step = 1
            endpoint = False
            if board[rightdown(step)] == kings:
                # print("kingattack", rightdown(step))
                out.append(rightdown(step))
            while not endpoint and board[rightdown(step)] == "":
                if rightdown(step) % 8 == 7 or rightdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if not is_enemy(rightdown(step)):
                pass
            elif board[rightdown(step)] == bee or board[rightdown(step)] == queens:
                # print(rightdown(step), "rightdown", step, board[rightdown(step)])
                for i in range(step):
                    out.append(rightdown(i + 1))
        if index % 8 != 0:
            steg = 1
            if board[left(steg)] == kings:
                # print("kingattack", left(steg))
                out.append(left(steg))
            while index // 8 == left(steg) // 8 and board[left(steg)] == "":
                steg += 1
            if left(steg) // 8 != index // 8:
                pass
            elif not is_enemy(left(steg)):
                pass
            elif board[left(steg)] == rookie or board[left(steg)] == queens:
                # print(left(steg), "left", steg, board[left(steg)])
                for i in range(steg):
                    out.append(left(i + 1))
        if index % 8 != 7:
            steg = 1
            if board[right(steg)] == kings:
                # print("kingattack", right(steg))
                out.append(right(steg))
            while index // 8 == right(steg) // 8 and board[right(steg)] == "":
                steg += 1
            if right(steg) // 8 != index // 8:
                pass
            elif not is_enemy(right(steg)):
                pass
            elif board[right(steg)] == rookie or board[right(steg)] == queens:
                # print(right(steg), "right", steg, board[right(steg)])
                for i in range(steg):
                    out.append(right(i + 1))
        if index // 8 + 1 != 1:
            steg = 1
            if board[up(steg)] == kings:
                # print("kingattack", up(steg))
                out.append(up(steg))
            while up(steg) >= 0 and board[up(steg)] == "":
                steg += 1
            if up(steg) < 0:
                pass
            elif not is_enemy(up(steg)):
                pass
            elif board[up(steg)] == rookie or board[up(steg)] == queens:
                # print(up(steg), "up", steg, board[up(steg)])
                for i in range(steg):
                    out.append(up(i + 1))
        if index // 8 + 1 != 8:
            steg = 1
            if board[down(steg)] == kings:
                # print("kingattack", down(steg))
                out.append(down(steg))
            while down(steg) <= 63 and board[down(steg)] == "":
                steg += 1
            if down(steg) > 63:
                pass
            elif not is_enemy(down(steg)):
                pass
            elif board[down(steg)] == rookie or board[down(steg)] == queens:
                # print(down(steg), "down", steg, board[down(steg)])
                for i in range(steg):
                    out.append(up(i + 1))
        if not tursvart:
            if index % 8 != 0:
                if board[leftup(1)] == pawn:
                    # print("pawnattack", leftup(1))
                    out.append(leftup(1))
            if index % 8 != 7:
                if board[rightup(1)] == pawn:
                    # print("pawnattack", rightup(1))
                    out.append(rightup(1))
        if tursvart:
            if index % 8 != 0:
                if board[leftdown(1)] == pawn:
                    # print("pawnattack", leftdown(1))
                    out.append(leftdown(1))
            if index % 8 != 7:
                if board[rightdown(1)] == pawn:
                    # print("pawnattack", rightdown(1))
                    out.append(rightdown(1))
        return out

    @staticmethod
    def countattacker(index):
        out = 0
        global tursvart
        pawn = "P"
        bee = "B"
        night = "N"
        rookie = "R"
        queens = "Q"
        kings = "K"
        if not tursvart:
            pawn = pawn.lower()
            bee = bee.lower()
            night = night.lower()
            rookie = rookie.lower()
            queens = queens.lower()
            kings = kings.lower()
        elif tursvart:
            pawn = pawn.upper()
            bee = bee.upper()
            night = night.upper()
            rookie = rookie.upper()
            queens = queens.upper()
            kings = kings.upper()

        def right(movements):
            right = index + movements
            return right

        def up(movements):
            up = index - (movements * 8)
            return up

        def down(movements):
            down = index + (movements * 8)
            return down

        def left(movements):
            left = index - movements
            return left

        def leftup(movements):
            value = index - (movements * 9)
            return value

        def leftdown(movements):
            value = index + (movements * 7)
            return value

        def rightup(movements):
            value = index - (movements * 7)
            return value

        def rightdown(movements):
            value = index + (movements * 9)
            return value

        nrightup = index - 6
        nrightdown = index + 10
        nleftup = index - 10
        nleftdown = index + 6
        ntopright = index - 15
        ntopleft = index - 17
        nbottomright = index + 17
        nbottomleft = index + 15
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 7:
            if board[ntopright] == night:
                # print(ntopright, "ntopright", board[ntopright])
                out += 1
            # print(topright)
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 0:
            if board[ntopleft] == night:
                # print(ntopleft, "ntopleft", board[ntopleft])
                out += 1
            # print(topleft)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 7:
            if board[nbottomright] == night:
                # print(nbottomright, "nbottomright", board[nbottomright])
                out += 1
            # print(bottomright)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 0:
            if board[nbottomleft] == night:
                # print(nbottomleft, "nbottomleft", board[nbottomleft])
                out += 1
            # print(bottomleft)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 1:
            if board[nrightup] == night:
                # print(nrightup, "nrightup", board[nrightup])
                out += 1
            # print(rightup)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 8:
            if board[nrightdown] == night:
                # print(nrightdown, "nrightdown", board[nrightdown])
                out += 1
            # print(rightdown)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 1:
            if board[nleftup] == night:
                # print(nleftup, "nleftup", board[nleftup])
                out += 1
            # print(leftup)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 8:
            if board[nleftdown] == night:
                # print(nleftdown, "nleftdown", board[nleftdown])
                out += 1
            # print(leftdown)
        if index // 8 != 0 and index % 8 != 0:
            step = 1
            endpoint = False
            if board[leftup(step)] == kings:
                # print("kingattak", leftup(step))
                out += 1
            while leftup(step) >= 0 and not endpoint and board[leftup(step)] == "":
                if leftup(step) % 8 == 0:
                    endpoint = True
                step += 1
            if leftup(step) < 0 or endpoint:
                pass
            elif board[leftup(step)] == bee or board[leftup(step)] == queens:
                # print(leftup(step), "leftup", step, board[leftup(step)])
                out += 1
        if index // 8 != 0 and index % 8 != 7:
            step = 1
            endpoint = False
            if board[rightup(step)] == kings:
                # print("kingattack", rightup(step))
                out += 1
            while not endpoint and board[rightup(step)] == "":
                if rightup(step) % 8 == 7 or rightup(step) // 8 == 0:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif not is_enemy(rightup(step)):
                pass
            elif board[rightup(step)] == bee or board[rightup(step)] == queens:
                # print(rightup(step), "rightup", step, board[rightup(step)])
                out += 1
        if index // 8 != 7 and index % 8 != 0:
            step = 1
            endpoint = False
            if board[leftdown(step)] == kings:
                # print("kingattack", leftdown(step))
                out += 1
            while not endpoint and board[leftdown(step)] == "":
                if leftdown(step) % 8 == 0 or leftdown(step) // 8 == 7:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif not is_enemy(leftdown(step)):
                pass
            elif board[leftdown(step)] == bee or board[leftdown(step)] == queens:
                # print(leftdown(step), "leftdown", step, board[leftdown(step)])
                out += 1
        if index // 8 != 7 and index % 8 != 7:
            step = 1
            endpoint = False
            if board[rightdown(step)] == kings:
                # print("kingattack", rightdown(step))
                out += 1
            while not endpoint and board[rightdown(step)] == "":
                if rightdown(step) % 8 == 7 or rightdown(step) // 8 == 7:
                    endpoint = True
                step += 1
            if endpoint:
                pass
            elif not is_enemy(rightdown(step)):
                pass
            elif board[rightdown(step)] == bee or board[rightdown(step)] == queens:
                # print(rightdown(step), "rightdown", step, board[rightdown(step)])
                out += 1
        if index % 8 != 0:
            steg = 1
            if board[left(steg)] == kings:
                # print("kingattack", left(steg))
                out += 1
            while index // 8 == left(steg) // 8 and board[left(steg)] == "":
                steg += 1
            if left(steg) // 8 != index // 8:
                pass
            elif not is_enemy(left(steg)):
                pass
            elif board[left(steg)] == rookie or board[left(steg)] == queens:
                # print(left(steg), "left", steg, board[left(steg)])
                out += 1
        if index % 8 != 7:
            steg = 1
            if board[right(steg)] == kings:
                # print("kingattack", right(steg))
                out += 1
            while index // 8 == right(steg) // 8 and board[right(steg)] == "":
                steg += 1
            if right(steg) // 8 != index // 8:
                pass
            elif not is_enemy(right(steg)):
                pass
            elif board[right(steg)] == rookie or board[right(steg)] == queens:
                # print(right(steg), "right", steg, board[right(steg)])
                out += 1
        if index // 8 + 1 != 1:
            steg = 1
            if board[up(steg)] == kings:
                # print("kingattack", up(steg))
                out += 1
            while up(steg) >= 0 and board[up(steg)] == "":
                steg += 1
            if up(steg) < 0:
                pass
            elif not is_enemy(up(steg)):
                pass
            elif board[up(steg)] == rookie or board[up(steg)] == queens:
                # print(up(steg), "up", steg, board[up(steg)])
                out += 1
        if index // 8 + 1 != 8:
            steg = 1
            if board[down(steg)] == kings:
                # print("kingattack", down(steg))
                out += 1
            while down(steg) <= 63 and board[down(steg)] == "":
                steg += 1
            if down(steg) > 63:
                pass
            elif not is_enemy(down(steg)):
                pass
            elif board[down(steg)] == rookie or board[down(steg)] == queens:
                # print(down(steg), "down", steg, board[down(steg)])
                out += 1
        if not tursvart:
            if index % 8 != 0:
                if board[leftup(1)] == pawn:
                    # print("pawnattack", leftup(1))
                    out += 1
            if index % 8 != 7:
                if board[rightup(1)] == pawn:
                    # print("pawnattack", rightup(1))
                    out += 1
        if tursvart:
            if index % 8 != 0:
                if board[leftdown(1)] == pawn:
                    # print("pawnattack", leftdown(1))
                    out += 1
            if index % 8 != 7:
                if board[rightdown(1)] == pawn:
                    # print("pawnattack", rightdown(1))
                    out += 1
        return out

    @staticmethod
    def causecheckenpassent(gotopos, oldpos):
        # print("starting process causecheckenpassent")
        global board
        fakeboard = board.copy()
        p = "P"
        b = "B"
        n = "N"
        r = "R"
        q = "Q"
        k = "K"
        if tursvart:
            p = p.lower()
            b = b.lower()
            n = n.lower()
            r = r.lower()
            q = q.lower()
            k = k.lower()
        elif not tursvart:
            p = p.title()
            b = b.title()
            n = n.title()
            r = r.title()
            q = q.title()
            k = k.title()
        # print(gotopos)
        if is_enemy(gotopos) or board[gotopos] == "":
            board[gotopos] = board[oldpos]
            board[oldpos] = ""
            if tursvart:
                board[gotopos - 8] = ""
            #    print(gotopos-8)
            elif not tursvart:
                board[gotopos + 8] = ""
            #    print(gotopos+8)
        if King.isattacked(board.index(k)):
            utgang = True
        else:
            utgang = False
        board = fakeboard.copy()
        # print(utgang)
        return utgang

    @staticmethod
    def causecheck(gotopos, oldpos):
        global board
        fakeboard = board.copy()
        k = "K"
        if tursvart:
            k = k.lower()
        elif not tursvart:
            k = k.title()
        if is_enemy(gotopos) or board[gotopos] == "":
            board[gotopos] = board[oldpos]
            board[oldpos] = ""
        if King.isattacked(board.index(k)):
            utgang = True
        else:
            utgang = False
        board = fakeboard.copy()
        return utgang

    @classmethod
    def reset(cls):
        cls.blackkingmoved = False
        cls.whitekingmoved = False
        cls.blackrookqueenside = False
        cls.whiterookqueenside = False
        cls.blackrookkingside = False
        cls.whiterookkingside = False

    @staticmethod
    def isattacked(index):
        out = False
        global tursvart
        pawn = "P"
        bee = "B"
        night = "N"
        rookie = "R"
        queens = "Q"
        kings = "K"
        if not tursvart:
            pawn = pawn.lower()
            bee = bee.lower()
            night = night.lower()
            rookie = rookie.lower()
            queens = queens.lower()
            kings = kings.lower()
        elif tursvart:
            pawn = pawn.upper()
            bee = bee.upper()
            night = night.upper()
            rookie = rookie.upper()
            queens = queens.upper()
            kings = kings.upper()

        def right(step):
            right = index + step
            return right

        def up(step):
            up = index - (step * 8)
            return up

        def down(step):
            down = index + (step * 8)
            return down

        def left(step):
            left = index - step
            return left

        def leftup(step):
            value = index - (step * 9)
            return value

        def leftdown(step):
            value = index + (step * 7)
            return value

        def rightup(step):
            value = index - (step * 7)
            return value

        def rightdown(step):
            value = index + (step * 9)
            return value

        nrightup = index - 6
        nrightdown = index + 10
        nleftup = index - 10
        nleftdown = index + 6
        ntopright = index - 15
        ntopleft = index - 17
        nbottomright = index + 17
        nbottomleft = index + 15
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 7:
            if board[ntopright] == night:
                # print(ntopright, "ntopright", board[ntopright])
                out = True
            # print(topright)
        if index // 8 + 1 != 1 and index // 8 + 1 != 2 and index % 8 != 0:
            if board[ntopleft] == night:
                # print(ntopleft, "ntopleft", board[ntopleft])
                out = True
            # print(topleft)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 7:
            if board[nbottomright] == night:
                # print(nbottomright, "nbottomright", board[nbottomright])
                out = True
            # print(bottomright)
        if index // 8 + 1 != 7 and index // 8 + 1 != 8 and index % 8 != 0:
            if board[nbottomleft] == night:
                # print(nbottomleft, "nbottomleft", board[nbottomleft])
                out = True
            # print(bottomleft)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 1:
            if board[nrightup] == night:
                # print(nrightup, "nrightup", board[nrightup])
                out = True
            # print(rightup)
        if index % 8 != 6 and index % 8 != 7 and index // 8 + 1 != 8:
            if board[nrightdown] == night:
                # print(nrightdown, "nrightdown", board[nrightdown])
                out = True
            # print(rightdown)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 1:
            if board[nleftup] == night:
                # print(nleftup, "nleftup", board[nleftup])
                out = True
            # print(leftup)
        if index % 8 != 0 and index % 8 != 1 and index // 8 + 1 != 8:
            if board[nleftdown] == night:
                # print(nleftdown, "nleftdown", board[nleftdown])
                out = True
            # print(leftdown)
        if index // 8 != 0 and index % 8 != 0:
            step = 1
            endpoint = False
            if board[leftup(step)] == kings:
                # print("kingattak", leftup(step))
                out = True
            while leftup(step) >= 0 and not endpoint and board[leftup(step)] == "":
                if leftup(step) % 8 == 0 or leftup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if board[leftup(step)] == bee or board[leftup(step)] == queens:
                # print(leftup(step), "leftup", step, board[leftup(step)])
                out = True
        if index // 8 != 0 and index % 8 != 7:
            step = 1
            endpoint = False
            if board[rightup(step)] == kings:
                # print("kingattack", rightup(step))
                out = True
            while not endpoint and board[rightup(step)] == "":
                if rightup(step) % 8 == 7 or rightup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if not is_enemy(rightup(step)):
                pass
            elif board[rightup(step)] == bee or board[rightup(step)] == queens:
                # print(rightup(step), "rightup", step, board[rightup(step)])
                out = True
        if index // 8 != 7 and index % 8 != 0:
            step = 1
            endpoint = False
            if board[leftdown(step)] == kings:
                # print("kingattack", leftdown(step))
                out = True
            while not endpoint and board[leftdown(step)] == "":
                if leftdown(step) % 8 == 0 or leftdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if not is_enemy(leftdown(step)):
                pass
            elif board[leftdown(step)] == bee or board[leftdown(step)] == queens:
                # print(leftdown(step), "leftdown", step, board[leftdown(step)])
                out = True
        if index // 8 != 7 and index % 8 != 7:
            step = 1
            endpoint = False
            if board[rightdown(step)] == kings:
                # print("kingattack", rightdown(step))
                out = True
            while not endpoint and board[rightdown(step)] == "":
                if rightdown(step) % 8 == 7 or rightdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if not is_enemy(rightdown(step)):
                pass
            elif board[rightdown(step)] == bee or board[rightdown(step)] == queens:
                # print(rightdown(step), "rightdown", step, board[rightdown(step)])
                out = True
        if index % 8 != 0:
            steg = 1
            if board[left(steg)] == kings:
                # print("kingattack", left(steg))
                out = True
            while index // 8 == left(steg) // 8 and board[left(steg)] == "":
                steg += 1
            if left(steg) // 8 != index // 8:
                pass
            elif not is_enemy(left(steg)):
                pass
            elif board[left(steg)] == rookie or board[left(steg)] == queens:
                # print(left(steg), "left", steg, board[left(steg)])
                out = True
        if index % 8 != 7:
            steg = 1
            if board[right(steg)] == kings:
                # print("kingattack", right(steg))
                out = True
            while index // 8 == right(steg) // 8 and board[right(steg)] == "":
                steg += 1
            if right(steg) // 8 != index // 8:
                pass
            elif not is_enemy(right(steg)):
                pass
            elif board[right(steg)] == rookie or board[right(steg)] == queens:
                # print(right(steg), "right", steg, board[right(steg)])
                out = True
        if index // 8 + 1 != 1:
            steg = 1
            if board[up(steg)] == kings:
                # print("kingattack", up(steg))
                out = True
            while up(steg) >= 0 and board[up(steg)] == "":
                steg += 1
            if up(steg) < 0:
                pass
            elif not is_enemy(up(steg)):
                pass
            elif board[up(steg)] == rookie or board[up(steg)] == queens:
                # print(up(steg), "up", steg, board[up(steg)])
                out = True
        if index // 8 + 1 != 8:
            steg = 1
            if board[down(steg)] == kings:
                # print("kingattack", down(steg))
                out = True
            while down(steg) <= 63 and board[down(steg)] == "":
                steg += 1
            if down(steg) > 63:
                pass
            elif not is_enemy(down(steg)):
                pass
            elif board[down(steg)] == rookie or board[down(steg)] == queens:
                # print(down(steg), "down", steg, board[down(steg)])
                out = True
        if not tursvart:
            if index // 8 != 0 and index % 8 != 0:
                if board[leftup(1)] == pawn:
                    # print("pawnattack", leftup(1))
                    out = True
            if index // 8 != 0 and index % 8 != 7:
                if board[rightup(1)] == pawn:
                    # print("pawnattack", rightup(1))
                    out = True
        if tursvart:
            if index // 8 != 7 and index % 8 != 0:
                if board[leftdown(1)] == pawn:
                    # print("pawnattack", leftdown(1))
                    out = True
            if index // 8 != 7 and index % 8 != 7:
                if board[rightdown(1)] == pawn:
                    # print("pawnattack", rightdown(1))
                    out = True
        return out

    @classmethod
    def hasmoved(cls):
        if tursvart:
            # print("black king moved")
            cls.blackkingmoved = True
        elif not tursvart:
            cls.whitekingmoved = True
            # print("white king moved")
        else:
            pass

    @classmethod
    def checkrooks(cls):
        kung = "K"
        torn = "R"
        if tursvart and not cls.blackkingmoved:
            kung = kung.lower()
            torn = torn.lower()
            if board[board.index(kung) - 4] != torn:
                cls.blackrookqueenside = True
                # print("black queen side rook has moved")
            if board[board.index(kung) + 3] != torn:
                cls.blackrookkingside = True
                # print("black king side rook has moved")
        if not tursvart and cls.whitekingmoved is False:
            kung = kung.title()
            torn = torn.title()
            if board[board.index(kung) - 4] != torn:
                cls.whiterookqueenside = True
                # print("white queen side rook has moved")
            if board[board.index(kung) + 3] != torn:
                cls.whiterookkingside = True
                # print("white king side rook has moved")
        # print(cls.blackkingmoved, cls.whitekingmoved, cls.blackrookqueenside, cls.whiterookqueenside,
        #      cls.blackrookkingside, cls.whiterookkingside)

    @staticmethod
    def activate(index):
        start_mode()
        up = index - 8
        down = index + 8
        left = index - 1
        right = index + 1
        leftup = index - 9
        leftdown = index + 7
        rightup = index - 7
        rightdown = index + 9
        if index // 8 + 1 != 1 and King.isattacked(up) == False and not King.causecheck(up, index):
            activate_square(up)
        if index // 8 + 1 != 8 and King.isattacked(down) == False and not King.causecheck(down, index):
            activate_square(down)
        if index % 8 != 0 and King.isattacked(left) == False and not King.causecheck(left, index):
            activate_square(left)
        if index % 8 != 7 and King.isattacked(right) == False and not King.causecheck(right, index):
            activate_square(right)
        if index // 8 != 0 and index % 8 != 0 and King.isattacked(leftup) == False and not King.causecheck(leftup,
                                                                                                           index):
            activate_square(leftup)
        if index // 8 != 7 and index % 8 != 0 and King.isattacked(leftdown) == False and not King.causecheck(leftdown,
                                                                                                             index):
            activate_square(leftdown)
        if index // 8 != 0 and index % 8 != 7 and King.isattacked(rightup) == False and not King.causecheck(rightup,
                                                                                                            index):
            activate_square(rightup)
        if index // 8 != 7 and index % 8 != 7 and King.isattacked(rightdown) == False and not King.causecheck(rightdown,
                                                                                                              index):
            activate_square(rightdown)
        if tursvart and not King.blackkingmoved:
            if not King.blackrookqueenside and not King.isattacked(index) and not King.isattacked(index - 1) and not \
                    King.isattacked(index - 2):
                if board[index - 1] == "" and board[index - 2] == "" and board[index - 3] == "":
                    activate_square(index - 2)
            if not King.blackrookkingside and not King.isattacked(index) and not King.isattacked(index + 1) and not \
                    King.isattacked(index + 2):
                if board[index + 1] == "" and board[index + 2] == "":
                    activate_square(index + 2)
        if not tursvart and not King.whitekingmoved:
            if not King.whiterookqueenside and not King.isattacked(index) and not King.isattacked(index - 1) and not \
                    King.isattacked(index - 2):
                if board[index - 1] == "" and board[index - 2] == "" and board[index - 3] == "":
                    activate_square(index - 2)
            if not King.whiterookkingside and not King.isattacked(index) and not King.isattacked(index + 1) and not \
                    King.isattacked(index + 2):
                if board[index + 1] == "" and board[index + 2] == "":
                    activate_square(index + 2)


class GameStat:
    piecename = ""
    kill = False
    piecepos = 64
    oldpospiece = 64
    repr = ""
    specialmove = ""

    @staticmethod
    def getfen():
        kopia = board.copy()
        kopia.append("end")
        eachrow = []
        for i in range(8):
            eachrow.append(kopia[i * 8:(i + 1) * 8])
        for d in range(len(eachrow)):
            cout = 0
            for i in range(len(eachrow[d])):
                if eachrow[d][i] == "":
                    cout += 1
                    if i + 1 == len(eachrow[d]):
                        for b in range(cout):
                            eachrow[d][i - b] = ""
                            if b + 1 == cout:
                                eachrow[d][i - b] = str(cout)
                else:
                    for e in range(cout):
                        eachrow[d][i - (e + 1)] = ""
                        if e == 0:
                            eachrow[d][i - (e + 1)] = str(cout)
                    cout = 0
            eachrow[d] = "".join(eachrow[d])
            # if d + 1 == len(eachrow):
            #    eachrow[d] = eachrow[d][:-1]
            # logger.debug(eachrow[d])
        if tursvart:
            turn = "b"
        else:
            turn = "w"
        if not King.whitekingmoved:
            if not King.whiterookkingside:
                wkingside = "K"
            else:
                wkingside = ""
            if not King.whiterookqueenside:
                wqueenside = "Q"
            else:
                wqueenside = ""
        else:
            wqueenside = ""
            wkingside = ""
        if not King.blackkingmoved:
            if not King.blackrookkingside:
                bkingside = "k"
            else:
                bkingside = ""
            if not King.blackrookqueenside:
                bqueenside = "q"
            else:
                bqueenside = ""
        else:
            bqueenside = ""
            bkingside = ""
        if bkingside == bqueenside == wqueenside == wkingside == "":
            castletext = "-"
        else:
            castletext = f"{wkingside}{wqueenside}{bkingside}{bqueenside}"
        if Enpassent.index == 64:
            enpassenttxt = "-"
        else:
            enpassenttxt = f"{AtoH[Enpassent.index % 8].lower()}{str(8 - (Enpassent.index // 8))}"
        fiftymoveruletxt = str(Draw.ruylopeznum)
        fullmove = str(countmoves + 1)
        thewholefen = (f"{eachrow[0]}/{eachrow[1]}/{eachrow[2]}/{eachrow[3]}/"
                       f"{eachrow[4]}/{eachrow[5]}/{eachrow[6]}/{eachrow[7]} {turn} {castletext}"
                       f" {enpassenttxt} {fiftymoveruletxt} {fullmove}")
        # logger.debug(thewholefen)
        return thewholefen

    @staticmethod
    def coveredbyknight(gotosqr, exception):
        out = []
        saverow = ""
        savecol = ""
        global tursvart
        night = "N"
        if tursvart:
            night = night.lower()
        elif not tursvart:
            night = night.upper()
        nrightup = gotosqr - 6
        nrightdown = gotosqr + 10
        nleftup = gotosqr - 10
        nleftdown = gotosqr + 6
        ntopright = gotosqr - 15
        ntopleft = gotosqr - 17
        nbottomright = gotosqr + 17
        nbottomleft = gotosqr + 15
        if gotosqr // 8 + 1 != 1 and gotosqr // 8 + 1 != 2 and gotosqr % 8 != 7:
            if board[ntopright] == night and not King.causecheck(gotosqr, ntopright) and ntopright != exception:
                # print(ntopright, "ntopright", board[ntopright])
                out.append(ntopright)
            # print(topright)
        if gotosqr // 8 + 1 != 1 and gotosqr // 8 + 1 != 2 and gotosqr % 8 != 0:
            if board[ntopleft] == night and not King.causecheck(gotosqr, ntopleft) and ntopleft != exception:
                # print(ntopleft, "ntopleft", board[ntopleft])
                out.append(ntopleft)
            # print(topleft)
        if gotosqr // 8 + 1 != 7 and gotosqr // 8 + 1 != 8 and gotosqr % 8 != 7:
            if board[nbottomright] == night and not King.causecheck(gotosqr,
                                                                    nbottomright) and nbottomright != exception:
                # print(nbottomright, "nbottomright", board[nbottomright])
                out.append(nbottomright)
            # print(bottomright)
        if gotosqr // 8 + 1 != 7 and gotosqr // 8 + 1 != 8 and gotosqr % 8 != 0:
            if board[nbottomleft] == night and not King.causecheck(gotosqr, nbottomleft) and nbottomleft != exception:
                # print(nbottomleft, "nbottomleft", board[nbottomleft])
                out.append(nbottomleft)
            # print(bottomleft)
        if gotosqr % 8 != 6 and gotosqr % 8 != 7 and gotosqr // 8 + 1 != 1:
            if board[nrightup] == night and not King.causecheck(gotosqr, nrightup) and nrightup != exception:
                # print(nrightup, "nrightup", board[nrightup])
                out.append(nrightup)
            # print(rightup)
        if gotosqr % 8 != 6 and gotosqr % 8 != 7 and gotosqr // 8 + 1 != 8:
            if board[nrightdown] == night and not King.causecheck(gotosqr, nrightdown) and nrightdown != exception:
                # print(nrightdown, "nrightdown", board[nrightdown])
                out.append(nrightdown)
            # print(rightdown)
        if gotosqr % 8 != 0 and gotosqr % 8 != 1 and gotosqr // 8 + 1 != 1:
            if board[nleftup] == night and not King.causecheck(gotosqr, nleftup) and nleftup != exception:
                # print(nleftup, "nleftup", board[nleftup])
                out.append(nleftup)
            # print(leftup)
        if gotosqr % 8 != 0 and gotosqr % 8 != 1 and gotosqr // 8 + 1 != 8:
            if board[nleftdown] == night and not King.causecheck(gotosqr, nleftdown) and nleftdown != exception:
                # print(nleftdown, "nleftdown", board[nleftdown])
                out.append(nleftdown)
            # print(leftdown)
        if len(out) == 0:
            out = ""
        else:
            for i in range(len(out)):
                if out[i] % 8 == exception % 8:
                    saverow = (exception // 8) + 1
                if out[i] // 8 == exception // 8:
                    savecol = AtoH[exception % 8].lower()
            if saverow != "" and savecol != "":
                out = str(savecol + str(saverow))
            elif savecol == "" and saverow != "":
                out = str(saverow)
            else:
                out = str(AtoH[exception % 8].lower())
        return out

    @staticmethod
    def coveredbyrook(index, exception):
        out = []
        rookie = "R"
        if tursvart:
            rookie = rookie.lower()
        elif not tursvart:
            rookie = rookie.upper()

        def right(step):
            right = index + step
            return right

        def up(step):
            up = index - (step * 8)
            return up

        def down(step):
            down = index + (step * 8)
            return down

        def left(step):
            left = index - step
            return left

        if index % 8 != 0:
            steg = 1
            while index // 8 == left(steg) // 8 and board[left(steg)] == "":
                steg += 1
            if left(steg) // 8 != index // 8:
                pass
            elif board[left(steg)] == rookie and not King.causecheck(index, left(steg)) and left(steg) != exception:
                # print(left(steg), "left", steg, board[left(steg)])
                out.append(left(steg))
        if index % 8 != 7:
            steg = 1
            while index // 8 == right(steg) // 8 and board[right(steg)] == "":
                steg += 1
            if right(steg) // 8 != index // 8:
                pass
            elif board[right(steg)] == rookie and not King.causecheck(index, right(steg)) and right(steg) != exception:
                # print(right(steg), "right", steg, board[right(steg)])
                out.append(right(steg))
        if index // 8 + 1 != 1:
            steg = 1
            while up(steg) >= 0 and board[up(steg)] == "":
                steg += 1
            if up(steg) < 0:
                pass
            elif board[up(steg)] == rookie and not King.causecheck(index, up(steg)) and up(steg) != exception:
                # print(up(steg), "up", steg, board[up(steg)])
                out.append(up(steg))
        if index // 8 + 1 != 8:
            steg = 1
            while down(steg) <= 63 and board[down(steg)] == "":
                steg += 1
            if down(steg) > 63:
                pass
            elif board[down(steg)] == rookie and not King.causecheck(index, down(steg)) and down(steg) != exception:
                # print(down(steg), "down", steg, board[down(steg)])
                out.append(down(steg))
        if len(out) == 0:
            out = ""
        else:
            saverow = ""
            savecol = ""
            for i in out:
                if i % 8 == exception % 8:
                    saverow = (exception // 8) + 1
                if i // 8 == exception // 8:
                    savecol = AtoH[exception % 8].lower()
            if saverow != "" and savecol != "":
                out = str(savecol + str(saverow))
            elif savecol == "" and saverow != "":
                out = str(saverow)
            else:
                out = str(AtoH[exception % 8].lower())
        return out

    @staticmethod
    def coveredbyq(index, exception):
        out = []
        dam = "Q"
        if tursvart:
            dam = dam.lower()
        elif not tursvart:
            dam = dam.upper()

        def right(step):
            right = index + step
            return right

        def up(step):
            up = index - (step * 8)
            return up

        def down(step):
            down = index + (step * 8)
            return down

        def left(step):
            left = index - step
            return left

        def leftup(step):
            value = index - (step * 9)
            return value

        def leftdown(step):
            value = index + (step * 7)
            return value

        def rightup(step):
            value = index - (step * 7)
            return value

        def rightdown(step):
            value = index + (step * 9)
            return value

        if index % 8 != 0:
            steg = 1
            while index // 8 == left(steg) // 8 and board[left(steg)] == "":
                steg += 1
            if left(steg) // 8 != index // 8:
                pass
            elif is_enemy(left(steg)):
                pass
            elif board[left(steg)] == dam and not King.causecheck(index, left(steg)) and left(steg) != exception:
                # print(left(steg), "left", steg, board[left(steg)])
                out.append(left(steg))
        if index % 8 != 7:
            steg = 1
            while index // 8 == right(steg) // 8 and board[right(steg)] == "":
                steg += 1
            if right(steg) // 8 != index // 8:
                pass
            elif is_enemy(right(steg)):
                pass
            elif board[right(steg)] == dam and not King.causecheck(index, right(steg)) and right(steg) != exception:
                # print(right(steg), "right", steg, board[right(steg)])
                out.append(right(steg))
        if index // 8 + 1 != 1:
            steg = 1
            while up(steg) >= 0 and board[up(steg)] == "":
                steg += 1
            if up(steg) < 0:
                pass
            elif is_enemy(up(steg)):
                pass
            elif board[up(steg)] == dam and not King.causecheck(index, up(steg)) and up(steg) != exception:
                # print(up(steg), "up", steg, board[up(steg)])
                out.append(up(steg))
        if index // 8 + 1 != 8:
            steg = 1
            while down(steg) <= 63 and board[down(steg)] == "":
                steg += 1
            if down(steg) > 63:
                pass
            elif is_enemy(down(steg)):
                pass
            elif board[down(steg)] == dam and not King.causecheck(index, down(steg)) and down(steg) != exception:
                # print(down(steg), "down", steg, board[down(steg)])
                out.append(down(steg))
        if index // 8 != 0 and index % 8 != 0:
            step = 1
            endpoint = False
            while leftup(step) >= 0 and not endpoint and board[leftup(step)] == "":
                if leftup(step) % 8 == 0 or leftup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if board[leftup(step)] == dam and not King.causecheck(index, leftup(step)) and leftup(step) != exception:
                # print(leftup(step), "leftup", step, board[leftup(step)])
                out.append(leftup(step))
        if index // 8 != 0 and index % 8 != 7:
            step = 1
            endpoint = False
            while not endpoint and board[rightup(step)] == "":
                if rightup(step) % 8 == 7 or rightup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if is_enemy(rightup(step)):
                pass
            elif board[rightup(step)] == dam and not King.causecheck(index, rightup(step)) \
                    and rightup(step) != exception:
                # print(rightup(step), "rightup", step, board[rightup(step)])
                out.append(rightup(step))
        if index // 8 != 7 and index % 8 != 0:
            step = 1
            endpoint = False
            while not endpoint and board[leftdown(step)] == "":
                if leftdown(step) % 8 == 0 or leftdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if is_enemy(leftdown(step)):
                pass
            elif board[leftdown(step)] == dam and not King.causecheck(index, leftdown(step)) \
                    and leftdown(step) != exception:
                # print(leftdown(step), "leftdown", step, board[leftdown(step)])
                out.append(leftdown(step))
        if index // 8 != 7 and index % 8 != 7:
            step = 1
            endpoint = False
            while not endpoint and board[rightdown(step)] == "":
                if rightdown(step) % 8 == 7 or rightdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if is_enemy(rightdown(step)):
                pass
            elif board[rightdown(step)] == dam and not King.causecheck(index, rightdown(step)) \
                    and rightdown(step) != exception:
                # print(rightdown(step), "rightdown", step, board[rightdown(step)])
                out.append(rightdown(step))
        if len(out) == 0:
            out = ""
        else:
            saverow = ""
            savecol = ""
            for i in range(len(out)):
                if out[i] % 8 == exception % 8:
                    saverow = (exception // 8) + 1
                if out[i] // 8 == exception // 8:
                    savecol = AtoH[exception % 8].lower()
            if saverow != "" and savecol != "":
                out = str(savecol + str(saverow))
            elif savecol == "" and saverow != "":
                out = str(saverow)
            else:
                out = str(AtoH[exception % 8].lower())
        return out

    @staticmethod
    def bishopcover(index, exception):
        out = []
        saverow = ""
        savecol = ""
        global tursvart
        bee = "B"
        if tursvart:
            bee = bee.lower()
        elif not tursvart:
            bee = bee.upper()
        leftup = lambda x: index - (x * 9)
        leftdown = lambda step: index + (step * 7)
        rightup = lambda step: index - (step * 7)
        rightdown = lambda step: index + (step * 9)
        if index // 8 != 0 and index % 8 != 0:
            step = 1
            endpoint = False
            while leftup(step) >= 0 and not endpoint and board[leftup(step)] == "":
                if leftup(step) % 8 == 0 or leftup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if board[leftup(step)] == bee and not King.causecheck(index, leftup(step)) and leftup(step) != exception:
                # print(leftup(step), "leftup", step, board[leftup(step)])
                out.append(leftup(step))
        if index // 8 != 0 and index % 8 != 7:
            step = 1
            endpoint = False
            while not endpoint and board[rightup(step)] == "":
                if rightup(step) % 8 == 7 or rightup(step) // 8 == 0:
                    endpoint = True
                else:
                    step += 1
            if board[rightup(step)] == bee and not King.causecheck(index, rightup(step)) \
                    and rightup(step) != exception:
                # print(rightup(step), "rightup", step, board[rightup(step)])
                out.append(rightup(step))
        if index // 8 != 7 and index % 8 != 0:
            step = 1
            endpoint = False
            while not endpoint and board[leftdown(step)] == "":
                if leftdown(step) % 8 == 0 or leftdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if board[leftdown(step)] == bee and not King.causecheck(index, leftdown(step)) \
                    and leftdown(step) != exception:
                # print(leftdown(step), "leftdown", step, board[leftdown(step)])
                out.append(leftdown(step))
        if index // 8 != 7 and index % 8 != 7:
            step = 1
            endpoint = False
            while not endpoint and board[rightdown(step)] == "":
                if rightdown(step) % 8 == 7 or rightdown(step) // 8 == 7:
                    endpoint = True
                else:
                    step += 1
            if board[rightdown(step)] == bee and not King.causecheck(index, rightdown(step)) \
                    and rightdown(step) != exception:
                # print(rightdown(step), "rightdown", step, board[rightdown(step)])
                out.append(rightdown(step))
        if len(out) == 0:
            out = ""
        else:
            for i in range(len(out)):
                if out[i] % 8 == exception % 8:
                    saverow = (exception // 8) + 1
                if out[i] // 8 == exception // 8:
                    savecol = AtoH[exception % 8].lower()
            if saverow != "" and savecol != "":
                out = str(savecol + str(saverow))
            elif savecol == "" and saverow != "":
                out = str(saverow)
            else:
                out = str(AtoH[exception % 8].lower())
        return out

    @classmethod
    def posrepr(cls):
        if cls.piecename == "":
            # Couldn't fetch piece-name earlier
            print("Couldn't fetch piece-name earlier")
            pass
        elif cls.piecename == "P":
            # Only in need of column-letter
            if cls.kill:
                cls.repr = AtoH[cls.oldpospiece % 8].lower()
            else:
                cls.repr = ""
        elif cls.piecename == "N":
            # Now we check which knight can go to the position that we are moving the knight to.
            # Copying the knight parts of the isprotected-function
            # And it should return its column or row number or both
            # Depending on how many same colored knights can go to that specific square
            cls.repr = GameStat.coveredbyknight(cls.piecepos, cls.oldpospiece)
        elif cls.piecename == "B":
            # Same proc but with bishop
            cls.repr = GameStat.bishopcover(cls.piecepos, cls.oldpospiece)
        elif cls.piecename == "R":
            # Same proc but with rook
            cls.repr = GameStat.coveredbyrook(cls.piecepos, cls.oldpospiece)
        elif cls.piecename == "Q":
            # Same proc but with rook
            cls.repr = GameStat.coveredbyq(cls.piecepos, cls.oldpospiece)
        elif cls.piecename == "K":
            cls.repr = ""
        else:
            print("Internal Error")

    @classmethod
    def resetdata(cls):
        cls.piecename = ""
        cls.kill = False
        cls.piecepos = 64
        cls.oldpospiece = 64
        cls.repr = ""
        cls.specialmove = ""

    @classmethod
    def fetchdata(cls, index, oldpos):
        cls.oldpospiece = oldpos
        cls.piecepos = index
        cls.piecename = board[index]
        cls.piecename = cls.piecename.upper()

    @classmethod
    def kingsidecastle(cls):
        cls.specialmove = "O-O"

    @classmethod
    def queensidecastle(cls):
        cls.specialmove = "O-O-O"

    @classmethod
    def promotion(cls):
        position = AtoH[cls.piecepos % 8].lower() + str(cls.piecepos + 1 // 8)
        cls.specialmove = position + "= Q, R, N, B"

    @staticmethod
    def print():
        kill = ""
        positio = AtoH[GameStat.piecepos % 8].lower() + str(8 - (GameStat.piecepos // 8))
        piecename = GameStat.piecename
        if piecename == "P":
            piecename = ""
        if GameStat.kill:
            kill = "x"
        if GameStat.specialmove == "":
            return f"{piecename}{GameStat.repr}{kill}{positio}"
        else:
            return "{}{}".format(kill, GameStat.specialmove)

    @classmethod
    def killed(cls):
        cls.kill = True


class Draw:
    gameplay = []
    ruylopeznum = 0

    @staticmethod
    def stalemate():
        global stoppedwhite
        global stoppedblack
        global draw
        k = "k"
        if tursvart:
            k = k.lower()
        elif not tursvart:
            k = k.upper()
        if King.cantgoanywhere(board.index(k)) and not King.isattacked(board.index(k)):
            draw = True
            for i in range(len(board)):
                if board[i] == "" or is_enemy(i):
                    if King.isprotected(i):
                        draw = False
            if draw:
                blackmailer.config(bg="red")
                whitewater.config(bg="red")
                stoppedwhite = True
                stoppedblack = True
                for i in range(len(buttons)):
                    buttons[i].config(state=DISABLED)

    @staticmethod
    def bymaterial():
        global stoppedwhite
        global stoppedblack
        global draw
        countpawnsb = board.count("p")
        countpawnsw = board.count("P")
        if not draw:
            if countpawnsb == 0 and countpawnsw == 0:
                # print("0 pawns on the board")
                if board.count("Q") == 0 and board.count("q") == 0:
                    # print("0 queens on the board")
                    if board.count("R") == 0 and board.count("r") == 0:
                        # print("0 rooks on the board")
                        if board.count("B") <= 1 and board.count("b") <= 1:
                            # print("0 Bishops on the board")
                            if board.count("N") <= 2 and board.count("n") <= 2:
                                # print("less than 3 knights on the board")
                                if board.count("N") >= 1 and board.count("B") == 1:
                                    pass
                                elif board.count("n") >= 1 and board.count("b") == 1:
                                    pass
                                else:
                                    draw = True
                                    stoppedblack = True
                                    stoppedblack = True

    @classmethod
    def repetition(cls):
        global draw
        global stoppedwhite
        global stoppedblack
        drawcounter = 0
        cls.gameplay.append(board.copy())
        if not draw:
            for i in range(len(cls.gameplay)):
                for j in range(len(cls.gameplay)):
                    if i != j and cls.gameplay[i] == cls.gameplay[j]:
                        drawcounter += 1
                if drawcounter >= 2:
                    draw = True
                    stoppedblack = True
                    stoppedwhite = True
                    print("Draw by repetition")
                else:
                    drawcounter = 0

    @classmethod
    def resetgame(cls):
        cls.gameplay = []
        cls.ruylopeznum = 0

    @classmethod
    def addonetoruy(cls):
        cls.ruylopeznum += 1

    @classmethod
    def ruylopezrulecheck(cls):
        global draw
        global stoppedblack
        global stoppedwhite
        if not draw:
            if cls.ruylopeznum == 100:
                draw = True
                stoppedwhite = True
                stoppedblack = True

    @classmethod
    def resetruyl(cls):
        cls.ruylopeznum = 0

    @classmethod
    def insruynum(cls, num):
        cls.ruylopeznum = num


def board_to_button():
    global board
    global buttons
    for i in range(64):
        if board[i] == "":
            buttons[i].config(image=clearer)
        if board[i] == "R":
            buttons[i].config(image=R)
        if board[i] == "r":
            buttons[i].config(image=r)
        if board[i] == "B":
            buttons[i].config(image=B)
        if board[i] == "b":
            buttons[i].config(image=b)
        if board[i] == "N":
            buttons[i].config(image=N)
        if board[i] == "n":
            buttons[i].config(image=n)
        if board[i] == "Q":
            buttons[i].config(image=Q)
        if board[i] == "q":
            buttons[i].config(image=q)
        if board[i] == "K":
            buttons[i].config(image=K)
        if board[i] == "k":
            buttons[i].config(image=k)
        if board[i] == "P":
            buttons[i].config(image=P)
        if board[i] == "p":
            buttons[i].config(image=p)


tursvart = False
positiones = 0
countmoves = 0
brada = board
blacksecond = float
whitesecond = float
goaltimeblack = float
goaltimewhite = float
stoppedblack = True
stoppedwhite = True
savewhitesmove = str


def blackupd():
    global goaltimeblack
    global blacksecond
    if not stoppedblack and blacksecond > 0.01:
        blacksecond = goaltimeblack
        blacksecond = blacksecond - time.time()
        minuter = ((blacksecond // 60) % 60)
        timmar = (blacksecond // 3600)
        sek = blacksecond % 60
        if blacksecond < 10:
            hundradelar = ((blacksecond * 100) % 100)
            alltihop = str("{:02d}:{:02d}:{:02d}.{:02d}".format(int(timmar), int(minuter), int(sek), int(hundradelar)))
        else:
            alltihop = str("{:02d}:{:02d}:{:02d}".format(int(timmar), int(minuter), int(sek)))
        blackmailer.config(text=alltihop, bg='#00f97c')
        window.after(7, blackupd)
    elif not stoppedblack:
        for i in range(len(buttons)):
            buttons[i].config(state=DISABLED)
        blackmailer.config(bg="red")
        window.after(50, blackupd)


def whiteupd():
    global goaltimewhite
    global whitesecond
    if not stoppedwhite and whitesecond > 0.01:
        whitesecond = goaltimewhite
        whitesecond = whitesecond - time.time()
        minuter = ((whitesecond // 60) % 60)
        timmar = (whitesecond // 3600)
        sek = whitesecond % 60
        if whitesecond < 10:
            hundradelar = ((whitesecond * 100) % 100)
            alltihop = str("{:02d}:{:02d}:{:02d}.{:02d}".format(int(timmar), int(minuter), int(sek), int(hundradelar)))
        else:
            alltihop = str("{:02d}:{:02d}:{:02d}".format(int(timmar), int(minuter), int(sek)))
        whitewater.config(text=alltihop, bg='#00f97c')
        window.after(7, whiteupd)
    elif not stoppedwhite:
        for i in range(len(buttons)):
            buttons[i].config(state=DISABLED)
        whitewater.config(bg="red")
        window.after(50, whiteupd)


def chessclock():
    global stagemoves
    global stagetime
    global tidsekunder
    global incrementime
    global blacksecond
    global whitesecond
    global goaltimewhite
    global goaltimeblack
    global stoppedwhite
    global stoppedblack
    if usingtimer:
        # print(countmoves)
        if countmoves == 0:
            blacksecond = int(tidsekunder)
            whitesecond = int(tidsekunder)
        if tursvart:
            stoppedblack = False
            stoppedwhite = True
            if len(stagemoves) == 0:
                goaltimeblack = blacksecond + time.time() + int(incrementime)
                blacksecond = time.time() + blacksecond
            else:
                goaltimeblack = blacksecond + time.time() + int(incrementime)
                blacksecond = time.time() + blacksecond
                for i in range(len(stagemoves)):
                    if countmoves == stagemoves[i]:
                        goaltimeblack = goaltimeblack + int(stagetime[i])
            blackupd()
        elif not tursvart:
            stoppedblack = True
            stoppedwhite = False
            if len(stagemoves) == 0:
                goaltimewhite = whitesecond + time.time() + int(incrementime)
                whitesecond = time.time() + whitesecond
            else:
                goaltimewhite = whitesecond + time.time() + int(incrementime)
                whitesecond = time.time() + whitesecond
                for i in range(len(stagemoves)):
                    if countmoves == stagemoves[i]:
                        goaltimewhite = goaltimewhite + int(stagetime[i])
            whiteupd()


def clicked(index):
    global buttons
    global board
    global positiones
    global tursvart
    global brada
    global countmoves
    global looking
    global savewhitesmove
    p = "P"
    b = "B"
    n = "N"
    r = "R"
    q = "Q"
    k = "K"
    if tursvart:
        p = p.lower()
        b = b.lower()
        n = n.lower()
        r = r.lower()
        q = q.lower()
        k = k.lower()
    elif not tursvart:
        p = p.title()
        b = b.title()
        n = n.title()
        r = r.title()
        q = q.title()
        k = k.title()
    # print(AtoH[index%8], 8 - index//8)
    brada = board.copy()
    if board[index] == "" or tursvart and board[index].isupper() or not tursvart and board[index].islower():
        Draw.addonetoruy()
        if positiones == 64:
            logger.error("System got invalid call")
            return
        if (tursvart and board[index].isupper() or not tursvart and board[index].islower()) and positiones != 64:
            GameStat.killed()
            Draw.resetruyl()
        if positiones != 64:
            board[index] = board[positiones]
            GameStat.fetchdata(index, positiones)
        # print(board[positiones])
        # checks if kings have moved this move to check castling rights
        # It does the move to if it is called any time
        if board[index] == k and (not King.blackkingmoved or not King.whitekingmoved) and positiones != 64:
            if index + 2 == positiones:
                board[positiones - 1] = board[positiones - 4]
                board[positiones - 4] = ""
                GameStat.queensidecastle()
            if index - 2 == positiones:
                board[index - 1] = board[index + 1]
                board[index + 1] = ""
                GameStat.kingsidecastle()
            King.hasmoved()
        # promotion checking and enpassent check (AKA checking all special things the pawn can do)
        if positiones != 64 and board[positiones] == p:
            Draw.resetruyl()
            if index // 8 + 1 == 8 or index // 8 + 1 == 1:
                Promotion.white(index)
                Promotion.promotion(index)
                GameStat.promotion()
            # checking if two-step move were made
            if not tursvart and positiones - 16 == index or tursvart and positiones + 16 == index:
                Enpassent.twostep(index)
            # checking if enpassent move were called
            if index == Enpassent.index:
                GameStat.killed()
                if tursvart:
                    board[index - 8] = ""
                elif not tursvart:
                    board[index + 8] = ""
        if positiones != 64:
            board[positiones] = ""
        # checks if the move causes check and disables the move instantly
        # and waits for the player to input new move or time ends
        if not King.isattacked(board.index(k)) and positiones != 64:
            GameStat.posrepr()
            # re-setting variable so you cant do enpassent move after one move
            if Enpassent.index // 8 == 2 and not tursvart or Enpassent.index // 8 == 5 and tursvart:
                Enpassent.resetvar()
            # checks if the rooks have moved from their position during move
            King.checkrooks()
            board_to_button()
            positiones = 64
            if tursvart:
                countmoves += 1
            tursvart = not tursvart
            chessclock()
            Draw.stalemate()
            Draw.repetition()
            Draw.bymaterial()
            Draw.ruylopezrulecheck()
            King.losscheck()
            kung = "k"
            if tursvart:
                kung = kung.lower()
                movenum = f"{str(countmoves + 1)}."
                textar = f"{movenum} {GameStat.print()}"
                if King.isattacked(board.index(kung)):
                    textar = f"{movenum} {GameStat.print()}+"
                if loss:
                    textar = f"{movenum} {GameStat.print()}#"
                    game_log.info(textar)
                savewhitesmove = textar
                # print(textar, end=" ")
            elif not tursvart:
                kung = kung.upper()
                textar = f"{GameStat.print()}"
                if King.isattacked(board.index(kung)):
                    textar = f"{GameStat.print()}+"
                if loss:
                    textar = f"{GameStat.print()}#"
                logtxt = f"{savewhitesmove} {textar}"
                game_log.info(logtxt)
                # print(textar, end=" ")
            save_game.append(board.copy())
            looking = len(save_game)
            GameStat.resetdata()
            if not loss and not draw:
                start_mode()
            elif draw:
                # print("½-½")
                game_log.info("½-½")
            else:
                if tursvart:
                    # print("1-0")
                    game_log.info("1-0")
                elif not tursvart:
                    # print("0-1")
                    game_log.info("0-1")
        elif King.isattacked(board.index(k)):
            board = brada.copy()
            GameStat.resetdata()
            start_mode()
            print("kings in check")
    elif board[index] == k:
        King.activate(index)
        # print("king")
        positiones = index
    elif board[index] == p:
        if not tursvart:
            WPawn.activate(index)
        elif tursvart:
            Bpawn.activate(index)
        positiones = index
        # print("pawn")
    elif board[index] == n:
        Knight.activate(index)
        # print("knight")
        positiones = index
    elif board[index] == r:
        Rook.activate(index)
        # print("rook")
        positiones = index
    elif board[index] == b:
        Bishop.activate(index)
        # print("bishop")
        positiones = index
    elif board[index] == q:
        Queen.activate(index)
        # print("queen")
        positiones = index


for i in range(8):
    Label(window, text=str(8 - i), font=("shonarbangla", 20)).grid(row=i + 2, column=0)
for i in range(8):
    Label(window, text=AtoH[i], font=("shonarbangla", 20)).grid(row=1, column=i + 1)
for i in range(64):
    buttons.append(Button(window, image=clearer, command=lambda index=i: clicked(index)))
    buttons[i].grid(row=(i // 8) + 2, column=(i % 8) + 1)
    if board[i] == "":
        buttons[i].config(state=DISABLED)
    if (i // 8) % 2 == 0 and (i % 8) % 2 == 0 or (i // 8) % 2 == 1 and (i % 8) % 2 == 1:
        buttons[i].config(background="white")
    else:
        buttons[i].config(background="light green")
countcalls = int(0)
tidsekunder = float
incrementime = float
moveamouns = 0
stagetime = []
stagemoves = []
usingtimer = False


def newwindow():
    timewindow = Toplevel()
    timewindow.attributes('-topmost', True)

    def finish():
        global incrementime
        global tidsekunder
        global usingtimer
        global blackmailer
        global whitewater
        usingtimer = True
        # print("finsihed")
        if countcalls == 0:
            if hours.get() == "":
                h = 0
            else:
                h = int(hours.get())
            if minutes.get() == "":
                minns = 0
            elif int(minutes.get()) > 59:
                minns = 59
            else:
                minns = int(minutes.get())
            if sekonds.get() == "":
                sekunders = 0
            elif int(sekonds.get()) > 59:
                sekunders = 59
            else:
                sekunders = int(sekonds.get())
            tidsekunder = sekunders + minns * 60 + h * 3600
        if tidsekunder <= 0:
            usingtimer = False
        else:
            sekunder = int(tidsekunder % 60)
            minuters = int(tidsekunder // 60 % 60)
            timme = int(tidsekunder // 3600)
            alltihop = str("{:02d}:{:02d}:{:02d}".format(timme, minuters, sekunder))
            blackmailer.config(font=("impact", 16), width=12, height=1, bg='#00f97c', fg='black', text=alltihop)
            whitewater.config(font=("impact", 16), width=12, height=1, bg='#00f97c', fg='black', text=alltihop)
            blackmailer.grid(row=2, columnspan=2, column=9)
            whitewater.grid(row=9, columnspan=2, column=9)
        if increment.get() == "":
            incrementime = 0
        else:
            incrementime = float(increment.get())
        timewindow.destroy()
        print(tidsekunder, "|", incrementime, stagetime, stagemoves)

    def addtime():
        global countcalls
        global tidsekunder
        global moveamouns
        global stagetime
        global stagemoves
        global usingtimer
        usingtimer = True
        try:
            if hours.get() == "":
                h = 0
            else:
                h = int(hours.get())
            if minutes.get() == "":
                minns = 0
            elif int(minutes.get()) > 59:
                minns = 59
            else:
                minns = int(minutes.get())
            if sekonds.get() == "":
                sekunders = 0
            elif int(sekonds.get()) > 59:
                sekunders = 59
            else:
                sekunders = int(sekonds.get())
            if countcalls < 1:
                tidsekunder = sekunders + minns * 60 + h * 3600
                if int(tidsekunder) <= 0:
                    if tidsekunder <= 0:
                        usingtimer = False
                    timewindow.destroy()
            countcalls += 1
            # print("adding time")
            if countcalls >= 1:
                moveamount.grid()
                movetxt.grid()
            if countcalls > 1:
                if moveamount.get() == "":
                    errtxt = Label(timewindow, font=("Dubai", 16), text="enter number of moves please")
                    errtxt.grid(row=3, column=3)
                    timewindow.update()
                    time.sleep(1)
                    errtxt.grid_remove()
                elif int(moveamount.get()) <= moveamouns:
                    errtxt = Label(timewindow, font=("Dubai", 16), text="enter number of moves higher than the last one"
                                                                        " please")
                    errtxt.grid(row=3, column=3)
                    timewindow.update()
                    time.sleep(1)
                    errtxt.grid_remove()
                else:
                    oldmoveamouns = moveamouns
                    moveamouns = int(moveamount.get())
                    stagetime.append(sekunders + minns * 60 + h * 3600)
                    errtxt = Label(timewindow, font=("Dubai", 16), text="")
                    if stagetime[len(stagetime) - 1] > 0:
                        stagemoves.append(moveamouns)
                    else:
                        moveamouns = oldmoveamouns
                        errtxt.config(font=("Dubai", 16), text="enter time")
                    errtxt.grid(row=3, column=3)
                    timewindow.update()
                    time.sleep(1)
                    errtxt.grid_remove()
            moveamount.delete(0, END)
            hours.delete(0, END)
            minutes.delete(0, END)
            sekonds.delete(0, END)
        except:
            print("write right")

    def callback(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    vcmd = (timewindow.register(callback))
    submit = Button(timewindow, font=("shonarbangla", 16), text="Finished", command=finish, bg='#00ff80')
    addtimeorstage = Button(timewindow, font=("shonarbangla", 16), text="Add time", command=addtime, bg='#00ff80')
    increment = Entry(timewindow, font=("Britannic Bold", 12), width=5, validate="key", validatecommand=(vcmd, '%P'),
                      justify=CENTER)
    hours = Entry(timewindow, font=("Britannic Bold", 12), width=5, justify=CENTER, validate="key",
                  validatecommand=(vcmd, '%P'))
    minutes = Entry(timewindow, font=("Britannic Bold", 12), width=5, justify=CENTER, validate="key",
                    validatecommand=(vcmd, '%P'))
    sekonds = Entry(timewindow, font=("Britannic Bold", 12), width=5, justify=CENTER, validate="key",
                    validatecommand=(vcmd, '%P'))
    movetxt = Label(timewindow, font=("shonarbangla", 16), text="Moves", bg='#fcc710')
    movetxt.grid(row=3, column=0)
    moveamount = Entry(timewindow, font=("Britannic Bold", 12), width=5, justify=CENTER, validate="key",
                       validatecommand=(vcmd, '%P'))
    moveamount.grid(row=3, column=2)
    hours.grid(row=2, column=2)
    minutes.grid(row=2, column=3, padx=10)
    sekonds.grid(row=2, column=4)
    submit.grid(row=4, columnspan=2, column=2)
    movetxt.grid_remove()
    moveamount.grid_remove()
    Label(timewindow, text=":", font=("cooper black", 12)).grid(columnspan=2, column=2, row=2)
    Label(timewindow, text=":", font=("cooper black", 12)).grid(columnspan=2, column=3, row=2)
    addtimeorstage.grid(row=2, columnspan=2, column=0)
    Label(timewindow, font=("shonarbangla", 16), text="increment", bg='#ff80c0').grid(column=0, columnspan=2, row=1)
    increment.grid(row=1, column=3)


setuptime = Button(window, text="Setup time", font=("shonarbangla", 16), command=newwindow)
setuptime.grid(row=5, column=9, columnspan=2)


def fen_data_get():
    copywind = Toplevel()
    copywind.attributes('-topmost', True)

    def copyfen():
        # logger.debug("Copying FEN")
        pyperclip.copy(GameStat.getfen())
        spam = pyperclip.paste()

    def copypgn():
        # logger.debug("Copying PGN")
        thefiletocopy = open("game.log", "r")
        stringen = thefiletocopy.read()
        pyperclip.copy(stringen)
        spam = pyperclip.paste()
        thefiletocopy.close()
    def pastefen():
        print("gh")

    copyfenn = Button(copywind, text="Copy FEN", font=("shonarbangla", 16), command=copyfen)
    copyfenn.grid()
    copypgnn = Button(copywind, text="Copy PGN", font=("shonarbangla", 16), command=copypgn)
    copypgnn.grid(column=1, row=0)
    pastefen = Button(copywind, text="Import FEN", font=("shonarbangla", 16), command=pastefen)
    pastefen.grid(column=0, row=1, columnspan=2)


copyben = Button(window, text="Info", font=("shonarbangla", 16), command=fen_data_get)
copyben.grid(column=9, columnspan=2, row=6)
copyben.grid_remove()
enter_move = Entry(window, font=("shonarbangla", 12), width=10)


def start():
    global board
    global buttons
    global tursvart
    global countmoves
    global stoppedblack
    global stoppedwhite
    global loss
    global draw
    global save_game
    copyben.grid()
    game_log.info("New Game")
    dlfile = open("game.log", "w")
    dlfile.close()
    save_game = []
    Draw.resetgame()
    draw = False
    loss = False
    stoppedblack = True
    stoppedwhite = True
    countmoves = 0
    tursvart = False
    King.reset()
    setuptime.grid_remove()
    # print("placing pieces")
    board = [
        "r", "n", "b", "q", "k", "b", "n", "r",
        "p", "p", "p", "p", "p", "p", "p", "p",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "P", "P", "P", "P", "P", "P", "P", "P",
        "R", "N", "B", "Q", "K", "B", "N", "R",
    ]
    # print(len(board))
    for i in range(64):
        if board[i] == "":
            buttons[i].config(image=clearer)
        if board[i] == "R":
            buttons[i].config(image=R)
        if board[i] == "r":
            buttons[i].config(image=r)
        if board[i] == "B":
            buttons[i].config(image=B)
        if board[i] == "b":
            buttons[i].config(image=b)
        if board[i] == "N":
            buttons[i].config(image=N)
        if board[i] == "n":
            buttons[i].config(image=n)
        if board[i] == "Q":
            buttons[i].config(image=Q)
        if board[i] == "q":
            buttons[i].config(image=q)
        if board[i] == "K":
            buttons[i].config(image=K)
        if board[i] == "k":
            buttons[i].config(image=k)
        if board[i] == "P":
            buttons[i].config(image=P)
        if board[i] == "p":
            buttons[i].config(image=p)
    for i in range(64):
        if board[i].isupper():
            buttons[i].config(state=ACTIVE)
            window.update()
        else:
            buttons[i].config(state=DISABLED)
            window.update()


startbutton = Button(window, text="START", font=("shonarbangla", 16), command=start).grid(row=4, column=9, columnspan=2)
nextimg = ImageTk.PhotoImage(Image.open("../Rest/ads.png").resize((60, 60)))
prev = Image.open("../Rest/ads.png").resize((60, 60))
prev = ImageOps.mirror(prev)
prev = ImageTk.PhotoImage(prev)


def nextmove():
    global board
    global save_game
    global looking
    if looking < len(save_game):
        looking += 1
        board = save_game[looking - 1].copy()
        board_to_button()
        for i in range(len(buttons)):
            buttons[i].config(state=DISABLED)
        if looking == len(save_game) and not loss and not draw:
            board = save_game[looking - 1].copy()
            board_to_button()
            start_mode()


def prevmove():
    global board
    global save_game
    global looking
    if looking >= 1:
        looking -= 1
        if looking > 0:
            board = save_game[looking - 1].copy()
        else:
            board = starboard
        board_to_button()
        for i in range(len(buttons)):
            buttons[i].config(state=DISABLED)


prevmovebut = Button(window, command=prevmove, image=prev)
prevmovebut.grid(row=1, column=0)
nextmovebut = Button(window, command=nextmove, image=nextimg)
nextmovebut.grid(row=1, column=9, sticky=W)
window.mainloop()


@atexit.register
def goodbye():
    global savewhitesmove
    if tursvart and not draw and not loss:
        game_log.info(savewhitesmove)
    logger.debug("Shutting down")
