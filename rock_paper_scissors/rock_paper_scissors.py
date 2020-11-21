import tkinter
from tkinter import *
from random import randint


# initialize window where game will be played
root = tkinter.Tk()
root.geometry("1500x300")
root.title("Rock, Paper, Scissors")
root.config(bg="white smoke")

# Define top label name
label_top = tkinter.Label(root, text="Rock, Paper, Scissors Game: select your choice below with your mouse ")
label_top.grid(row=0, columnspan=6)
label_top.config(font="aerial 20 italic", bg="light green", bd=10, padx=270)

# variables
Result = StringVar()
player_number = IntVar()


# Function to play game and show result
def show_message(user_pick, comp_pick):
    if user_pick == 1 and comp_pick == 1:
        Result.set("Draw,you both selected Rock")
    elif user_pick == 2 and comp_pick == 2:
        Result.set("Draw,you both selected Paper")
    elif user_pick == 3 and comp_pick == 3:
        Result.set("Draw,you both selected Scissors")
    elif user_pick == 1 and comp_pick == 2:
        Result.set("You Lost! Comp picked paper, you chose rock. Paper beats rock!")
    elif user_pick == 1 and comp_pick == 3:
        Result.set("You Win! You chose rock, comp picked scissors. Rock beats scissors!")
    elif user_pick == 2 and comp_pick == 1:
        Result.set("You Win! You chose paper, comp picked rock. Paper beats rock!")
    elif user_pick == 2 and comp_pick == 3:
        Result.set("You Lost! Comp picked scissors, you chose paper. Scissors beats paper!")
    elif user_pick == 3 and comp_pick == 1:
        Result.set("You Lost! Comp picked rock, you chose scissors. Rock beats scissors!")
    elif user_pick == 3 and comp_pick == 2:
        Result.set("You Win! You chose scissors, Comp picked paper. Scissors beats paper!")


# Define entry label to show results
entry_label_top = tkinter.Label(root, textvariable=Result)
entry_label_top.grid(row=2, columnspan=6)
entry_label_top.config(font="roman 25 bold", fg="indian red", bd=25)


# Definition for computer choice
def comp():
    comp_pick = randint(1, 3)
    return comp_pick


# functions for user to make choice via pressing the button
def rock_clicked():
    user_pick = 1
    comp_pick = randint(1, 3)
    show_message(user_pick, comp_pick)


def paper_clicked():
    user_pick = 2
    comp_pick = randint(1, 3)
    show_message(user_pick, comp_pick)


def scissors_clicked():
    user_pick = 3
    comp_pick = randint(1, 3)
    show_message(user_pick, comp_pick)


# Functions for reset and close
def reset():
    player_number.set("")
    Result.set("")


def close():
    root.destroy()


# Define rock / paper / scissors / buttons
button_rock = tkinter.Button(root, text="Rock", command=lambda: rock_clicked())
button_rock.grid(row=1, column=0)
button_rock.config(font="aerial 20 bold", bg="dim grey", padx=30, pady=10, bd=10)

button_paper = tkinter.Button(root, text="Paper", command=lambda: paper_clicked())
button_paper.grid(row=1, column=2)
button_paper.config(font="aerial 20 bold", bg="cyan", padx=30, pady=10, bd=10)

button_scissors = tkinter.Button(root, text="Scissors", command=lambda: scissors_clicked())
button_scissors.grid(row=1, column=4)
button_scissors.config(font="aerial 20 bold", bg="gold", padx=30, pady=10, bd=10)

# Define reset and close button
reset_button = tkinter.Button(root, text="Reset", command=reset)
reset_button.grid(row=3, column=1, sticky=W)
reset_button.config(font="aerial 15 bold", bg="sandy brown", padx=30, pady=10, bd=10)

close_button = tkinter.Button(root, text="Close", command=close)
close_button.grid(row=3, column=3, sticky=E)
close_button.config(font="aerial 15 bold", bg="red", padx=30, pady=10, bd=10)


root.mainloop()
