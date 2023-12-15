class WordleSolver:
    def __init__(self, word_length, heuristics):
        self.word_length = word_length
        self.heuristics = heuristics
        self.secret_word = None
        self.guesses = []
        self.feedback = []
        self.used_words = set()

    def set_secret_word(self, secret_word):
        """
        Sets the secret word to be the given word. Lowercases for standardization.
        """
        self.secret_word = secret_word.lower()

    def solve(self, heuristic, secret_word=None):
        """
        Solves for the given secret_word using the given heuristic function.
        """
        # Ensure that a secret word is given
        if not secret_word:
            raise ValueError("Secret word is not provided.")
        self.set_secret_word(secret_word)
        # Use up to word_length + 1 guesses
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
        """
        Chooses a candidate word to be the guess answer, using the given heuristic.
        """
        while True:
            candidate_word = heuristic(self.word_length, self.guesses, self.feedback, self.used_words, self.secret_word)
            if candidate_word not in self.used_words:
                self.used_words.add(candidate_word)
                return candidate_word

    def _get_feedback(self, guess):
        """
        Gets feedback for each letter in a guess word in an ordered array.
        Feedback of 2 indicates green; 1 indicates yellow; 0 indicates gray.
        Green = letter AND position right; yellow = letter right but wrong position; gray = exclude letter.
        This feedback aligns with how Wordle operates traditionally to give users hints.
        """
        feedback = []
        for i, letter in enumerate(guess):
            if letter == self.secret_word[i]:
                feedback.append(2)
            elif letter in self.secret_word:
                feedback.append(1)
            else:
                feedback.append(0)
        return feedback
