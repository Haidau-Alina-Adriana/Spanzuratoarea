import random
import os

score = {"Number of played games": 0, "Won games": 0, "Lost games": 0}


def display_start_menu():
    print("\nHi! :)")
    print("You can choose to guess a word from a certain category or you can leave the app.")
    print("Choose a number that corresponds to the category from which you want to guess the word or exit: ")
    print("[0] EXIT")
    print("[1] Food -> ingredients")
    print("[2] House -> things from a house")
    print("[3] Feelings")
    print("[4] Clothing")
    print("[5] Careers")
    print("[6] Programming -> computer science related")
    print("[7] Animals")
    print("[8] Universe -> things from space")
    print("[9] Human body")
    print("[10] Car -> car related (even brands)")


def display_menu():
    print()
    print("Choose a category (or 0 to exit): ")
    print("[0] EXIT")
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
            if category < 0 or category > 10:
                raise ValueError()
            return category
        except ValueError:
            print("Please enter a valid number (between 0 and 10 and numbers only): ")


def display_category(category):
    possible_categories = {0: "EXIT", 1: "Food", 2: "House", 3: "Feelings", 4: "Clothing", 5: "Careers",
                           6: "Programming", 7: "Animals", 8: "Universe", 9: "HumanBody", 10: "Car"}
    result = possible_categories.get(category)
    print("You have chosen: " + str(result))
    return get_word(result)


def get_word(category):
    category_file = str(category) + ".txt"
    try:
        file = open(category_file, "r")
        line_count = 0
        for _ in file:
            line_count += 1
        row_number = random.randint(0, line_count - 1)
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


def update_and_register_score(result):
    score.update({"Number of played games": score.get("Number of played games") + 1})
    if result == 1:
        score.update({"Won games": score.get("Won games") + 1})
    else:
        score.update({"Lost games": score.get("Lost games") + 1})
    if not os.path.isfile('./log.txt'):
        file = open("log.txt", "x")
        file.write(str(score))
    else:
        file = open("log.txt", "w")
        file.write(str(score))
    file.close()


def start_guessing(word, attempts):
    diff = attempts
    current_state = ["_" for _ in range(len(word))]
    used_letters = []
    while True:
        print("--->   " + ' '.join(current_state) + "              Number of attempts left: " + str(attempts))
        print("Check this letter: ", end='')
        letter = input().lower()
        mistake = 0
        if letter == '':
            print("Give me a letter, buddy.")
            continue
        if len(letter) > 1 or not letter.isalpha():
            print("Please only one letter at a time, no numbers or others characters.")
            mistake = 1
        if letter in used_letters:
            if attempts != 1:
                print("Try a different letter.")
            mistake = 1
        else:
            used_letters.append(letter)
        ok = 0
        for curr_letter in range(0, len(word)):
            if mistake == 1:
                break
            if word[curr_letter] == letter:
                current_state[curr_letter] = letter
                ok = 1
        if "_" not in current_state:
            return 1, diff - attempts
        if ok == 0 or mistake == 1:
            attempts = attempts - 1
        if attempts == 0:
            print("--->   " + ' '.join(current_state) + "              Number of attempts left: " + str(attempts))
            return -1, diff - attempts


def start_game():
    display_start_menu()
    while True:
        category = get_category()
        if category == 0:
            print("Sad to see you leaving :(")
            return
        word_to_guess = display_category(category)
        number_of_attempts = int(len(word_to_guess) / 2 + 1)
        result, failed_attempts = start_guessing(word_to_guess, number_of_attempts)
        update_and_register_score(result)
        if result == 1:
            print()
            print("The word was: " + word_to_guess)
            print("Well played!")
            print("Failed attempts: " + str(failed_attempts))
        else:
            if result == -1:
                print()
                print("You don't have any attempts left!")
                print("The word was: " + word_to_guess)
                print("Failed attempts: " + str(failed_attempts))
        display_menu()


if __name__ == '__main__':
    start_game()
