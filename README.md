# WORDLE SOLVER AGENT

## How does Wordle work?
New York Times Wordle is a 5-letter word guessing game wherein players have the opportunity to take up to 6 attempts to guess a secret word from the English dictionary. For each guess, players receive hints about how correct their guess is, broken down by letter. Correctly placed letters are green, correct letters in invalid indices within a word are yellow, and letters that are fully excluded in the secret word are grayed. The goal is to get all greens which means each letter matches that of the SECRET_WORD.

Advanced variants might have different versions. For the scope of this project we are also including 6 and 7 letter word options with letter_count + 1 number of attempted guesses in line with another Wordle inspired website: MoreWordle.

## Run instructions
To run the Wordle Solver Agent:
1. Install the zip of the `agent.py` code and accepted 5-7 letter word lists
2. Run `agent.py` with command: `python agent.py`
3. Follow the given instructions to choose to run all heuristics (Comparison mode) or a single heuristic on either a single word or a selected percentage of words from your list of words. Your word list will the list of 5, 6, or 7 letter words from the English dictionary.

##### [COMPARISON MODE]
Comparison mode runs every heuristic on the chosen secret word or word list rather than on a single heuristic.

##### [DEMO] Single instance mode: 
Runs Wordle solver with a single word from the desired word length list, using the given heuristic. 

Demonstrates guesswork process for the single word and states number of guesses needed.

##### [INSIGHTS] Multi instance mode:
Runs Wordle solver randomly on the given percentage of the desired word length list, using the given heuristic. 

Counts the average number of guesses needed per heuristic and their fail rate to complete guesswork within word length + 1 attempts.
