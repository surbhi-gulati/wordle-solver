from collections import Counter
import math

from heuristics import HEURISTICS, _get_all_valid_words, _get_valid_words

class WordleSolver:
    def __init__(self, word_length, heuristics):
        self.word_length = word_length
        self.heuristics = heuristics
        self.secret_word = None
        self.guesses = []
        self.feedback = []
        self.used_words = set()  # New attribute to track used words

    def set_secret_word(self, secret_word):
        self.secret_word = secret_word.lower()

    def solve(self, heuristic, secret_word=None):
        if not secret_word:
            raise ValueError("Secret word is not provided.")
        self.set_secret_word(secret_word)
        while len(self.guesses) < self.word_length + 1:
            guess = self._choose_word(heuristic)
            feedback = self._get_feedback(guess)
            self.guesses.append(guess)
            self.feedback.append(feedback)
            if guess == self.secret_word:
                break
            else:
                print("BAD GUESS:", guess)
        if guess == self.secret_word:
            print("GOOD GUESS:", guess)
        print(f"Word solved in {len(self.guesses)} guesses using {heuristic} heuristic.")
        return len(self.guesses)

    def _choose_word(self, heuristic):
        valid_words = _get_valid_words(self.word_length, self.guesses, self.feedback, self.used_words)
        while True:
            candidate_word = heuristic(self.word_length, self.guesses, self.feedback, self.used_words)
            if candidate_word not in self.used_words:
                self.used_words.add(candidate_word)
                return candidate_word

    def _get_feedback(self, guess):
        feedback = []
        for i, letter in enumerate(guess):
            if letter == self.secret_word[i]:
                feedback.append(2)
            elif letter in self.secret_word:
                feedback.append(1)
            else:
                feedback.append(0)
        return feedback
