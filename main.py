from tkinter import Tk, Entry, Text, Button, Label, END
from pathlib import Path
import os
from random import choices

'''
 1. Set up timer to count down from 60 seconds when button is pushed.
 2. Create come kind of paragraph text box.
 3. Get some text to test with.

 Next steps:
 Make the text entry box cycle to the next paragraph when pressing Enter.
'''

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
        self.start_button = Button(text='Start Test.', command=self.start_timer)
        self.seconds = 60
        self.timer_display = Label(text=str(self.seconds))
        self.timer_on = False

        # Text input
        self.input_box = Text(width=35, height=20)

        # Get paragraphs
        self.paragraphs = self.get_paragraphs()
        self.sequence_number = 0
        self.test_paragraph = Text(width=35, height=20, wrap='word')
        self.test_paragraph.insert(END, intro)
        

        # Set up UI
        self.timer_display.grid(column=0, row=0)
        self.start_button.grid(column=1, row=0)
        self.test_paragraph.grid(column=0, row=1)
        self.input_box.grid(column=1, row=1)
        

    def start_timer(self):
        if self.timer_on:
            return
        self.timer_on = True
        self.countdown()

    def countdown(self):
        if self.seconds == 0:
            self.seconds = 60
            self.timer_on = False
            self.timer_display.config(text=str(self.seconds))
            return
        self.timer = self.window.after(1000, self.countdown)
        self.seconds = self.seconds - 1
        self.timer_display.config(text=str(self.seconds))

    def get_paragraphs(self):
        paragraphs = []
        with open('paragraphs.txt', 'r') as file:
            input = file.readlines()
        for i in input:
            paragraphs.append(i.strip('\n').strip())
        randomized_paragraphs = choices(paragraphs, k=len(paragraphs))
        return randomized_paragraphs
        
        


def main():
    app = App()
    # print(app.paragraphs)
    app.window
    app.window.mainloop()


if __name__ == "__main__":
    main()