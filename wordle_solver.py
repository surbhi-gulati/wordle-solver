from heuristics import HEURISTICS, _get_all_valid_words, _get_valid_words

class WordleSolver:
    def __init__(self, word_length, heuristics):
        self.word_length = word_length
        self.heuristics = heuristics
        self.secret_word = None
        self.guesses = []
        self.feedback = []

    # Set the given word as the secret word for this Wordle game.
    def set_secret_word(self, secret_word):
        self.secret_word = secret_word.lower()

    # Solve the given Wordle puzzle by prioritizing given heuristic.
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
                print("BAD GUESS: " + guess)
        if guess == self.secret_word:
            print("GOOD GUESS: " + guess)
            print(f"Word solved in {len(self.guesses)} guesses using {heuristic} heuristic.")
            return len(self.guesses)
        else:
            print(f"Failed to solve the word after {len(self.guesses)} guesses.")
            return -1

    # Select a word guess based on the heuristic function given.
    def _choose_word(self, heuristic):
        valid_words = _get_valid_words(self.word_length, self.guesses, self.feedback)
        # Random anchor guess.
        if len(self.guesses) == 0:
            return valid_words.pop()
        # Heuristic guess after feedback is given.
        else:
            return heuristic(self.word_length, self.guesses, self.feedback)

    # Simulate word feedback. Green = 2; Yellow = 1; Gray = 0.
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
