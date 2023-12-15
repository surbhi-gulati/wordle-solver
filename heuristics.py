from collections import Counter
import math

def _get_all_valid_words(word_length: int) -> set[str]:
    """
    Loads and returns the set of all valid words.
    """

    file = str(word_length) + "_letter_words.txt"
    with open(file) as f:
        return set(f.read().splitlines())

def _get_valid_words(word_length, guesses, feedback, used_words):
    """
    Filters the valid words to exclude old guesses and introduces Hard Mode.
    """
        
    valid_words = _get_all_valid_words(word_length)
    for guess, fb in zip(guesses, feedback):
        for i, letter in enumerate(guess):
            # greens
            if fb[i] == 2:
                valid_words = [w for w in valid_words if w[i] == letter]
            # yellows
            elif fb[i] == 1:
                valid_words = [w for w in valid_words if letter in w and w[i] != letter]
            # grays and guessed words
            else:
                valid_words = [w for w in valid_words if letter not in w and w not in used_words]
    return valid_words

# Heuristic 1: Information Gain (modified to penalize used letters)
def information_gain_heuristic(word_length, guesses, feedback, used_words, penalty_factor=0.5):
    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    letter_counts = Counter(letter for word in valid_words for letter in word)
    total_counts = sum(letter_counts.values())
    scores = {letter: (count / total_counts) * math.log2(total_counts / (count + 1))
              for letter, count in letter_counts.items()}
    for word in valid_words:
        score = sum(scores[letter] for letter in word)
        # Penalize words with used letters (adjust penalty as needed)
        score -= penalty_factor * sum(1 for letter in word if letter in used_words)
    return max(valid_words, key=lambda word: score)

# Heuristic 2: Most Frequent Remaining Letters (modified to exclude used words)
def frequent_letters_heuristic(word_length, guesses, feedback, used_words):
    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    letter_counts = Counter(letter for word in valid_words for letter in word)
    letter_scores = {letter: count for letter, count in letter_counts.items() if letter not in used_words}
    return max(valid_words, key=lambda word: sum(letter_scores[letter] for letter in word))

HEURISTICS = {
    "information_gain": information_gain_heuristic,
    "frequent_letters": frequent_letters_heuristic,
}
