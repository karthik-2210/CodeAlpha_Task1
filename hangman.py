import tkinter as tk
from tkinter import messagebox
import random

# Word categories
WORD_CATEGORIES = {
    "Animals": ["elephant", "giraffe", "dolphin", "kangaroo", "penguin", "tiger"],
    "Programming": ["python", "compiler", "variable", "function", "recursion", "loop"],
    "Countries": ["canada", "brazil", "germany", "japan", "nigeria", "france"],
    "Sports": ["cricket", "football", "badminton", "basketball", "wrestling"],
    "Foods": ["pizza", "lasagna", "burger", "sushi", "biryani"],
    "Movies": ["inception", "avatar", "titanic", "gladiator", "matrix"]
}

MAX_HINTS = 3
MAX_TRIES = 6

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Advanced Hangman Game")
        self.wins = 0
        self.losses = 0
        self.reset_variables()

        self.setup_ui()

    def reset_variables(self):
        self.word = ""
        self.guessed = set()
        self.tries_left = MAX_TRIES
        self.hints_left = MAX_HINTS

    def setup_ui(self):
        # Category selection
        tk.Label(self.root, text="Choose Category:").pack()
        self.category_var = tk.StringVar(self.root)
        self.category_var.set("Animals")
        category_menu = tk.OptionMenu(self.root, self.category_var, *WORD_CATEGORIES.keys())
        category_menu.pack()

        # Canvas for hangman
        self.canvas = tk.Canvas(self.root, width=200, height=250)
        self.canvas.pack()

        # Word display
        self.word_label = tk.Label(self.root, font=("Courier", 24))
        self.word_label.pack(pady=10)

        # Keyboard frame
        self.keyboard_frame = tk.Frame(self.root)
        self.keyboard_frame.pack()
        self.letter_buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(self.keyboard_frame, text=letter, width=4, command=lambda l=letter: self.guess_letter(l.lower()))
            btn.grid(row=i//9, column=i%9, padx=2, pady=2)
            self.letter_buttons[letter] = btn

        # Hint and Restart
        self.hint_btn = tk.Button(self.root, text="💡 Hint", command=self.use_hint)
        self.hint_btn.pack(pady=5)

        self.restart_btn = tk.Button(self.root, text="🔁 New Game", command=self.new_game)
        self.restart_btn.pack(pady=5)

        # Score
        self.score_label = tk.Label(self.root, text="Wins: 0 | Losses: 0")
        self.score_label.pack(pady=10)

        self.new_game()

    def new_game(self):
        self.reset_variables()
        self.word = random.choice(WORD_CATEGORIES[self.category_var.get()])
        self.update_display()
        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL)
        self.draw_hangman()
        self.update_score()

    def update_display(self):
        displayed = ' '.join([letter if letter in self.guessed else '_' for letter in self.word])
        self.word_label.config(text=displayed)

    def guess_letter(self, letter):
        self.letter_buttons[letter.upper()].config(state=tk.DISABLED)
        self.guessed.add(letter)
        if letter not in self.word:
            self.tries_left -= 1
            self.draw_hangman()
        self.update_display()
        self.check_game_status()

    def use_hint(self):
        if self.hints_left == 0:
            messagebox.showinfo("No hints", "You have used all your hints.")
            return
        for letter in self.word:
            if letter not in self.guessed:
                self.guessed.add(letter)
                self.hints_left -= 1
                self.update_display()
                self.check_game_status()
                return

    def check_game_status(self):
        if all(letter in self.guessed for letter in self.word):
            self.wins += 1
            messagebox.showinfo("🎉 Victory", f"You guessed the word: {self.word.upper()}!")
            self.update_score()
            self.new_game()
        elif self.tries_left == 0:
            self.losses += 1
            messagebox.showinfo("💀 Game Over", f"The word was: {self.word.upper()}")
            self.update_score()
            self.new_game()

    def update_score(self):
        self.score_label.config(text=f"Wins: {self.wins} | Losses: {self.losses}")

    def draw_hangman(self):
        self.canvas.delete("all")
        # base
        self.canvas.create_line(20, 230, 180, 230)
        self.canvas.create_line(50, 230, 50, 20)
        self.canvas.create_line(50, 20, 130, 20)
        self.canvas.create_line(130, 20, 130, 40)
        if self.tries_left <= 5:
            self.canvas.create_oval(110, 40, 150, 80)  # head
        if self.tries_left <= 4:
            self.canvas.create_line(130, 80, 130, 140)  # body
        if self.tries_left <= 3:
            self.canvas.create_line(130, 100, 110, 120)  # left arm
        if self.tries_left <= 2:
            self.canvas.create_line(130, 100, 150, 120)  # right arm
        if self.tries_left <= 1:
            self.canvas.create_line(130, 140, 110, 180)  # left leg
        if self.tries_left <= 0:
            self.canvas.create_line(130, 140, 150, 180)  # right leg

# Launch the game
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
