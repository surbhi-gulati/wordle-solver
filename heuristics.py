from typing import List, Set, Counter
from collections import Counter
import math

def _get_all_valid_words(word_length: int) -> Set[str]:
    """
    Loads and returns the set of all valid words.
    """

    file = str(word_length) + "_letter_words.txt"
    with open(file) as f:
        return set(f.read().splitlines())

def _get_valid_words(word_length: int, guesses: List[str] = None, feedback: List[List[int]] = None):
    """
    Filters valid words based on past guesses and feedback.

    Args:
        word_length: The length of the word to guess.
        guesses: (Optional) List of past guesses.
        feedback: (Optional) List of feedback for each guess.

    Returns:
        A set of valid words that are consistent with the provided information.
    """
    if guesses is None:
        guesses = []
    if feedback is None:
        feedback = []

    valid_words = set(_get_all_valid_words(word_length))
    # Exclude words containing any letters already used in guesses
    for guess in guesses:
        valid_words -= set(guess)
    # Filter out remaining words based on feedback (green and gray)
    for guess, fb in zip(guesses, feedback):
        for i, (letter, fb_value) in enumerate(zip(guess, fb)):
            if fb_value == 2:  # Green: letter in correct position
                valid_words = {word for word in valid_words if word[i] == letter}
    return valid_words

def _letter_frequency(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic based on letter frequency, excluding used letters.
    """
    # Count letter occurrences, excluding used letters
    letter_counts = Counter()
    for word in guesses:
        letter_counts.update(set(word) - set(guess for guess in guesses))

    # Prioritize words with most frequent unused letters
    valid_words = _get_valid_words(word_length, guesses, feedback)
    return max(valid_words, key=lambda word: sum(letter_counts[letter] for letter in word))

def _letter_position_information(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic based on letter position information from feedback.
    """

    # Collect information from feedback
    known_positions = [[] for _ in range(word_length)]
    possible_positions = set()
    excluded_letters = set()
    for guess, fb in zip(guesses, feedback):
        for i, (letter, fb_value) in enumerate(zip(guess, fb)):
            if fb_value == 2:  # green: letter in correct position
                known_positions[i].append(letter)
            elif fb_value == 1:  # yellow: letter in word but wrong position
                possible_positions.add(letter)
            else:  # gray: letter not in word
                excluded_letters.add(letter)

    # Prioritize words that fulfill known positions and avoid excluded letters
    valid_words = _get_valid_words(word_length, guesses, feedback)
    scored_words = []
    for word in valid_words:
        score = 0
        for i, letter in enumerate(word):
            if letter in known_positions[i]:
                score += 3
            elif letter not in excluded_letters and letter in possible_positions:
                score += 1
        scored_words.append((score, word))

    return max(scored_words, key=lambda x: x[0])[1]


def _word_entropy(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic based on word entropy to maximize information gain.
    """

    # Calculate entropy for each possible state
    entropies = {}
    for word in _get_valid_words(word_length, guesses, feedback):
        states = _get_possible_states(word, guesses, feedback)
        entropy = sum(
            -len(state) * math.log2(len(state))
            for state in states
            if len(state) > 0
        )
        entropies[word] = entropy

    # Return the word with the highest entropy
    return max(entropies.items(), key=lambda item: item[1])[0]

def _maximize_elimination(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic that maximizes the number of words eliminated per guess.
    """

    # Calculate the number of words eliminated for each possible guess
    elimination_counts = {}
    for word in _get_valid_words(word_length, guesses, feedback):
        eliminated_words = _get_eliminated_words(word_length, word, guesses, feedback)
        elimination_counts[word] = len(eliminated_words)

    # Return the word that eliminates the most words
    return max(elimination_counts.items(), key=lambda item: item[1])[0]

def _fulfill_known_positions(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic that prioritizes fulfilling known positions from feedback.
    """

    # Count occurrences of letters in known positions
    known_letter_counts = Counter()
    for guess, fb in zip(guesses, feedback):
        for i, (letter, fb_value) in enumerate(zip(guess, fb)):
            if fb_value == 2:
                known_letter_counts[letter] += 1

    # Prioritize words that fulfill the most known positions
    valid_words = _get_valid_words(word_length, guesses, feedback)
    scored_words = []
    for word in valid_words:
        score = 0
        fulfilled_positions = set()
        for i, (letter, fb_value) in enumerate(zip(word, feedback)):
            if fb_value == 2:
                score += 1
                fulfilled_positions.add(i)
        for i, letter in enumerate(word):
            if i in fulfilled_positions:
                continue
            if known_letter_counts[letter] > 0:
                score += 0.5
        scored_words.append((score, word))

    return max(scored_words, key=lambda x: x[0])[1]

def _consider_remaining_letters(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic that ensures the guess contains potential remaining letters.
    """

    # Collect possible letters from feedback
    possible_letters = set()
    for guess, fb in zip(guesses, feedback):
        for i, (letter, fb_value) in enumerate(zip(guess, fb)):
            if fb_value == 1 or fb_value == 2:
                possible_letters.add(letter)

    # Prioritize words that contain the most possible remaining letters
    valid_words = _get_valid_words(word_length, guesses, feedback)
    scored_words = []
    for word in valid_words:
        score = sum(1 for letter in word if letter in possible_letters)
        scored_words.append((score, word))

    return max(scored_words, key=lambda x: x[0])[1]


def _minimize_invalid_combinations(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic that avoids invalid letter combinations based on feedback.
    """

    # Analyze feedback to identify forbidden letter combinations
    invalid_combinations = set()
    for i, guess in enumerate(guesses):
        for j, letter in enumerate(guess):
            if feedback[i][j] == 0:  # gray: letter not in word
                other_letters = guess[j + 1:]
                for other_letter in other_letters:
                    invalid_combinations.add((letter, other_letter))

    # Prioritize words that avoid invalid combinations
    valid_words = _get_valid_words(word_length, guesses, feedback)
    scored_words = []
    for word in valid_words:
        score = len(word)  # higher score means fewer invalid combinations
        for i, letter in enumerate(word):
            for other_letter in word[i + 1:]:
                if (letter, other_letter) in invalid_combinations:
                    score -= 1
        scored_words.append((score, word))

    return max(scored_words, key=lambda x: x[0])[1]

def _calculate_entropy(words: Set[str]):
    """
    Calculates the entropy of a set of words.

    Args:
        words: Set of valid words.

    Returns:
        Entropy of words.
    """

    word_counts = Counter(words)
    entropy = 0
    for count in word_counts.values():
        probability = count / len(words)
        entropy += -probability * math.log2(probability)
    return entropy

def _calculate_information_gain(word_length: int, word: str, guesses: List[str], feedback: List[List[int]]):
    """
    Calculates the information gain of a given word as a guess.

    Args:
        word: Newest guess to evaluate.
        guesses: All past guesses.
        feedback: Feedback per guess.

    Returns:
        The information gain of the word.
    """

    # Collect possible states after the guess
    states = _get_possible_states(word, guesses, feedback)

    # Calculate entropy with and without the current guess
    entropy_without_guess = _calculate_entropy(_get_all_valid_words(word_length))
    entropy_with_guess = sum(
        len(state) * _calculate_entropy(state) for state in states
    )

    # Information gain is the reduction in entropy from making the guess
    information_gain = entropy_without_guess - entropy_with_guess
    return information_gain

def _start_high_information(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic that prioritizes informative guesses early on.
    """

    # Calculate the information gain for each possible guess
    information_gains = {}
    for word in _get_valid_words(word_length, guesses, feedback):
        information_gains[word] = _calculate_information_gain(word_length, word, guesses, feedback)

    # Return the word with the highest information gain
    return max(information_gains.items(), key=lambda item: item[1])[0]

def _diversify_guesses(word_length: int, guesses: List[str], feedback: List[List[int]]):
    """
    Heuristic that avoids repeating letters and positions from past failures.
    """

    # Collect used letters and positions from past guesses
    used_letters = set()
    used_positions = set()
    for guess in guesses:
        for i, letter in enumerate(guess):
            used_letters.add(letter)
            used_positions.add((i, letter))

    # Prioritize words with unique letters and positions not used in past failures
    valid_words = _get_valid_words(word_length, guesses, feedback)
    scored_words = []
    for word in valid_words:
        score = 0
        for i, letter in enumerate(word):
            if letter not in used_letters and (i, letter) not in used_positions:
                score += 1
        scored_words.append((score, word))

    return max(scored_words, key=lambda x: x[0])[1]

def _get_possible_states(word: str, guesses: List[str], feedback: List[List[int]]):
    """
    Generates all possible states of the target word after making a guess.

    Args:
        word: Newest guess to evaluate.
        guesses: All past guesses.
        feedback: Feedback per guess.

    Returns:
        List of sets representing a possible state of the target word.
    """

    states = []
    for i, (letter, fb_value) in enumerate(zip(word, feedback)):
        if fb_value == 2:  # green: letter in correct position
            new_states = []
            for state in states:
                if state[i] == letter:
                    new_states.append(state)
                else:
                    new_state = state.copy()
                    new_state[i] = letter
                    new_states.append(new_state)
            states = new_states
        elif fb_value == 1:  # yellow: letter in word but wrong position
            new_states = []
            for state in states:
                if state[i] == letter:
                    continue
                else:
                    new_state = state.copy()
                    new_state[i] = None
                    new_states.append(new_state)
            states = new_states
    return states

def _get_eliminated_words(word_length: int, word: str, guesses: List[str], feedback: List[List[int]]):
    """
    Determines which words are eliminated based on a guess + feedback on the guess.

    Args:
        word: Newest guess to evaluate.
        guesses: All past guesses.
        feedback: Feedback per guess.

    Returns:
        Eliminated word subset of potential target words.
    """

    eliminated_words = set()
    for guess, fb in zip(guesses, feedback):
        for _, (letter, fb_value) in enumerate(zip(guess, fb)):
            if fb_value == 0:  # gray: letter not in word
                for other_word in _get_all_valid_words(word_length):
                    if letter in other_word:
                        eliminated_words.add(other_word)
    return eliminated_words

# Heuristic functions: a dictionary mapping heuristic names to their corresponding functions
HEURISTICS = {
    "letter_frequency": _letter_frequency,
    "letter_position_information": _letter_position_information,
    "word_entropy": _word_entropy,
    "maximize_elimination": _maximize_elimination,
    "fulfill_known_positions": _fulfill_known_positions,
    "consider_remaining_letters": _consider_remaining_letters,
    "minimize_invalid_combinations": _minimize_invalid_combinations,
    "start_high_information": _start_high_information,
    "diversify_guesses": _diversify_guesses,
}
