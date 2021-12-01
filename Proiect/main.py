import os
import random
import time


class Error(Exception):
    pass


class ValueNotInRange(Error):
    pass


score = {"won game": "no", "time": "none"}


def display_menu():
    print("\nHi! :)")
    print("You can choose to guess a word from a certain category or you can leave the app.")
    print("Choose a number that corresponds to the category from which you want to guess the word or exit: ")
    print("[0] Exit the program")
    print("[1] Food")
    print("[2] House")
    print("[3] Feelings")
    print("[4] Clothing")
    print("[5] Careers")
    print("[6] Programming")
    print("[7] Animals")
    print("[8] Universe")
    print("[9] Human body")
    print("[10] Car")


def get_category():
    while True:
        try:
            category = int(input("Category:"))
            if category < 0 or category > 12:
                raise ValueNotInRange
            return category
        except ValueError:
            print("Please enter a number corresponding with the category: ")
        except ValueNotInRange:
            print("This value is not a valid option!")


def get_word(category):
    category_file = str(category) + ".txt"
    try:
        file = open(category_file, "r")
        line_count = 0
        for _ in file:
            line_count += 1
        row_number = random.randint(0, line_count)
        file.seek(0)
        word = ""
        for i, row in enumerate(file):
            if i + 1 == row_number:
                word = row
                break
        file.close()
        word = word.replace("\n", "")
        return word
    except FileNotFoundError:
        print("Couldn't find the file!")
    except IOError:
        print("Couldn't open the file!")


def display_category(category):
    switch = {
        0: "exit",
        1: "food",
        2: "house",
        3: "feelings",
        4: "clothing",
        5: "careers",
        6: "programming",
        7: "animals",
        8: "universe",
        9: "human body",
        10: "car"
    }
    result = switch.get(category)
    print("You have chosen: " + str(result))
    return get_word(result)


def start_guessing(word, attempts):
    diff = attempts
    current_state = ["_" for _ in range(len(word))]
    while True:
        print("--->   " + ' '.join(current_state) + "              Number of attempts left: " + str(attempts))
        print("Try: ", end='')
        letter = input().lower()
        mistake = 0
        if letter in current_state:
            if attempts != 1:
                print("Try a different letter.")
            mistake = 1
        if len(letter) > 1:
            print("Too many characters.")
            mistake = 1
        if letter.isdigit():
            print("Letters only.")
            mistake = 1
        ok = 0
        for curr_letter in range(0, len(word)):
            if mistake == 1:
                break
            if word[curr_letter] == letter:
                current_state[curr_letter] = letter
                ok = 1
        if "_" not in current_state:
            obj = time.localtime()
            obj = time.strftime("%Y-%m-%d -> %H:%M:%S", obj)
            return 1, diff - attempts, obj
        if ok == 0 or mistake == 1:
            attempts = attempts - 1
        if attempts == 0:
            print("--->   " + ' '.join(current_state) + "              Number of attempts left: " + str(attempts))
            obj = time.localtime()
            obj = time.strftime("%Y-%m-%d -> %H:%M:%S", obj)
            return -1, diff - attempts, obj


def update_and_register_score(result, finishing_time):
    if result == 1:
        score.update({"won game": "yes"})
    else:
        score.update({"won game": "no"})
    score.update({"time": finishing_time})
    if not os.path.isfile('./log.txt'):
        file = open("log.txt", "x")
        file.write(str(score))
    else:
        file = open("log.txt", "a")
        file.write("\n" + str(score))
    file.close()


def start_game():
    display_menu()
    category = get_category()
    if category == 0:
        print("Sad to see you leaving :(")
        return
    word_to_guess = display_category(category)
    number_of_attempts = int(len(word_to_guess) / 2 + 1)
    result, failed_attempts, fin_time = start_guessing(word_to_guess, number_of_attempts)
    update_and_register_score(result, fin_time)
    if result == 1:
        print()
        print("Failed attempts: " + str(failed_attempts))
        print("Well played!")
    else:
        if result == -1:
            print()
            print("You don't have any attempts left!")
            print("The word was: " + word_to_guess)
            print("Failed attempts: " + str(failed_attempts))


if __name__ == '__main__':
    start_game()
