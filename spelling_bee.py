import random
import string
from english_words import english_words_set
import keyboard

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Generate a string of 7 letters
def generate_letters():
    picked_chars = set()

    while len(picked_chars) != 7:
        num = random.randint(0, 25)
        picked_chars.add(CHARS[num])

    return list(picked_chars)

# Draw ASCII ART of the characters
def draw_letter_hexes(picked_chars):
    letter_hex_str = """
          ____
         /    \\
    ____/  {}   \\____
   /    \      /    \\
  /  {}   \____/  {}   \\
  \      /    \      /
   \____/  {}   \____/
   /    \      /    \\
  /  {}   \____/  {}   \\
  \      /    \      /
   \____/  {}   \____/
        \      /
         \____/
    
    
    """.format(*picked_chars)

    # Print the ASCII art string as raw text
    print(r"{}".format(letter_hex_str))

# Check if the word is valid
def is_word_valid(word, picked_chars):

    word_upper = word.upper()

    # Check if the word contains only valid letters
    if any(c not in picked_chars for c in word_upper):
        print("Invalid character(s) present!")
        return False

    # Check if the word contains the middle letter
    if (picked_chars[3] not in word_upper):
        print("Missing center letter!")
        return False

    # Check if the word is in the word list
    if (word not in english_words_set):
        print("Word not in word list!")
        return False
    else:
        print("Valid word!")
        return True
    


def main():
    print("\nWelcome to PyBee, a Python implementation of New York Times' Spelling Bee!")
    print("\nPress 'ESC' to quit.\n")

    print("The letters are: ")
    picked_chars = generate_letters()
    draw_letter_hexes(picked_chars)

    # Get user input
    print("Make words from the letters shown above!")

    while True:
        word_input = input()
        is_word_valid(word_input, picked_chars)

        if keyboard.press_and_release('esc'):
            return


if __name__ == "__main__":
    main()


