import random
import string
from english_words import english_words_set
import keyboard

# Generate a string of 7 letters
def generateLetters() -> set:
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    picked_chars = set()

    while len(picked_chars) != 7:
        num = random.randint(0, 25)
        picked_chars.add(chars[num])
    
    print(picked_chars)

    return picked_chars 


def main():
    print("\nWelcome to the PyBee, a Python implementation of New York Times' Spelling Bee!")
    print("\nPress 'ESC' to quit.\n")

    print("The letters are: ")
    generateLetters()

    keyboard.wait("esc")

if __name__ == "__main__":
    main()


