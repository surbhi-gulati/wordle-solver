import argparse
import random

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--word_length", type=int, default=5, choices=[5, 6, 7],
                    help="Length of the Wordle game (5, 6, or 7)")
  args = parser.parse_args()
  return args

def load_words(word_length):
  with open(f"{word_length}_letter_words.txt") as f:
    words = [word.lower() for word in f.read().splitlines()]
  return words

def check_guess(guess, secret):
  green, yellow, gray = [], [], []
  for i, (g, s) in enumerate(zip(guess, secret)):
    if g == s:
      green.append(i)
    elif g in secret and g != s:
      yellow.append(i)
    else:
      gray.append(i)
  return green, yellow, gray

# Define base heuristic (most frequent letter)
def base_heuristic(word_list, state):
  letter_counts = {}
  for word in word_list:
    for i, letter in enumerate(word):
      if i not in state["greens"] and i not in state["yellows"]:
        letter_counts.setdefault(letter, 0)
        letter_counts[letter] += 1
  return max(letter_counts, key=letter_counts.get)

# Function to choose a guess based on a heuristic
def choose_guess(word_list, state, heuristic=base_heuristic):
  remaining_words = {word for word in word_list if all(
    letter not in word for letter, indices in (list(state["grays"].items()))
    for index in indices) and all(
        word[i] not in word for i in state["greens"])}
  return heuristic(remaining_words, state)

# Main game loop
def play_wordle(word_length):
  word_list = load_words(word_length)
  secret = random.choice(word_list)
  state = {
      "greens": [],
      "yellows": [],
      "grays": set(),
      "guesses_left": word_length + 1,
  }
  for _ in range(state["guesses_left"]):
    guess = choose_guess(word_list, state)
    print(f"Guess {state['guesses_left']}: {guess}")
    green, yellow, gray = check_guess(guess, secret)
    state["greens"].extend(green)
    state["yellows"].extend(yellow)
    state["grays"].update(gray)
    state["guesses_left"] -= 1
    if all(i in state["greens"] for i in range(word_length)):
      print(f"You won!  Secret word was {secret}")
      break
  else:
    print(f"You lost!  Secret word was {secret}")
    print(f"Total guesses: {state['guesses_left']}")

if __name__ == "__main__":
  args = parse_args()
  play_wordle(args.word_length)
