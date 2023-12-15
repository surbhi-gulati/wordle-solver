import random
from wordle_solver import WordleSolver
from heuristics import HEURISTICS
from random import choice
from statistics import mean, stdev
import argparse

def choose_word_length(args):
    """
    Validate and return chosen word length of 5, 6, or 7.
    """
    if args.word_length not in (5, 6, 7):
        raise ValueError(f"Invalid word length: {args.word_length}")
    return args.word_length

def choose_heuristic(args, heuristics):
    """
    Parse and validate heuristic for single analysis.
    """
    try:
        # Validate heuristic number within range and return the heuristic name
        if args.heuristic:
            if not (1 <= args.heuristic <= len(heuristics)):
                raise ValueError("Invalid heuristic number. Choose between 1 and 8.")
            index = args.heuristic - 1
            return list(heuristics.values())[index]
        # No heuristic need be chosen for comparison mode
        else:
            if args.comparison:
                return None
            raise ValueError("Heuristic number required for single-word analysis.")
    except ValueError as e:
        raise ValueError(f"Invalid heuristic: {e}") from e

def analyze_single_heuristic(word_length, heuristic):
    """
    Run single-word analysis for a chosen heuristic.
    """
    word_list = load_word_list(word_length)
    secret_word = choice(word_list)
    solver = WordleSolver(word_length, [heuristic])
    guesses = solver.solve(heuristic, secret_word)
    print(f"Heuristic: {heuristic.__name__}")
    print(f"Secret word: {secret_word}")
    print(f"Guesses made: {guesses} / {word_length + 1}")

def analyze_comparison_mode(word_length, percentage):
    """
    Run comparison mode analysis for all heuristics on a chosen percentage of words.
    """
    # Randomly select the percentage given from the word list of word_length
    word_list = load_word_list(word_length)
    num_words = int(len(word_list) * percentage / 100)
    chosen_words = random.sample(word_list, num_words)

    # Collect guess counts of each heuristic on each word of the chosen sub-list
    heuristic_averages = {}
    for name, _ in HEURISTICS.items():
        heuristic_averages[name] = 0
        heuristic = HEURISTICS[name]
        for word in chosen_words:
            solver = WordleSolver(word_length, [heuristic])
            guesses = solver.solve(heuristic, word)
            heuristic_averages[name] += guesses

        # Calculate and print average guesses for each heuristic
        for name, total_guesses in heuristic_averages.items():
            average = total_guesses / len(chosen_words)
            print(f"{name} heuristic: Average guesses: {average:.2f}")

    # Find and print the best performing heuristic
    best_average = min(heuristic_averages.values())
    best_heuristic = [name for name, average in heuristic_averages.items() if average == best_average][0]
    print(f"\nBest performing heuristic: {best_heuristic}")

def load_word_list(word_length):
    """
    Load words from the specified word length file.
    """
    with open(f"{word_length}_letter_words.txt", "r") as f:
        return f.read().splitlines()

def main():
    """
    Runs analysis based on command line arguments.
    Accepts word_length + single heuristic analysis with heuristic number, 
    or comparison analysis + percentage of word list to analyze against all 8 heuristics.
    """
    parser = argparse.ArgumentParser(description="Wordle Heuristic Analysis")
    parser.add_argument("word_length", type=int, choices=[5, 6, 7], help="Length of Wordle words")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--heuristic", type=int, help="Heuristic number for single analysis (1-8)")
    group.add_argument("--comparison", action="store_true", help="Run comparison mode for all heuristics with chosen percentage")
    parser.add_argument("--percent", type=float, default=50, help="Percentage of word list to analyze (default: 50%)")
    args = parser.parse_args()

    try:
        if args.heuristic:
            # Validate heuristic number within range
            if not (1 <= args.heuristic <= len(HEURISTICS)):
                raise ValueError("Invalid heuristic number. Choose between 1 and 8.")
            heuristic = choose_heuristic(args, HEURISTICS)
            analyze_single_heuristic(args.word_length, heuristic)
        elif args.comparison:
            # Validate percentage within range
            if not (0 <= args.percent <= 100):
                raise ValueError("Invalid percentage. Enter a value between 0 and 100.")
            analyze_comparison_mode(args.word_length, args.percent)
        else:
            raise ValueError("Please specify either --heuristic or --comparison --percent")
    except ValueError as e:
        print(f"Error: {e}")
        parser.print_usage()

if __name__ == "__main__":
    main()
