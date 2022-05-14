# imports used code built into python
import os
import time
import tkinter
from tkinter import *
import socket
import threading

# makes file with instructions
readme = open("readme.txt", "w")
readme.write("How To Play:\n\n1. use ws to move for\n2. try to get the ball to hit the other players wall")
readme.close()

# imports code not built into python
try:
    from pynput import keyboard
except:
    os.system('pip install pynput')
    from pynput import keyboard


# detects when keys are pressed
def keypress(key):
    global p1

    if str(key) == "'w'":
        if p1 > 0:
            p1 -= 10
    elif str(key) == "'s'":
        if p1 + 300 < 950:
            p1 += 10


# new menu for online
def main2():

    AI.pack_forget()
    Online.pack_forget()
    host.pack(expand=True, fill='both')
    join.pack(expand=True, fill='both')
    Back.pack(expand=True, fill='both')


# return to main menu
def back():

    label.pack_forget()
    text.pack_forget()
    Enter.pack_forget()
    host.pack_forget()
    join.pack_forget()
    score.pack_forget()
    Back.pack_forget()
    AI.pack(expand=True, fill='both')
    Online.pack(expand=True, fill='both')
    s.close()


# loss function
def loss(player):
    global p1score, p2score, p1, p2, ballx, bally, slopex, slopey, score

    if player == 'p1':
        p2score += 1
        Score_Number = "You lost"
    elif player == 'p2':
        p1score += 1
        Score_Number = "You won"

    p1 = 325
    p2 = 325
    ballx = screen_width / 2 - 25
    bally = screen_height / 2 - 25
    slopex = gamespeed
    slopey = 0
    canvas.pack_forget()
    score = Button(window, height=2, width=20, bg='green', text=f"{Score_Number} this round\nYour score: {p1score}\nEnemy score: {p2score}\nClick To Play Again", font=("Times New Roman", 60), command=lambda: main())
    score.pack(expand=True, fill='both')
    Back.pack(expand=True, fill='both')


# main code
def main():
    global p1, p2, bally, ballx, slopey, slopex, itr

    # startup for window
    try:
        score.pack_forget()
    except AttributeError:
        pass
    AI.pack_forget()
    Online.pack_forget()
    Back.pack_forget()
    label.pack_forget()
    canvas.pack()

    # main loop
    while True:

        time.sleep(.001)

        # calculates ball cords
        ballx = ballx - slopex
        bally = bally - slopey

        # loss detection
        if ballx == 0:
            loss('p1')
            return
        if ballx == 1450:
            loss('p2')
            return

        # player collision detection and calculates slope of ball
        if ballx == 100 and p1 - 50 < bally < p1 + 300:
            slopex = -gamespeed
            slopey = ((p1 + 150) - (bally - 25))/25
        if ballx == 1350 and p2 - 50 < bally < p2 + 300:
            slopex = gamespeed
            slopey = ((p2 + 150) - (bally - 25))/25

        # map collision detection
        if bally < 0 or bally > 900:
            slopey = -slopey

        itr += 1
        if itr == difficulty:
            # enemy player ai
            if bally > p2 + 160:
                p2 += 10
            elif bally < p2 + 140:
                p2 -= 10
            itr = 0

        # updates window
        canvas.delete('all')
        canvas.create_rectangle(50, p1, 100, p1 + 300, fill='black')
        canvas.create_rectangle(screen_width - 100, p2, screen_width - 50, p2 + 300, fill='black')
        canvas.create_rectangle(ballx, bally, ballx + 50, bally + 50, fill='red')
        window.update()


def server():

    while True:
        c.send('Thank you for connecting'.encode())


def test():

    while True:
        window.update()


#todo code for hosting server
def server_start():
    global label, c, s

    host.pack_forget()
    join.pack_forget()
    Back.pack_forget()

    s = socket.socket()
    port = 12345
    ip = socket.gethostbyname(socket.gethostname())
    label = Label(window, text=f"Your IP is: {ip}\nWaiting for player", font=("Times New Roman", 60), bg='green')
    label.pack(expand=True, fill='both')
    Back.pack(expand=True, fill='both')
    window.update()
    s.bind((ip, port))

    s.listen(5)
    c, addr = s.accept() # todo make so window updates here so back button works

    thread1 = threading.Thread(target=main(), args=None)
    thread2 = threading.Thread(target=server(), args=None)
    thread1.start()
    thread2.start()


#todo code for connecting to server
def connect():

    host.pack_forget()
    join.pack_forget()
    Back.pack_forget()
    text.pack(expand=True, fill='both')
    Enter.pack(expand=True, fill='both')
    Back.pack(expand=True, fill='both')


#todo code for connecting to server
def enter():

    ip = text.get("1.0", "end-1c")
    s = socket.socket()
    port = 12345
    s.connect((ip, port))

    while True:
        print(s.recv(1024).decode())


# variables subject to change (based on computer and preference)
screen_height = 950
screen_width = 1500
gamespeed = 5
difficulty = 3 # higher numbers = easier

# constant variables
p1 = 325
p2 = 325
ballx = screen_width/2 - 25
bally = screen_height/2 - 25
slopex = gamespeed
slopey = 0
p1score = 0
p2score = 0
itr = 0

# setup for window
window = Tk()
window.title("Pong")
window.geometry("1920x1080")
window.attributes('-fullscreen', True)
window.configure(bg='black')
AI = Button(window, height=2, width=20, bg='green', text="Pong\nClick To Play Against AI",
            font=("Times New Roman", 60), command=lambda: main())
AI.pack(expand=True, fill='both')
Online = Button(window, height=2, width=20, bg='green', text="Pong\nClick To Play Online",
            font=("Times New Roman", 60), command=lambda: main2())
Online.pack(expand=True, fill='both')
host = Button(window, height=2, width=20, bg='green', text="Host Server",
              font=("Times New Roman", 60), command=lambda: server_start())
join = Button(window, height=2, width=20, bg='green', text="Join Server",
              font=("Times New Roman", 60), command=lambda: connect())
Back = Button(window, height=2, width=20, bg='green', text="Main Menu",
              font=("Times New Roman", 60), command=lambda: back())
score = Button(window, command=lambda: main())
label = Label(window)
text = Text(window, height=2, width=20, bg="white", font=("Times New Roman", 60))
Enter = Button(window, height=2, width=20, bg='green', text="Enter IP",
               font=("Times New Roman", 60), command=lambda: enter())
canvas = tkinter.Canvas(window, bg='gray', height=screen_height, width=screen_width)
listener = keyboard.Listener(on_press=keypress)
listener.start()
window.mainloop()
