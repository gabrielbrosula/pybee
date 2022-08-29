import random
import json
import re
import time
import sys
import argparse

CHARS = "ABCDEFGHIJKLMNOPQRTUVWXYZ"

# Print the time taken to execute of various functions
measurePerf = False      

# Load english words
def load_words():
    with open("words_dictionary.json") as words_file:
        words_dict = json.load(words_file)

    return words_dict


# Generate a string of 7 letters
# TODO: Devise improved algorithm for letter set generation
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
def score_word(word, picked_chars, print_notif=True):

    word_score = 0

    if len(word) == 4:
        word_score = 1
    else:
        word_score = len(word)

        # Detect pangram
        if ( (len(word) >= 7) and (set(word.upper()) == set(picked_chars) )):
            word_score += 7

            if print_notif: 
                print("Pangram!")
    
    return word_score

# Generate the list of all possible valid words
def generate_valid_words(picked_chars, words_dict):

    mid_char = picked_chars[3].lower()
    
    # Regex to match only words containing letters from a restricted alphabet
    re_str = r'\b[' + ''.join(picked_chars) + r']+\b'
    pat = re.compile(re_str, re.IGNORECASE)

    start = time.perf_counter()
    
    # Ensure that middle character shows up in each word
    valid_words_list = [word for word in words_dict.keys() if (len(word) >= 4 and pat.match(word) and mid_char in word)]
    end = time.perf_counter()

    if measurePerf:
        print(f"Found all valid words in {end - start:0.4f} seconds.")

    return valid_words_list

# Get the maximum possible score
def get_max_score(valid_words_list, picked_chars):

    max_score = 0

    # Measure performance of getting the maximum score
    start = time.perf_counter()

    for word in valid_words_list:

            # Disable printing of "Pangram!" notification with False parameter
            max_score += score_word(word, picked_chars, False)

    end = time.perf_counter()
    
    if measurePerf: print(f"Found max possible score in {end - start:0.4f} seconds.")
    
    return max_score

# Shuffle the picked characters EXCEPT for the middle character
def shuffle_chars(picked_chars):
    copy = picked_chars
    mid_char = copy.pop(3)

    random.shuffle(copy)

    copy.insert(3, mid_char)

    return copy

# Check validity of picked chars set the valid words list
'''
Ensure that the valid words list is:
- not empty (and has enough words)
- has at least one pangram
'''
def is_valid(picked_chars, words_dict):

    if (len(picked_chars) == 0):
        return False

    valid_words_list = generate_valid_words(picked_chars, words_dict)

    # Check if there is a pangram
    has_pangram = any( [set(word.upper()) == set(picked_chars) for word in valid_words_list] )
    
    return len(valid_words_list) >= 20 and not has_pangram

def main():

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A Python implementation of New York Times' Spelling Bee!")
    parser.add_argument('-m', '--mode', type=str, help='The Spelling Bee mode you want to play. The options are randoms, custom, and date ', default='random')
    args = parser.parse_args()

    picked_chars = []
    date = ''
    words_dict = load_words()

    # Generate the picked character list 
    if args.mode == 'random':

        while not is_valid(picked_chars, words_dict):
            picked_chars = generate_letters()

    if args.mode == 'custom':

        pcl_input = input("Enter the custom letter set you want to use (first letter = central letter): ")

        pcl_input.upper()

        for c in pcl_input:
            picked_chars.append(c)
        
        # Switch the first and central characters
        picked_chars[3] = pcl_input[0]
        picked_chars[0] = pcl_input[3]

    elif args.mode == 'date':

        date = input("Enter a date (yy-mm-dd): ")
        date.replace('-', '')

        # TODO: Retrieve the letters based on the date
        # TODO: Retrieve the official answers list based on the date

        # Date of the first puzzle
        MAY_9_2018 = 1

    print("\nWelcome to PyBee, a Python implementation of New York Times' Spelling Bee!")

    # Generate the letters and draw hex art
    # Generate letters until a valid set is picked

    print("The letters are: ")
    draw_letter_hexes(picked_chars)

    # Generate the valid words list and get the max score
    valid_words_list = generate_valid_words(picked_chars, words_dict)
    max_score = get_max_score(valid_words_list, picked_chars)

    print("\nMake words from the letters shown above!")
    print(f"The number of valid words is {len(valid_words_list)} and the maximum possible score is {max_score}!")
    print(f"How many words can you get?")

    print("\nScore: 0")

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


if __name__ == "__main__":
    main()

