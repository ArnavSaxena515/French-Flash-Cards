import os
import random
from tkinter import *

import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

try:
    word_dict = pd.read_csv("words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError:
    word_dict = pd.read_csv("data/french_words.csv").to_dict(orient="records")

english_translation = ''


def reset():
    os.remove("words_to_learn.csv")


def generate_words():
    global word_dict, word, english_translation, flip_timer
    window.after_cancel(flip_timer)
    new_pair = random.choice(word_dict)
    canvas.itemconfig(word, text=new_pair["French"], fill="black")
    canvas.itemconfig(fre, fill="black", text="French")
    print(new_pair)
    english_translation = new_pair["English"]
    canvas.itemconfig(canvas_image, image=front_card)
    flip_timer = window.after(3000, func=flip)
    return new_pair


def tick():
    new_pair = generate_words()
    remove_word(new_pair)


def cross():
    generate_words()


def remove_word(item_to_remove):
    word_dict.remove(item_to_remove)
    words_to_go = pd.DataFrame(word_dict)
    words_to_go.to_csv("words_to_learn.csv", index=False)


def flip():
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(word, text=english_translation, fill="white")
    canvas.itemconfig(fre, fill="white", text="English")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flashy")
flip_timer = window.after(3000, flip)

front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_image = canvas.create_image(410, 263, image=front_card)

fre = canvas.create_text(400, 150, text="", font="Calibri 50 italic ")
word = canvas.create_text(400, 263, text="", font="Calibri 60 bold ")
canvas.grid(row=1, column=1, columnspan=2)

wrong = PhotoImage(file="images/wrong.png")
right = PhotoImage(file="images/right.png")

wrong_button = Button(image=wrong, highlightthickness=0, borderwidth=0, command=cross)
wrong_button.grid(column=1, row=2)

right_button = Button(image=right, highlightthickness=0, borderwidth=0, command=tick)
right_button.grid(column=2, row=2)
reset_button = Button(text="Reset", highlightthickness=0, borderwidth=0, command=reset, fg="Red",
                      activebackgroun=BACKGROUND_COLOR,
                      font="Calibri 40 bold ")
reset_button.grid(row=3, column=1, columnspan=2, )
generate_words()
window.mainloop()
