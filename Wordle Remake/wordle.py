import random

# Sample word list (usually you'd want a bigger list)
WORD_LIST = [
    "apple", "bread", "crane", "drink", "eagle",
    "flame", "grape", "house", "input", "joker",
    "knife", "lemon", "mango", "night", "ocean",
    "piano", "queen", "river", "snake", "tiger",
    "urban", "vivid", "whale", "xenon", "yield", "zebra"
]

# Colors for terminal output (works on many terminals)
GREEN = '\033[92m'    # correct letter & position
YELLOW = '\033[93m'   # correct letter wrong position
GRAY = '\033[90m'     # letter not in word
RESET = '\033[0m'     # reset color


def get_feedback(guess, target):
    """Returns a string with colored feedback like Wordle"""
    feedback = [''] * 5
    target_chars = list(target)

    # First pass: check correct positions (green)
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = GREEN + guess[i].upper() + RESET
            target_chars[i] = None  # mark matched

    # Second pass: check letters in wrong positions (yellow)
    for i in range(5):
        if feedback[i] == '':
            if guess[i] in target_chars:
                feedback[i] = YELLOW + guess[i].upper() + RESET
                target_chars[target_chars.index(guess[i])] = None
            else:
                feedback[i] = GRAY + guess[i].upper() + RESET

    return ''.join(feedback)


def main():
    target_word = random.choice(WORD_LIST)
    attempts = 6

    print("Welcome to Wordle! Guess the 5-letter word.")
    print(f"You have {attempts} attempts.\n")

    for attempt in range(1, attempts + 1):
        while True:
            guess = input(f"Attempt {attempt}: ").lower()
            if len(guess) != 5:
                print("Please enter exactly 5 letters.")
            elif guess not in WORD_LIST:
                print("Word not in word list. Try another word.")
            else:
                break

        feedback = get_feedback(guess, target_word)
        print(feedback, "\n")

        if guess == target_word:
            print(f"Congratulations! You guessed the word in {attempt} attempts.")
            break
    else:
        print(f"Sorry, you ran out of attempts. The word was: {target_word.upper()}")


if __name__ == "__main__":
    main()
