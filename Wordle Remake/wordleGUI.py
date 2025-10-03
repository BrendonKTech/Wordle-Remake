import os
import sys
import random
import tkinter as tk
from tkinter import messagebox

# Function to get path to resource
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller .exe """
    try:
        # PyInstaller sets this at runtime
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Word list placeholder — replace with your big list
def load_word_list(words):
    with open(resource_path(words), "r") as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == 5]
    return words

WORD_LIST = load_word_list("words.txt")


# Light mode colors
LIGHT_BG = "#ffffff"
LIGHT_TEXT = "#000000"
LIGHT_GREEN = "#6aaa64"
LIGHT_YELLOW = "#c9b458"
LIGHT_GRAY = "#787c7e"
LIGHT_EMPTY_BG = "#d3d6da"

# Dark mode colors
DARK_BG = "#121213"
DARK_TEXT = "#d7dadc"
DARK_GREEN = "#538d4e"
DARK_YELLOW = "#b59f3b"
DARK_GRAY = "#3a3a3c"
DARK_EMPTY_BG = "#818384"

FONT = ("Helvetica", 24, "bold")
ATTEMPTS = 6

class WordleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wordle")
        master.resizable(False, False)

        self.is_dark_mode = False
        self.show_unused = False

        self.target_word = random.choice(WORD_LIST)
        self.current_attempt = 0
        self.guessed_letters = set()
        self.incorrect_letters = set()

        self.setup_colors()
        self.create_widgets()
        self.update_colors()
        
        self.hints_used = 0
        self.max_hints = 1
        
        # Hint button
        self.hint_button = tk.Button(self.top_frame, text="Hint", command=self.use_hint)
        self.hint_button.pack(side=tk.RIGHT, padx=5)
        
    def use_hint(self):
        if self.hints_used >= self.max_hints:
            messagebox.showinfo("No hints left", "You have used all your hints.")
            return

        if self.current_attempt >= ATTEMPTS:
            messagebox.showinfo("Hint", "No more attempts left.")
            return

        # Collect letters already revealed (green tiles) in previous attempts
        revealed_positions = {}
        for attempt in range(self.current_attempt):
            for i, lbl in enumerate(self.guess_grid[attempt]):
                if lbl['bg'] == self.green:
                    revealed_positions[i] = lbl['text'].lower()

        # Find first letter and position in target word that is NOT revealed yet
        for i, letter in enumerate(self.target_word):
            if i not in revealed_positions:
                # Reveal this letter in the current attempt row at position i
                lbl = self.guess_grid[self.current_attempt][i]
                lbl.config(text=letter.upper(), bg=self.green, fg="white")

                self.hints_used += 1
                if self.hints_used >= self.max_hints:
                    self.hint_button.config(state=tk.DISABLED)

                messagebox.showinfo("Hint", f"Letter '{letter.upper()}' revealed at position {i+1}!")
                return

        # If all letters already revealed
        messagebox.showinfo("Hint", "All letters are already revealed!")


    def setup_colors(self):
        if self.is_dark_mode:
            self.bg_color = DARK_BG
            self.text_color = DARK_TEXT
            self.green = DARK_GREEN
            self.yellow = DARK_YELLOW
            self.gray = DARK_GRAY
            self.empty_bg = DARK_EMPTY_BG
        else:
            self.bg_color = LIGHT_BG
            self.text_color = LIGHT_TEXT
            self.green = LIGHT_GREEN
            self.yellow = LIGHT_YELLOW
            self.gray = LIGHT_GRAY
            self.empty_bg = LIGHT_EMPTY_BG

        self.master.configure(bg=self.bg_color)

    def create_widgets(self):
        # Top bar frame
        self.top_frame = tk.Frame(self.master, bg=self.bg_color)
        self.top_frame.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(10,5))

        self.title_label = tk.Label(self.top_frame, text="Wordle", font=("Helvetica", 30, "bold"),
                                    fg=self.text_color, bg=self.bg_color)
        self.title_label.pack(side="left", padx=10)

        self.settings_btn = tk.Button(self.top_frame, text="⋮", font=("Helvetica", 24), width=2, 
                                      command=self.toggle_settings, bg=self.bg_color, fg=self.text_color,
                                      bd=0, activebackground=self.bg_color, activeforeground=self.text_color)
        self.settings_btn.pack(side="right", padx=10)

        # Guess grid frame
        self.grid_frame = tk.Frame(self.master, bg=self.bg_color)
        self.grid_frame.grid(row=1, column=0, columnspan=5, pady=5, padx=10)

        self.guess_grid = []
        for row in range(ATTEMPTS):
            row_labels = []
            for col in range(5):
                lbl = tk.Label(self.grid_frame, text="", width=4, height=2, font=FONT,
                               relief="solid", borderwidth=2, bg=self.empty_bg, fg=self.text_color)
                lbl.grid(row=row, column=col, padx=3, pady=3)
                row_labels.append(lbl)
            self.guess_grid.append(row_labels)

        # Entry and submit button frame
        self.entry_frame = tk.Frame(self.master, bg=self.bg_color)
        self.entry_frame.grid(row=2, column=0, columnspan=5, pady=10)

        self.entry = tk.Entry(self.entry_frame, font=FONT, width=5, justify='center')
        self.entry.pack(side="left", padx=(0,10))
        self.entry.focus()
        self.entry.bind("<Return>", lambda event: self.submit_guess())

        self.submit_btn = tk.Button(self.entry_frame, text="Submit", font=FONT,
                                    command=self.submit_guess, bg=self.empty_bg, fg=self.text_color)
        self.submit_btn.pack(side="left")

        # Settings panel (hidden initially)
        self.settings_panel = tk.Frame(self.master, bg=self.bg_color, relief="raised", borderwidth=1)
        self.settings_panel.grid(row=3, column=0, columnspan=5, sticky="ew", padx=10)
        self.settings_panel.grid_remove()

        # Dark mode toggle
        self.dark_mode_var = tk.BooleanVar(value=self.is_dark_mode)
        self.dark_mode_check = tk.Checkbutton(self.settings_panel, text="Dark Mode", font=("Helvetica", 14),
                                              bg=self.bg_color, fg=self.text_color, selectcolor=self.bg_color,
                                              variable=self.dark_mode_var, command=self.toggle_dark_mode)
        self.dark_mode_check.pack(anchor="w", padx=10, pady=5)

        # Show unused letters toggle
        self.show_unused_var = tk.BooleanVar(value=self.show_unused)
        self.show_unused_check = tk.Checkbutton(self.settings_panel, text="Show Unused Letters", font=("Helvetica", 14),
                                                bg=self.bg_color, fg=self.text_color, selectcolor=self.bg_color,
                                                variable=self.show_unused_var, command=self.toggle_unused_letters)
        self.show_unused_check.pack(anchor="w", padx=10, pady=5)

        # Unused letters panel (hidden initially)
        self.unused_panel = tk.Frame(self.master, bg=self.bg_color)
        self.unused_panel.grid(row=4, column=0, columnspan=5, sticky="ew", padx=10)
        self.unused_panel.grid_remove()

        self.unused_label = tk.Label(self.unused_panel, text="Unused Letters: ", font=("Helvetica", 16),
                                     fg=self.text_color, bg=self.bg_color)
        self.unused_label.pack(side="left", padx=5, pady=5)

        self.unused_letters_text = tk.Label(self.unused_panel, text="", font=("Helvetica", 16, "bold"),
                                            fg=self.text_color, bg=self.bg_color)
        self.unused_letters_text.pack(side="left", padx=5, pady=5)

    def toggle_settings(self):
        if self.settings_panel.winfo_ismapped():
            self.settings_panel.grid_remove()
        else:
            self.settings_panel.grid()

    def toggle_dark_mode(self):
        self.is_dark_mode = self.dark_mode_var.get()
        self.setup_colors()
        self.update_colors()

    def toggle_unused_letters(self):
        self.show_unused = self.show_unused_var.get()
        if self.show_unused:
            self.unused_panel.grid()
            self.update_unused_letters()
        else:
            self.unused_panel.grid_remove()

    def update_colors(self):
        # Update all widget colors to match theme
        self.master.configure(bg=self.bg_color)
        self.top_frame.configure(bg=self.bg_color)
        self.title_label.configure(bg=self.bg_color, fg=self.text_color)
        self.settings_btn.configure(bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color, activeforeground=self.text_color)

        self.grid_frame.configure(bg=self.bg_color)
        for row_labels in self.guess_grid:
            for lbl in row_labels:
                # Only change bg of empty labels, colored ones keep their color
                if lbl['text'] == "":
                    lbl.configure(bg=self.empty_bg, fg=self.text_color)
                else:
                    # Adjust fg in case theme changed
                    lbl.configure(fg="white")

        self.entry_frame.configure(bg=self.bg_color)
        self.entry.configure(bg=self.empty_bg, fg=self.text_color, insertbackground=self.text_color)
        self.submit_btn.configure(bg=self.empty_bg, fg=self.text_color)

        self.settings_panel.configure(bg=self.bg_color)
        self.dark_mode_check.configure(bg=self.bg_color, fg=self.text_color, selectcolor=self.bg_color)
        self.show_unused_check.configure(bg=self.bg_color, fg=self.text_color, selectcolor=self.bg_color)

        self.unused_panel.configure(bg=self.bg_color)
        self.unused_label.configure(bg=self.bg_color, fg=self.text_color)
        self.unused_letters_text.configure(bg=self.bg_color, fg=self.text_color)

    def submit_guess(self):
        guess = self.entry.get().lower()
        if len(guess) != 5:
            messagebox.showwarning("Invalid input", "Please enter exactly 5 letters.")
            return
        if guess not in WORD_LIST:
            messagebox.showwarning("Invalid word", "Word not in word list.")
            return

        # Display guess and color feedback
        feedback = self.get_feedback(guess, self.target_word)

        for i, (char, color) in enumerate(feedback):
            lbl = self.guess_grid[self.current_attempt][i]
            lbl.config(text=char.upper(), bg=color, fg="white")

        # Track guessed and incorrect letters
        self.guessed_letters.update(guess)
        for i, (char, color) in enumerate(feedback):
            if color == self.gray:
                self.incorrect_letters.add(char)

        self.current_attempt += 1
        self.entry.delete(0, tk.END)

        # Update unused letters panel if visible
        if self.show_unused:
            self.update_unused_letters()

        if guess == self.target_word:
            self.ask_play_again(f"Congratulations! You guessed the word '{self.target_word.upper()}'!")
        elif self.current_attempt == ATTEMPTS:
            self.ask_play_again(f"Game Over! The word was '{self.target_word.upper()}'.")

    def ask_play_again(self, message):
        from tkinter import messagebox
        answer = messagebox.askyesno("Play Again?", message + "\n\nWould you like to play again?")
        if answer:
            self.reset_game()
        else:
            self.master.destroy()

    def reset_game(self):
        self.target_word = random.choice(WORD_LIST)
        self.current_attempt = 0
        self.guessed_letters.clear()
        self.incorrect_letters.clear()

        # Clear grid labels
        for row_labels in self.guess_grid:
            for lbl in row_labels:
                lbl.config(text="", bg=self.empty_bg, fg=self.text_color)

        self.entry.delete(0, tk.END)
        self.entry.focus()

        # Update unused letters panel
        if self.show_unused:
            self.update_unused_letters()
        else:
            self.unused_letters_text.config(text="")


    def get_feedback(self, guess, target):
        result = [None] * 5
        target_chars = list(target)

        # First pass: correct positions
        for i in range(5):
            if guess[i] == target[i]:
                result[i] = (guess[i], self.green)
                target_chars[i] = None

        # Second pass: letter in word but wrong position or not in word
        for i in range(5):
            if result[i] is None:
                if guess[i] in target_chars:
                    result[i] = (guess[i], self.yellow)
                    target_chars[target_chars.index(guess[i])] = None
                else:
                    result[i] = (guess[i], self.gray)

        return result

    def update_unused_letters(self):
        # Show incorrect letters sorted alphabetically
        sorted_letters = ' '.join(sorted(self.incorrect_letters)).upper()
        self.unused_letters_text.config(text=sorted_letters)


def main():
    root = tk.Tk()
    wordle = WordleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
