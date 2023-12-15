from collections import Counter
import math
import random

def _get_all_valid_words(word_length: int) -> set[str]:
    """
    Loads and returns the set of all valid words for the given word length.

    Args:
        word_length: The length of the desired words.

    Returns:
        A set containing all valid words of the given length.
    """

    file = str(word_length) + "_letter_words.txt"
    with open(file) as f:
        return set(f.read().splitlines())

def _get_valid_words(word_length, guesses, feedback, used_words):
    """
    Filters the remaining valid words based on past guesses and feedback, implementing Hard Mode.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.

    Returns:
        A set containing all valid words remaining under the given constraints.
    """

    valid_words = _get_all_valid_words(word_length)
    for guess, fb in zip(guesses, feedback):
        for i, letter in enumerate(guess):
            # Greens
            if fb[i] == 2:
                valid_words = {w for w in valid_words if w[i] == letter}
            # Yellows
            elif fb[i] == 1:
                valid_words = {w for w in valid_words if letter in w and w[i] != letter}
            # Grays and already guessed words
            else:
                valid_words = {w for w in valid_words if letter not in w and w not in used_words}
    return valid_words


# Heuristic 1: Information Gain (modified to penalize used letters)
def information_gain_heuristic(word_length, guesses, feedback, used_words, penalty_factor=0.5):
    """
    Prioritizes words that maximize information gain based on letter frequencies, penalizing used letters.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.
        penalty_factor: The weight for penalizing used letters (adjust as needed).

    Returns:
        The word with the highest information gain score among the remaining valid words.
    """

    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    letter_counts = Counter(letter for word in valid_words for letter in word)
    total_counts = sum(letter_counts.values())
    scores = {
        letter: (count / total_counts) * math.log2(total_counts / (count + 1))
        for letter, count in letter_counts.items()
    }
    for word in valid_words:
        score = sum(scores[letter] for letter in word)
        # Penalize words with used letters
        score -= penalty_factor * sum(1 for letter in word if letter in used_words)
    return max(valid_words, key=lambda word: score)


# Heuristic 2: Most Frequent Remaining Letters (modified to exclude used words)
def frequent_letters_heuristic(word_length, guesses, feedback, used_words):
    """
    Prioritizes words containing the most frequent remaining letters, excluding already used ones.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.

    Returns:
        The word with the highest score based on the remaining letter frequencies, excluding used letters.
    """

    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    letter_counts = Counter(letter for word in valid_words for letter in word)
    letter_scores = {letter: count for letter, count in letter_counts.items() if letter not in used_words}
    return max(valid_words, key=lambda word: sum(letter_scores[letter] for letter in word))

# Heuristic 3: Positional Information Gain
def positional_information_gain_heuristic(word_length, guesses, feedback, used_words):
    """
    Prioritizes words where informative letters appear in more likely positions, based on their remaining frequency.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.

    Returns:
        The word with the highest score based on the position-weighted information gain of its letters.
    """

    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    letter_counts = Counter(letter for word in valid_words for letter in word)
    total_counts = sum(letter_counts.values())
    position_weights = {i: math.log2(word_length - i + 1) for i in range(word_length)}
    scores = {letter: 0 for letter in letter_counts}
    for word in valid_words:
        for i, letter in enumerate(word):
            scores[letter] += position_weights[i] * (letter_counts[letter] / total_counts) * math.log2(total_counts / (letter_counts[letter] + 1))
    return max(valid_words, key=lambda word: sum(scores[letter] for letter in word))


# Heuristic 4: Double Letter Prioritization
def double_letter_heuristic(word_length, guesses, feedback, used_words):
    """
    Prioritizes words containing double letters, as they potentially reveal more information and eliminate possibilities.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.

    Returns:
        The word with the highest score based on the number of double letters it contains.
    """

    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    double_letter_counts = Counter(letter * 2 for word in valid_words for letter in word)
    scores = {word: double_letter_counts.get(word, 0) for word in valid_words}
    return max(valid_words, key=lambda word: scores[word])


# Heuristic 5: Vowel Frequency
def vowel_frequency_heuristic(word_length, guesses, feedback, used_words):
    """
    Prioritizes words with higher vowel content, as vowels are statistically more common and informative.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.

    Returns:
        The word with the highest score based on the number of vowels it contains.
    """

    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    vowels = "aeiou"
    vowel_counts = Counter(letter for word in valid_words for letter in word if letter in vowels)
    scores = {word: vowel_counts.get(word, 0) for word in valid_words}
    return max(valid_words, key=lambda word: scores[word])

def get_feedback(guess, answer):
    """
    Calculates the feedback for a guessed word based on the actual answer.

    Args:
        guess: The word guessed by the player.
        answer: The actual Wordle answer.

    Returns:
        A list of integers representing the feedback for each letter:
            2 - green (correct position),
            1 - yellow (present elsewhere),
            0 - gray (absent).
    """

    feedback = [0] * len(guess)
    for i, letter in enumerate(guess):
        if letter == answer[i]:
            feedback[i] = 2
        elif letter in answer:
            feedback[i] = 1
    return feedback

# Heuristic 6: Entropy-Based Elimination
def entropy_based_elimination_heuristic(word_length, guesses, feedback, used_words):
    """
    Prioritizes words that eliminate the most remaining possibilities based on the current information and entropy.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.

    Returns:
        The word that eliminates the most remaining valid words based on its feedback, maximizing the reduction in entropy.
    """

    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    initial_entropy = math.log2(len(valid_words))
    scores = {word: 0 for word in valid_words}
    for word in valid_words:
        remaining_words = _get_valid_words(word_length, guesses + [word], feedback + [get_feedback(word)], used_words)
        remaining_entropy = math.log2(len(remaining_words))
        scores[word] = initial_entropy - remaining_entropy
    return max(valid_words, key=lambda word: scores[word])

# Heuristic 7: Word Pair Exclusion
def word_pair_exclusion_heuristic(word_length, guesses, feedback, used_words):
    """
    Prioritizes words that eliminate pairs of possible solutions based on their feedback, reducing uncertainty.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.

    Returns:
        The word that eliminates the most pairs of possible solutions based on its feedback, aiding in faster convergence.
    """

    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    pair_scores = {word: 0 for word in valid_words}
    for word1 in valid_words:
        for word2 in valid_words:
            if word1 != word2 and get_feedback(word1) != get_feedback(word2):
                pair_scores[word1] += 1
    return max(valid_words, key=lambda word: pair_scores[word])

# Random Guesser Function (implements Hard Mode constraints)
def random_guesser_function(word_length, guesses, feedback, used_words):
    """
    Randomly selects a valid word from the remaining options, enforcing Hard Mode rules.

    Args:
        word_length: The length of the desired words.
        guesses: A list of previously guessed words.
        feedback: A list of feedback values (2 - green, 1 - yellow, 0 - gray) for each guess.
        used_words: A set of words already used in guesses.

    Returns:
        A randomly chosen word from the remaining valid options, adhering to Hard Mode rules.
    """

    valid_words = _get_valid_words(word_length, guesses, feedback, used_words)
    return random.choice(list(valid_words))

HEURISTICS = {
    "information_gain": information_gain_heuristic,
    "frequent_letters": frequent_letters_heuristic,
    "positional_information_gain": positional_information_gain_heuristic,
    "double_letter": double_letter_heuristic,
    "vowel_frequency": vowel_frequency_heuristic,
    "entropy_based_elimination_heuristic": entropy_based_elimination_heuristic,
    "word_pair_exclusion_heuristic": word_pair_exclusion_heuristic,
    "random_guesser_function": random_guesser_function,
}
