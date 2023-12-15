from collections import Counter
from heuristics import _get_valid_words

class WordleSolver:
    def __init__(self, word_length, heuristics):
        self.word_length = word_length
        self.heuristics = heuristics
        self.secret_word = None
        self.guesses = []
        self.feedback = []
        self.used_words = set()

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
                print("GOOD GUESS:", guess)
                break
            else:
                print("BAD GUESS:", guess)
        # Feedback 
        if guess == self.secret_word:
            print(f"SOLVED WORD!!!")
        else:
            print(f"FAILED!!!")
        return len(self.guesses)

    def _choose_word(self, heuristic):
        valid_words = _get_valid_words(self.word_length, self.guesses, self.feedback, self.used_words)
        while True:
            candidate_word = heuristic(self.word_length, self.guesses, self.feedback, self.used_words, self.secret_word)
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
