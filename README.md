# Wordle Heuristic Analysis

This script analyzes the performance of different Wordle heuristics.

### But first, how does Wordle work?
New York Times Wordle is a 5-letter word guessing game wherein players have the opportunity to take up to 6 attempts to guess a secret word from the English dictionary. For each guess, players receive hints about how correct their guess is, broken down by letter. Correctly placed letters are green, correct letters in invalid indices within a word are yellow, and letters that are fully excluded in the secret word are grayed. The goal is to get all greens which means each letter matches that of the SECRET_WORD.

Advanced variants might have different versions. For the scope of this project we are also including 6 and 7 letter word options with letter_count + 1 number of attempted guesses in line with another Wordle inspired website: MoreWordle.

### 2 Modes

Our script operates in 1 of 2 modes.

* Single-word analysis: Applies a chosen heuristic on a single secret word.
* Comparison mode: Analyzes the performance of all heuristics on a chosen percentage of words from the word list.

### Usage

python agent.py WORD_LENGTH (--heuristic [HEURISTIC_NUMBER] | --comparison [PERCENT])

#### Arguments:

WORD_LENGTH: Length of Wordle words (5, 6, or 7)
--heuristic: Flag to run a single option from the heuristics dictionary (optional)
[HEURISTIC_NUMBER]: Index or name of the heuristic to analyze (1-8) (used only with --heuristic)
--comparison: Flag to run comparison mode for all heuristics (optional)
[PERCENT]: Percentage of word list to analyze (default 50%) (used only with --comparison)

While the heuristic and comparison flags are mutually exclusive it is required to have one of them.

#### Example usages:

##### Analyze single-word performance of the second heuristic on 5-letter words:
python agent.py 5 --heuristic 2

##### Run comparison mode on 6-letter words with 75% of the word list:
python agent.py 6 --comparison 75