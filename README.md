# Wordle Remake (Console & GUI Versions)

This project is a Python remake of the popular **Wordle** game. It includes both a **console-based version** and a fully functional **Tkinter GUI version**, with additional features like dark mode, hints, and unused letter tracking.

---

## Game Versions

### Console Version
- A simple, text-based version of Wordle.
- Runs directly in the terminal or command line.
- Randomly selects a 5-letter word from a text file (`words.txt`).
- You get 6 attempts to guess the correct word.
- After each guess, feedback is given:
  - Correct letter in correct position
  - Correct letter in wrong position
  - Incorrect letter

### GUI Version (Tkinter)
- Built with Python’s built-in `tkinter` module.
- Features:
  - Word grid similar to the official Wordle layout.
  - Dark/Light mode toggle.
  - Toggle to show unused letters after each guess.
  - "Hint" button that reveals one letter in the next guess row.
- Later Features:
  - Scrollable word list on the left showing words from `words.txt`.
- The app selects a random 5-letter word from the same `words.txt` file.
- Once the game is over, users are prompted to play again.

---

## File Structure
wordle-remake/
--wordle.py # Console version
--wordleGUI.py # GUI version
--words.txt # List of allowed 5-letter words

---

## `words.txt` – Word List
- All valid 5-letter words used by both game versions are stored in `words.txt`.
- This allows you to customize the game easily—just add or remove words from the file.
- In the current version, the GUI references this file directly and validates guesses based on it.

---

> **Note:** Until a full dictionary integration is added, users should reference `words.txt` to know which guesses are valid.

---

## How to Run

### Console Version
python wordle.py

### GUI Version
python wordleGUI.py

---

### Requirements
tkinter
random
python

---

### Author
This was built as learning experience and fun side project. The GUI version especially was designed to mimic the layout and logic of the real Wordle game, while also exploring Tkinter features like grid layout, theming, and event handling. The overall project took me a couple of days to complete since I am a student and have other responsibilities. AI was used in addition to my own code for error analysis as well as making my code a bit cleaner and more efficient to look back on for future projects.

--

### Feedback
If you come into any errors or would like to contribute, open an issue or send a pull request. All improvements are welcome!
