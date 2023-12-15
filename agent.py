import random
from wordle_solver import WordleSolver
from heuristics import HEURISTICS
from random import choice
from statistics import mean, stdev
import argparse

def choose_word_length(args):
    """
    Validate and return chosen word length.
    """
    if args.word_length not in (5, 6, 7):
        raise ValueError(f"Invalid word length: {args.word_length}")
    return args.word_length

def choose_heuristic(args, heuristics):
    """
    Parse and validate heuristic.
    """
    try:
        index = int(args.heuristic_number) - 1
        if 0 <= index < len(heuristics):
            return list(heuristics.values())[index]
        else:
            raise ValueError
    except ValueError:
        if args.heuristic_number not in heuristics:
            raise ValueError(f"Invalid heuristic: {args.heuristic_number}")
        return heuristics[args.heuristic_number]

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

def analyze_comparison_mode(word_length, percentage, heuristics):
    """
    Run comparison mode analysis for all heuristics on a chosen percentage of words.
    """
    word_list = load_word_list(word_length)
    # Calculate number of words to analyze
    num_words = int(len(word_list) * percentage / 100)
    # Randomly select the sub-list of words
    chosen_words = random.sample(word_list, num_words)

    # Initialize data structures
    heuristic_averages = {}
    best_heuristic = None
    best_average = float('inf')

    for name, heuristic in HEURISTICS.items():
        solver = WordleSolver(word_length, [heuristic])
        total_guesses = 0
        for word in chosen_words:
            guesses = solver.solve(heuristic, word)
            total_guesses += guesses
        # Calculate average guesses for this heuristic
        heuristic_averages[heuristic] = total_guesses / len(chosen_words)
        # Update best heuristic if this average is lower
        if heuristic_averages[heuristic] < best_average:
            best_heuristic = heuristic
            best_average = heuristic_averages[heuristic]

    # Print overall results for each heuristic
    for heuristic, average in heuristic_averages.items():
        min_guesses = min(heuristic_averages.values(), key=min)
        max_guesses = max(heuristic_averages.values(), key=max)
        std_dev = stdev(list(heuristic_averages.values()))
        print(f"{heuristic.__name__} heuristic:")
        print(f"- Average guesses: {average:.2f}")
        print(f"- Minimum guesses: {min_guesses}")
        print(f"- Maximum guesses: {max_guesses}")
        print(f"- Standard deviation: {std_dev:.2f}")

    # Print the best performing heuristic
    print(f"\nBest heuristic by average guesses: {best_heuristic.__name__}")

def load_word_list(word_length):
    """
    Load words from the specified word length file.
    """
    with open(f"{word_length}_letter_words.txt", "r") as f:
        return f.read().splitlines()

def main():
    """
    Runs analysis based on command line arguments.
    """
    parser = argparse.ArgumentParser(description="Wordle Heuristic Analysis")
    parser.add_argument("word_length", type=int, choices=[5, 6, 7], help="Length of Wordle words")
    parser.add_argument("heuristic_number", help="Index or name of the heuristic to analyze")
    parser.add_argument("--comparison", action="store_true", help="Run comparison mode for all heuristics")
    parser.add_argument("--percent", type=float, default=50, help="Percentage of word list to analyze (default: 50%)")
    args = parser.parse_args()

    try:
        word_length = choose_word_length(args)
        heuristic = choose_heuristic(args, HEURISTICS)

        if args.comparison:
            # Run comparison mode for all heuristics with chosen percentage
            analyze_comparison_mode(word_length, args.percent, HEURISTICS)
        else:
            # Run single-word analysis for the chosen heuristic
            analyze_single_heuristic(word_length, heuristic)
    except ValueError as e:
        print(f"Error: {e}")
        parser.print_usage()

if __name__ == "__main__":
    main()
