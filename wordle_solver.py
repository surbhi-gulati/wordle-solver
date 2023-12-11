from typing import Dict, List
from heuristics import HEURISTICS


class WordleSolver:
    def __init__(self, word_length: int):
        self.word_length = word_length

    def solve(self, heuristic: str, target_word: str) -> int:
        """Solves the Wordle game for a given target word and heuristic."""
        # Validate heuristic
        if heuristic not in HEURISTICS:
            raise ValueError(f"Invalid heuristic: {heuristic}")

        # Initialize variables
        guesses = 0
        current_state = ""
        feedback = {letter: None for letter in range(self.word_length)}

        # Loop while the solution hasn't been found
        all_positions_updated = False
        while current_state != target_word and not all_positions_updated:
            # Generate next guess based on the heuristic
            next_guess = HEURISTICS[heuristic](self.word_length, current_state, feedback)

            # Get feedback from the game on the guess
            feedback = get_feedback(next_guess, target_word)

            # Update the internal state based on the feedback
            current_state = update_state(current_state, next_guess, feedback)

            all_positions_updated = True
            for value in feedback.values():
                if value is None:
                    all_positions_updated = False
                    break

            guesses += 1

        if not all_positions_updated:
            raise ValueError("Feedback dictionary is missing entries")

        return guesses


def update_state(state: str, guess: str, feedback: Dict[str, str]) -> str:
    """Updates the internal state based on the guess and feedback."""

    new_state = ""
    for i, letter in enumerate(guess):
        if feedback[letter] == "🟩":
            new_state += letter
        elif feedback[letter] == "🟨":
            if letter not in state:
                # Not in the word, exclude from future guesses
                new_state += "X"
            else:
                # In the word but wrong position, mark for future guesses
                new_state += letter
        else:
            # Not in the word, exclude from future guesses
            new_state += "X"

    return new_state


def validate_feedback(feedback: Dict[str, str]) -> None:
    """Validates the feedback dictionary."""

    if len(feedback) != 5:
        raise ValueError("Feedback dictionary must have 5 entries.")

    valid_values = {"🟩", "🟨", "⬛"}
    for key, value in feedback.items():
        if len(key) != 1 or value not in valid_values:
            raise ValueError(f"Invalid feedback entry: {key}={value}")


def get_feedback(guess: str, target_word: str) -> Dict[str, str]:
    """Simulates the game and returns feedback for the guess."""

    # Simulate Wordle game logic to generate feedback
    feedback = {}
    for i, letter in enumerate(guess):
        if letter == target_word[i]:
            feedback[letter] = "🟩"
        elif letter in target_word:
            feedback[letter] = "🟨"
        else:
            feedback[letter] = "⬛"

    # Validate the feedback dictionary
    validate_feedback(feedback)

    return feedback
