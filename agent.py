import logging
import random
from typing import Dict

from wordle_solver import WordleSolver
from heuristics import HEURISTICS


def user_input():
    """
    Collect user input for desired analysis mode, word length, and (for multi-word) percentage.

    This function now uses numbered options and handles both numerical and text-based user input.
    """

    logging.info("Choose analysis mode:")

    analysis_choices = {
        1: "Single Heuristic",
        2: "All Heuristics (Comparison Mode)",
    }

    for number, choice in analysis_choices.items():
        print(f"{number}. {choice}")

    user_choice = input("> ")

    try:
        # Try parsing user input as integer
        analysis_choice = int(user_choice)
    except ValueError:
        # Treat input as text if parsing as integer fails
        analysis_choice_text = user_choice.lower().strip()
        for number, choice in analysis_choices.items():
            if choice.lower().strip() == analysis_choice_text:
                analysis_choice = number
                break
        else:
            print(f"Invalid choice: '{user_choice}'. Please enter a valid number: 1 or 2.")
            exit(1)

    # Validate chosen analysis mode
    if analysis_choice not in analysis_choices:
        print(f"Invalid choice: {analysis_choice}. Please enter a valid number: 1 or 2.")
        exit(1)

    analysis_mode = analysis_choices[analysis_choice]

    if analysis_mode == "Single Heuristic":
        # Single heuristic mode, choose heuristic and word length

        logging.info("Choose desired heuristic:")
        for heuristic_name in HEURISTICS.keys():
            print(f"- {heuristic_name}")

        heuristic_choice = input("> ")

        word_length = int(input("Enter your desired word length (5 | 6 | 7): "))

        # Ask single or multi-word analysis
        logging.info("Choose operation:")
        single_multi_choices = {
            1: "Single Word",
            2: "Multi-Word with percentage",
        }

        for number, choice in single_multi_choices.items():
            print(f"{number}. {choice}")

        single_multi_choice = input("> ")

        try:
            single_multi_choice = int(single_multi_choice)
        except ValueError:
            # Treat input as text if parsing as integer fails
            single_multi_choice_text = single_multi_choice.lower().strip()
            for number, choice in single_multi_choices.items():
                if choice.lower().strip() == single_multi_choice_text:
                    single_multi_choice = number
                    break
            else:
                print(f"Invalid choice: '{single_multi_choice}'. Please enter a valid number: 1 or 2.")
                exit(1)

        # Validate chosen single/multi-word mode
        if single_multi_choice not in single_multi_choices:
            print(f"Invalid choice: {single_multi_choice}. Please enter a valid number: 1 or 2.")
            exit(1)

        single_or_multi_mode = single_multi_choices[single_multi_choice]

        if single_or_multi_mode == "Single Word":
            # Single word analysis, select one random word
            logging.info("Selecting a random word from the list...")
            word_list = random.choice(load_word_list(word_length))
        else:
            # Multi-word analysis
            percentage = validate_percentage(input("Enter percentage of word list to use (1-100): "))
            word_list = load_word_list(word_length, percentage)

    else:
        # Comparison mode, use all available heuristics
        word_length = int(input("Enter your desired word length (5 | 6 | 7): "))

        # Set appropriate defaults for comparison mode
        analysis_mode = "All Heuristics (Comparison Mode)"
        heuristic_choice = None
        word_list = None

    return analysis_mode, heuristic_choice, word_length, word_list

def validate_percentage(percentage_str):
    """Validate and convert percentage input."""
    try:
        percentage = float(percentage_str)
        if 1 <= percentage <= 100:
            return percentage / 100  # Convert to a value between 0 and 1
        else:
            print("Error: Percentage must be between 1 and 100.")
            exit(1)
    except ValueError:
        print("Error: Invalid percentage input.")
        exit(1)


def load_word_list(word_length, percentage=None):
    """Load word list based on word length and optionally extract random items."""
    word_list_file = f"{word_length}_letter_words.txt"
    logging.info(f"Loading word list from {word_list_file}...")
    with open(word_list_file, "r") as f:
        word_list = [line.strip() for line in f.readlines()]

    if percentage is None:
        return word_list

    # Multi-word analysis, extract a random subset of words based on percentage
    logging.info(f"Extracting {percentage * 100}% of the words...")
    random_index_list = random.sample(range(len(word_list)), int(len(word_list) * percentage))
    return [word_list[i] for i in random_index_list]


def run_heuristic_analysis(analysis_mode, heuristic_choice, word_length, word_list):
    """Run analysis based on the chosen mode."""

    logging.info(f"Starting analysis with mode '{analysis_mode}'...")

    solver = WordleSolver(word_length)

    # Single heuristic analysis
    if analysis_mode == "Single Heuristic":
        total_guesses = solver.solve(heuristic_choice, word_list)
        num_words_analyzed = len(word_list)
        print(f"\nAnalysis completed with heuristic '{heuristic_choice}':")
        print(f"{num_words_analyzed} words analyzed.")

        if num_words_analyzed > 0:
            average_guesses = total_guesses / num_words_analyzed
            print(f"Average number of guesses: {average_guesses:.2f}")

    # Multi-word analysis (single or all heuristics)
    elif analysis_mode in ("Multi-Word with percentage", "All Heuristics (Comparison Mode)"):
        total_guesses = 0
        num_words_analyzed = len(word_list)

        if analysis_mode == "Multi-Word with percentage":
            for word in word_list:
                total_guesses += solver.solve(heuristic_choice, word)

        elif analysis_mode == "All Heuristics (Comparison Mode)":
            heuristic_results = {}
            for heuristic_name, heuristic_function in HEURISTICS.items():
                guesses = 0
                for word in word_list:
                    guesses += solver.solve(heuristic_name, word)
                guesses /= len(word_list)
                heuristic_results[heuristic_name] = guesses

            print("**Comparison of Heuristics:**")
            print("| Heuristic | Average Guesses |")
            print("|---|---|")
            for heuristic_name, average_guesses in heuristic_results.items():
                print(f"| {heuristic_name} | {average_guesses:.2f} |")

        print(f"\nAnalysis completed with {analysis_mode}:")
        print(f"{num_words_analyzed} words analyzed.")

        if num_words_analyzed > 0:
            print("TOTAL GUESSES" + total_guesses)
            print("NUM WORDS ANALYZED" + num_words_analyzed)
            average_guesses = float(total_guesses) / float(num_words_analyzed)
            print(f"Average number of guesses: {average_guesses:.2f}")

    else:
        print("Invalid analysis mode. Please try again.")


def main():
    """Main function of the Wordle Solver Agent."""
    logging.basicConfig(level=logging.INFO)

    try:
        analysis_mode, heuristic_choice, word_length, word_list = user_input()
        run_heuristic_analysis(analysis_mode, heuristic_choice, word_length, word_list)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
