from wordle_solver import WordleSolver
from heuristics import HEURISTICS

def choose_word_length():
    """
    Prompts the user to choose a word length and validates their input.

    Returns:
        The chosen word length (5, 6, or 7).
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
        word_length: The chosen word length.

    Returns:
        A list of words with the specified length.
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
    Allows user to choose a single heuristic by name or number.

    Args:
        heuristics: A dictionary of available heuristics.

    Returns:
        The chosen heuristic function.
    """
    while True:
        choice = input("Enter the name or number of the heuristic you want to use (e.g., 1, letter_frequency, etc.): ")
        try:
            # Try to interpret choice as an integer (index)
            index = int(choice) - 1
            if 0 <= index < len(heuristics):
                if callable(list(heuristics.values())[index]):
                    return list(heuristics.values())[index]
                else:
                    print(f"Invalid heuristic function. Please choose from the available options: {', '.join(heuristics.keys())}")
            else:
                print(f"Invalid heuristic index. Please choose from the available options: {', '.join(heuristics.keys())}")
        except ValueError:
            # If not an integer, try to match the heuristic name
            if choice in heuristics:
                if callable(heuristics[choice]):
                    return heuristics[choice]
                else:
                    print(f"Invalid heuristic function. Please choose from the available options: {', '.join(heuristics.keys())}")
            else:
                print(f"Invalid heuristic name. Please choose from the available options: {', '.join(heuristics.keys())}")

def choose_word_list_size():
    """
    Prompts the user to choose a word list size and validates their input.

    Returns:
        "single" if the user chooses a single word,
        "multi" if the user chooses a percentage of the word list.
    """
    while True:
        choice = input("Choose a word list size: \n"
                       "1. Single Word\n"
                       "2. Multi-Word (Percentage)\n").lower()
        if choice in ("1", "single word"):
            return "single"
        elif choice in ("2", "multi-word", "percentage"):
            return "multi"
        else:
            print("Invalid choice. Please try again.")


def choose_percentage():
    """
    Prompts the user to enter a percentage and validates their input.

    Returns:
        The chosen percentage as a float between 0 and 100.
    """
    while True:
        try:
            percentage = float(input("Enter percentage (0-100): "))
            if 0 <= percentage <= 100:
                return percentage
            else:
                print("Invalid percentage. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    # Choose word length and word list
    word_length = choose_word_length()
    word_list = choose_word_list(word_length)

    # Choose heuristic mode
    heuristic_mode = choose_heuristic_mode()

    if heuristic_mode == "single":
        # Choose single heuristic and word list
        heuristic = choose_single_heuristic(HEURISTICS)
        word_list_size = choose_word_list_size()

        if word_list_size == "single":
            # Solve for a single secret word
            word = input("Enter a secret word: ")
            solver = WordleSolver(word_length, [heuristic])
            guesses = solver.solve(heuristic, word)
            print(f"Word solved in {guesses} guesses using {heuristic} heuristic.")
        else:
            # Solve for a percentage of the word list
            percentage = choose_percentage()
            num_words = int(len(word_list) * percentage / 100)
            solver = WordleSolver(word_length, [heuristic])
            total_guesses = 0
            for word in word_list[:num_words]:
                guesses = solver.solve(heuristic, word)
                total_guesses += guesses
            average_guesses = total_guesses / num_words
            print(f"Average guesses for {percentage}% of the word list using {heuristic} heuristic: {average_guesses}")
    else:
        # Run comparison mode for all heuristics
        word_list_size = choose_word_list_size()

        if word_list_size == "single":
            # Compare all heuristics for a single secret word
            word = input("Enter a secret word: ")
            for heuristic in HEURISTICS:
                solver = WordleSolver(word_length, [heuristic])
                guesses = solver.solve(heuristic, word)
                print(f"{heuristic} heuristic solved the word in {guesses} guesses.")
        else:
            # Compare all heuristics for a percentage of the word list
            percentage = choose_percentage()
            num_words = int(len(word_list) * percentage / 100)
            for heuristic in HEURISTICS:
                solver = WordleSolver(word_length, [heuristic])
                total_guesses = 0
                for word in word_list[:num_words]:
                    guesses = solver.solve(heuristic, word)
                    total_guesses += guesses
                average_guesses = total_guesses / num_words
                print(f"{heuristic} heuristic averaged {average_guesses} guesses for {percentage}% of the word list.")


if __name__ == "__main__":
    main()
