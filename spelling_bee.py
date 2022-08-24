import random
import keyboard
import json

CHARS = "ABCDEFGHIJKLMNOPQRTUVWXYZ"
PICKED_CHARS_LIST = ['N', 'M', 'R', 'E', 'G', 'A', 'I']
rand_gen_letters = False

# Load english words
def load_words():
    with open("words_dictionary.json") as words_file:
        words_dict = json.load(words_file)

    return words_dict


# Generate a string of 7 letters
def generate_letters():
    picked_chars = set()

    while len(picked_chars) != 7:
        num = random.randint(0, len(CHARS) - 1)
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
def is_word_valid(word, picked_chars, word_list, words_dict):

    word_upper = word.upper()

    # Check if word is long enough
    if (len(word) <= 3):
        print("Insufficient word length!")
        return False

    # Check if the word contains only valid letters
    if any(c not in picked_chars for c in word_upper):
        print("Invalid character(s) present!")
        return False

    # Check if the word contains the middle letter
    if (picked_chars[3] not in word_upper):
        print("Missing center letter!")
        return False

    # Check if the word is in the dictionary
    if (word not in words_dict):
        print("Word not in word list!")
        return False
    
    # Check if the user has already inputted the word
    if (word in word_list):
        print("Word already inputted!")
        return False
    
    return True

# Properly score a valid word based on NYT Spelling Bee rules
def score_word(word, picked_chars):

    word_score = 0

    if len(word) == 4:
        word_score = 1
    else:
        word_score = len(word)
        # Detect pangram
        if ( (len(word) >= 7) and (set(word.upper()) == set(picked_chars) )):
            word_score += 7
            print("Pangram!")
    
    return word_score

def main():

    words_dict = load_words()

    print("\nWelcome to PyBee, a Python implementation of New York Times' Spelling Bee!")
    print("\nPress 'ESC' to quit.\n")

    print("The letters are: ")
    picked_chars = generate_letters() if rand_gen_letters else PICKED_CHARS_LIST
    draw_letter_hexes(picked_chars)

    # Get user input
    print("Make words from the letters shown above!")
    print("Score: 0")

    # List of inputted words
    word_list = []
    
    # Current score
    score = 0

    while True:
        word_input = input()
        if (is_word_valid(word_input, picked_chars, word_list, words_dict)):
            word_list.append(word_input)
            score += score_word(word_input, picked_chars)
            print(f"Score: {score}")

        if keyboard.press_and_release('esc'):
            return


if __name__ == "__main__":
    main()

