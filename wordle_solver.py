from heuristics import HEURISTICS, _get_all_valid_words

class WordleSolver:

    def __init__(self, word_length, heuristics):
        self.word_length = word_length
        self.heuristics = heuristics
        self.secret_word = None
        self.guesses = []
        self.feedback = []

    def set_secret_word(self, secret_word):
        self.secret_word = secret_word.lower()

    def get_valid_words(self):
        # TODO: Implement a more efficient way to get valid words based on feedback
        valid_words = set()
        for word in _get_all_valid_words(self.word_length):
            if self._is_valid_word(word):
                valid_words.add(word)
        return valid_words

    def _is_valid_word(self, word):
        # TODO: Improve efficiency by checking only applicable feedback
        for guess, feedback in zip(self.guesses, self.feedback):
            for i, (letter, fb_value) in enumerate(zip(guess, feedback)):
                if fb_value == 0: # gray
                    if letter in word:
                        return False
                elif fb_value == 1: # yellow
                    if letter not in word or word[i] == letter:
                        return False
                elif fb_value == 2: # green
                    if letter != word[i]:
                        return False
        return True

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
        if guess == self.secret_word:
            print(f"Word solved in {len(self.guesses)} guesses using {heuristic} heuristic.")
            return len(self.guesses)
        else:
            print(f"Failed to solve the word after {len(self.guesses)} guesses.")
            return -1


    def _choose_word(self, heuristic):
        valid_words = self.get_valid_words()
        if len(self.guesses) == 0:
            # First guess, any valid word can be chosen
            return valid_words.pop()
        else:
            # Choose word based on provided heuristic
            return heuristic(self.word_length, self.guesses, self.feedback)

    def _get_feedback(self, guess):
        # Simulate feedback based on the secret word
        feedback = []
        for i, letter in enumerate(guess):
            if letter == self.secret_word[i]:
                feedback.append(2) # green
            elif letter in self.secret_word:
                feedback.append(1) # yellow
            else:
                feedback.append(0) # gray
        return feedback
