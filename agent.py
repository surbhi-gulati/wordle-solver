from wordle_solver import WordleSolver
from heuristics import HEURISTICS
from random import choice

def choose_word_length():
    """
    Gets user-selected word length (5, 6, or 7).

    Returns:
        word_length = (5, 6, or 7).
    """
    while True:
        try:
            word_length = int(input("Choose a word length (5, 6, or 7): "))
            if word_length in (5, 6, 7):
                return word_length
            print("Invalid word length. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def choose_word_list(word_length):
    """
    Reads the corresponding word list for the requested word length.

    Args:
        word_length: Chosen word length.

    Returns:
        word_list: Word list of specified length.
    """
    with open(f"{word_length}_letter_words.txt", "r") as f:
        word_list = f.read().splitlines()
    return word_list

def choose_heuristic_mode():
    """
    Prompts the user to choose a heuristic mode and validates their input.

    Returns:
        "single" if the user chooses a single heuristic,
        "comparison" if the user chooses to compare all heuristics.
    """
    while True:
        choice = input("Choose a heuristic mode: \n"
                       "1. Single Heuristic\n"
                       "2. Comparison Mode (All Heuristics)\n").lower()
        if choice in ("1", "single heuristic"):
            return "single"
        elif choice in ("2", "comparison mode", "all heuristics"):
            return "comparison"
        else:
            print("Invalid choice. Please try again.")

def choose_single_heuristic(heuristics):
    """
    Choose a single heuristic analysis by name or number.

    Args:
        heuristics: A dictionary of available heuristics functions.

    Returns:
        Chosen heuristic function.
    """
    while True:
        try:
            heuristic_choice = input("Enter name/number of your chosen heuristic (e.g., 1, letter_frequency, etc.): ")
            # Try to interpret choice as an integer (index)
            if heuristic_choice.isdigit():
                index = int(heuristic_choice) - 1
                if 0 <= index < len(heuristics):
                    if callable(list(heuristics.values())[index]):
                        return list(heuristics.values())[index]
                    else:
                        print(f"Invalid heuristic; choose from: {', '.join(heuristics.keys())}")
                else:
                    print(f"Invalid heuristic; choose from: {', '.join(heuristics.keys())}")
            # If not an integer, try to match the heuristic name
            else:
                if heuristic_choice in heuristics:
                    if callable(heuristics[heuristic_choice]):
                        return heuristics[heuristic_choice]
                    else:
                        print(f"Invalid heuristic; choose from: {', '.join(heuristics.keys())}")
                else:
                    print(f"Invalid heuristic; choose from: {', '.join(heuristics.keys())}")
        except ValueError:
            print("Invalid heuristic.")

def choose_word_list_size():
    """
    Choose whether to guess 1 or many words.

    Returns:
        "single" if the user chooses a single word,
        "multi" if the user chooses a percentage of the word list.
    """
    while True:
        choice = input("Choose a word list size: \n"
                       "1. one = randomly chosen word\n"
                       "2. many = many (percentage)\n").lower()
        if choice in ("1", "one"):
            return "single"
        elif choice in ("2", "many", "percentage"):
            return "multi"
        else:
            print("Invalid choice -- try again; choose 1) Single Word or 2) Multi-word analysis.")

def choose_percentage():
    """
    Prompts the user to enter a percentage (only used in "multi" mode).

    Returns:
        Selected percentage of word list.
    """
    while True:
        try:
            percentage = float(input("Enter percentage (1-100): "))
            if 1 <= percentage <= 100:
                return percentage
            else:
                print("Invalid percentage. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """
    Runs the Wordle solver based on user input settings.

    1. Get chosen word length list, "single" or "comparison" analysis & heuristic mode choice.
    2. "single" mode: Solves based on heuristic(s) selected on a single word.
    3. "comparison" mode: Solves based on heuristic(s) selected on a selected % of the list.
    """
    # Choose word length and word list
    word_length = choose_word_length()
    word_list = choose_word_list(word_length)

    # Choose heuristic mode
    heuristic_mode = choose_heuristic_mode()

    # One heuristic
    if heuristic_mode == "single":
        # Choose single heuristic
        heuristic = choose_single_heuristic(HEURISTICS)

        # Choose and solve a random secret word
        secret_word = choice(word_list)
        solver = WordleSolver(word_length, [heuristic])
        guesses = solver.solve(heuristic, secret_word)
        print(f"Word solved in {guesses} guesses using {heuristic} heuristic. (Secret word: {secret_word})")
    # Comparison (all heuristics)
    else:
        word_list_size = choose_word_list_size()

        if word_list_size == "single":
            # Single word
            secret_word = choice(word_list)
            for heuristic in HEURISTICS:
                solver = WordleSolver(word_length, [heuristic])
                guesses = solver.solve(heuristic, secret_word)
                print(f"{heuristic} heuristic solved the word in {guesses} guesses. (Secret word: {secret_word})")
        else:
            # % Word List
            percentage = choose_percentage()
            num_words = int(len(word_list) * percentage / 100)
            for heuristic in HEURISTICS:
                solver = WordleSolver(word_length, [heuristic])
                total_guesses = 0
                heuristic_averages = {}
                for word in word_list[:num_words]:
                    guesses = solver.solve(heuristic, word)
                    total_guesses += guesses
                    if heuristic not in heuristic_averages:
                        heuristic_averages[heuristic] = 0
                    heuristic_averages[heuristic] += guesses
                average_guesses = total_guesses / num_words
                print(f"{heuristic} heuristic averaged {average_guesses} guesses for {percentage}% of the word list.")

if __name__ == "__main__":
    main()
