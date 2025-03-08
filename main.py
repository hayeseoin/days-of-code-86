from tkinter import Tk, Entry, Text, Button, Label, END
from pathlib import Path
import os
from random import choices
from time import sleep


app_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_dir)
intro = \
'''Welcome to the typing speed test. 

Press 'Start test' to being the test. A number of test phrases will appear in this box.

Write out as many paragraphs as you can in the box to the right. Press 'Enter' when finished each paragraph.

You have 60 seconds.
'''


class App:
    def __init__(self):
        self.window = Tk()
        self.window.config(padx=5, pady=5)

        # Timer
        self.start_button = Button(text='Start Test.', command=self.click_start)
        self.seconds = 60
        self.starting_seconds = 3
        self.timer_display = Label(text=str(self.seconds))
        self.timer_on = False

        # Text input
        self.input_box = Text(width=35, height=20, wrap='word')
        self.input_box.config(state='disabled')
        self.next_button = Button(text='Next', command=self.submit_paragraph)
        self.input_box.bind('<Return>', self.press_enter)

        # Get paragraphs
        self.paragraphs = self.get_paragraphs()
        self.sequence_number = 0
        self.test_paragraph = Text(width=35, height=20, wrap='word')
        self.test_paragraph.insert(END, intro)
        self.test_paragraph.config(state='disabled')
        
        # word counts
        self.test_paragraph_words = []
        self.input_words = []

        # Game Logic
        self.game_on = False


        # Set up UI
        self.timer_display.grid(column=1, row=0)
        self.start_button.grid(column=0, row=0)
        self.test_paragraph.grid(column=0, row=1)
        self.input_box.grid(column=1, row=1)    
        self.next_button.grid(column=1, row=2)   

    def start_game(self):
        self.game_on = True
        self.input_box.config(state='normal')
        self.input_box.focus_set()
        self.input_box.delete('1.0', END)
        self.next_paragraph()
        self.countdown()

    def starting_countdown(self):
        if self.starting_seconds == 0:
            self.start_game()
            return
        self.timer_on = True
        self.input_box.focus_set()
        self.test_paragraph.config(state='normal')
        self.test_paragraph.delete('1.0', END)
        self.test_paragraph.insert(END, f'{self.starting_seconds}...')
        self.test_paragraph.config(state='disabled')
        self.starting_seconds -= 1
        self.window.after(1000, self.starting_countdown)

    def countdown(self):
        if self.seconds == 0:
            self.seconds = 60
            self.timer_display.config(text=str(self.seconds))
            self.game_end()
            return
        self.timer = self.window.after(1000, self.countdown)
        self.seconds = self.seconds - 1
        self.timer_display.config(text=str(self.seconds))

    def submit_paragraph(self):
        if not self.game_on:
            return
        input_text = self.input_box.get('1.0', END)
        self.input_box.delete('1.0', END)
        self.input_box.delete('1.0', END)
        self.record_words(input_text, self.input_words)
        self.sequence_number += 1
        self.input_box.focus_set()
        self.next_paragraph()

    def next_paragraph(self):
        self.test_paragraph.config(state='normal')
        next_paragraph = self.paragraphs[self.sequence_number]
        self.record_words(next_paragraph, self.test_paragraph_words)
        self.test_paragraph.delete('1.0', END)
        self.test_paragraph.insert(END, next_paragraph)
        self.test_paragraph.config(state='disabled')

    def get_paragraphs(self):
        paragraphs = []
        with open('paragraphs.txt', 'r') as file:
            input = file.readlines()
        for i in input:
            paragraphs.append(i.strip('\n').strip())
        randomized_paragraphs = choices(paragraphs, k=len(paragraphs))
        return randomized_paragraphs

    def game_end(self):
        self.timer_on = False
        self.game_on = False
        input_text = self.input_box.get('1.0', END)
        self.record_words(input_text, self.input_words)
        word_count = 0
        for i in self.input_words:
            word_count += len(i)

        mistakes = 0
        for i, j in zip(self.input_words, self.test_paragraph_words):
            for k in range(len(i)):
                if i[k] != j[k]:
                    mistakes += 1
        result = f'You type at {word_count} words per minute.\nYou made {mistakes} mistakes.'

        self.input_box.delete('1.0', END)
        self.input_box.config(state='disabled')

        self.test_paragraph.config(state='normal')
        self.test_paragraph.delete('1.0', END)
        self.test_paragraph.insert(END, result)
        self.test_paragraph.config(state='disabled')

    def press_enter(self, event):
        self.submit_paragraph()
        return 'break'

    def click_start(self):
        if self.timer_on:
            return
        self.starting_seconds = 3
        self.starting_countdown()

    def record_words(self, source: str, target: list[str]):
        target.append(source.strip('\n').split(' '))

def main():
    app = App()
    app.window
    app.window.mainloop()


if __name__ == "__main__":
    main()