# Guess The Word Game

A console-based Hangman-style word guessing game written in Python.  
The computer randomly selects a word from a staggering assemblage of over 300000 words, and the player guesses letters one at a time.  
The game tracks guessed letters, remaining lives, and displays the masked word.

## Features

- Random word selection from a predefined list
- Masked word display (e.g., `_ a _ _ _`)
- Tracks guessed letters and incorrect guesses
- Win/loss detection
- Replay option without restarting the program
- Clean separation of game logic and user interface

## How to Run

1. Make sure you have **Python 3.8 or higher** installed.
2. Clone or download this repository.
3. Open a terminal in the project folder.
4. Run the game:

```bash
python main.py
