from tkinter import *

from tkinter import StringVar
from dictionary import words
import random
from threading import Thread
from time import sleep



THEME_COLOR = "#375362"
BLACK_COLOR = "#000000"

class TypeInterface:

    def __init__(self):

        self.window = Tk()
        self.window.title("Type Speed")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.words = words
        self.chunk = ""
        self.index = 0
        # print(self.words[5])
        # ch = self.get_words()
        ch = "plant fall does notice this lead box work came again done fly came last record fill here act fine"
        self.canvas = Canvas(width=570, height=150, bg="white")
        self.cpm = 0
        self.wpm = 0


        self.canvas.grid(row=1, column=0, columnspan=6, pady=50)
        # this will create a label widget
        l1 = Label(self.window, text="Corrected CPM:")
        l2 = Label(self.window, text="WPM")
        l3 = Label(self.window, text="Time Left")
        self.cpm_text = Entry(self.window,  width=10)
        self.wpm_text = Entry(self.window,  width=10)
        self.time_left = Entry(self.window, width=10)

        self.cpm_text.insert(index=0, string="?")
        self.wpm_text.insert(index=0, string="?")
        self.time_left.insert(index=0, string="60")

        self.cpm_text.config(state=DISABLED)
        self.wpm_text.config(state=DISABLED)
        self.time_left.config(state=DISABLED)

        self.get_words()
        self.canvas.create_text(300, 50, text=self.chunk, fill="black", font=('Helvetica 15 bold'))
        l1.grid(row=0, column=0)
        self.cpm_text.grid(row=0, column=1)
        l2.grid(row=0, column=2)
        self.wpm_text.grid(row=0, column=3)
        l3.grid(row=0, column=4)
        self.time_left.grid(row=0, column=5)

        var = StringVar()
        var.trace_add('write', self.true_pressed)

        # self.question_text = Entry(self.window,  justify="center", width=90, textvariable=var)
        self.question_text = Entry(self.window, justify="center", width=90)
        self.question_text.grid(row=2, column=0, columnspan=6)
        self.question_text.focus_set()
        self.question_text.bind("<Key>", self.keypress)

        self.timer_thread = Thread(target=self.timer)
        self.first = TRUE
        self.sleep_duration = 60
        self.window.mainloop()

    def timer(self):

        while self.sleep_duration > 0:
            self.time_left.config(state=NORMAL)
            self.time_left.delete(0, 'end')
            self.time_left.insert(index=0, string=str(self.sleep_duration))
            self.time_left.config(state=DISABLED)
            sleep(1)
            self.sleep_duration -= 1
        print("timer completed")

    def true_pressed(self, *args):
        self.question_text.insert(index=0, string=str(self.cpm))

    def keypress(self, event):
        if self.first:
            self.timer_thread.start()
            self.first = FALSE
        if self.timer_thread.is_alive():
            try:
                if ord(event.char) == 32:
                    self.check_word()
            except:  # for blank press
                pass
        else:
            print("Game over")
            self.update_values(0, 0)
            self.question_text.config(state=DISABLED)
    def get_words(self):


        for _ in range(1):
            for _ in range(5):
                self.chunk += random.choice(self.words) + " "
        print(self.chunk)

    def check_word(self, *args):

        a = self.chunk.split()

        print(f"Current text: {self.question_text.get()}, {a[self.index]}")
        if self.question_text.get().strip() == a[self.index].strip():

            self.question_text.delete(0, 'end')
            ll = len(a[self.index])
            self.index += 1
            self.update_values(ll, 1)

        else:

            self.index += 1
            self.question_text.delete(0, 'end')

        if self.index > 4:
            self.canvas.delete('all')
            self.chunk = ""
            self.get_words()
            self.canvas.create_text(300, 50, text=self.chunk, fill="black", font=('Helvetica 15 bold'))
            self.index = 0

    def update_values(self, count, wc):

        self.cpm += count
        self.wpm += wc

        current_cpm = int((60 * self.cpm) / (60-self.sleep_duration))
        current_wpm = int((60 * self.wpm) / (60-self.sleep_duration))

        self.cpm_text.config(state=NORMAL)
        self.cpm_text.delete(0, 'end')
        self.cpm_text.insert(index=0, string=str(current_cpm))
        self.cpm_text.config(state=DISABLED)

        self.wpm_text.config(state=NORMAL)
        self.wpm_text.delete(0, 'end')
        self.wpm_text.insert(index=0, string=str(current_wpm))
        self.wpm_text.config(state=DISABLED)

        return
