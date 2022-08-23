import random
import string
from english_words import english_words_set
import keyboard

# Generate a string of 7 letters
def generateLetters():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    picked_chars = set()

    while len(picked_chars) != 7:
        num = random.randint(0, 25)
        picked_chars.add(chars[num])
    
    print(picked_chars)

    return list(picked_chars)

# Draw ASCII ART of the characters

def drawLetterHexes(picked_chars):
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
    


def main():
    print("\nWelcome to PyBee, a Python implementation of New York Times' Spelling Bee!")
    print("\nPress 'ESC' to quit.\n")

    print("The letters are: ")
    picked_chars = generateLetters()
    drawLetterHexes(picked_chars)

    keyboard.wait("esc")

if __name__ == "__main__":
    main()


