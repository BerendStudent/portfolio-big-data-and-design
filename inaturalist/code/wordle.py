import pandas as pd
import random

#file = 'inaturalist/code/EUPVP_Official_List.xlsx'
#df = pd.read_excel(file)


words = ['gudrun', 'red mountain', 'alko', 'gufi', 'vulpera', 'arone', 'bison']

print('Guess the word!')
random_word = words[random.randint(0, len(words))]

guessed = []
for i in range(0, len(random_word)):
    guessed.append('_')

delimeter = ""

def process_guess(guess, guessed_array, target):
    for i in range(0, len(guessed_array)):
        if guess[i] == target[i]:
            guessed_array[i] = target[i]
    return guessed_array

def check_victory(guessed_array, target):
    for i in range(0, len(target)):
        if guessed_array[i] != target[i]:
            return False
    return True

while True:
    print(f'Current guess: {delimeter.join(guessed)}')
    word = input('Insert equal length word: ')
    if len(word) != len(random_word):
        print('Incorrect length!')
        continue
    guessed = process_guess(word, guessed, random_word)
    if check_victory(guessed, random_word):
        print(f'Victory! The word was: {random_word}')
        break