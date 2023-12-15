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
    if args.heuristic:
      # Validate heuristic number within range
      if not (1 <= args.heuristic <= len(heuristics)):
        raise ValueError("Invalid heuristic number. Choose between 1 and 8.")
      index = args.heuristic - 1
      return list(heuristics.values())[index]
    else:
      if args.comparison:
        return None  # No heuristic needed for comparison mode
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
  for name, _ in HEURISTICS.items():
    heuristic_averages[name] = 0

  for word in chosen_words:
    for name, heuristic in HEURISTICS.items():
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
      analyze_comparison_mode(args.word_length, args.percent, HEURISTICS)
    else:
      raise ValueError("Please specify either --heuristic or --comparison")
  except ValueError as e:
    print(f"Error: {e}")
    parser.print_usage()

if __name__ == "__main__":
  main()
