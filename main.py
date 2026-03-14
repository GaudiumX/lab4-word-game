"""
Core state helper for the Hangman-style game.

Provides a single pure helper `update_game_state(...)` used by the
game loop to process one letter guess. Key guarantees:

- Returned `lives` is always >= 0.
- Returned guessed-letters list is sorted and contains no duplicates.
- Invalid guesses (empty, multi-char, non-ascii letters) are ignored
    without penalty.
- Membership checks are case-insensitive with ASCII letters only.

Example:
        new_guessed, new_lives = update_game_state('apple', ['a'], 'p', 6)
"""

import random
import sys



def update_game_state(secret_word: str, guessed_letters: list[str], guess: str, lives: int) -> tuple[list[str], int]:
    """
    Update game state with a new guess.

    Parameters:
    - secret_word: the word to guess (lowercase, no spaces)
    - guessed_letters: list of letters already guessed (lowercase)
    - guess: the new guessed letter (should be a single lowercase letter)
    - lives: current lives remaining (non‑negative)

    Returns:
    - new list of guessed letters (sorted)
    - updated lives (never negative)

    Notes:
    - Invalid guesses are ignored without penalty.
    """
    
    safe_lives = max(0, lives)

    
    guess = guess.strip().lower()
    if len(guess) != 1 or not (guess.isalpha() and guess.isascii()):
        return sorted(guessed_letters.copy()), safe_lives

    
    guessed_set = set(guessed_letters)
    if guess in guessed_set:
        
        return sorted(guessed_letters.copy()), safe_lives

    
    new_guessed = guessed_letters.copy()
    new_guessed.append(guess)

    
    if guess in secret_word.lower():
        new_lives = safe_lives
    else:
        new_lives = max(0, safe_lives - 1)

    
    new_guessed.sort()

    return new_guessed, new_lives




def build_display_word(secret_word: str, guessed_letters: list[str]) -> str:
    
    return ''.join(letter if letter in guessed_letters else '_' for letter in secret_word)


def is_word_guessed(secret_word: str, guessed_letters: list[str]) -> bool:
    
    return all(letter in guessed_letters for letter in secret_word)


def get_valid_guess(guessed_letters: list[str]) -> str:
    
    while True:
        raw = input("Guess a letter: ").strip()
        if len(raw) != 1:
            print("❌ Please enter exactly one character.")
            continue
        if not raw.isalpha():
            print("❌ Please enter a letter (a-z).")
            continue
        guess = raw.lower()
        if guess in guessed_letters:
            print(f"⏳ You already guessed '{guess}'. Try a different letter.")
            continue
        return guess


def display_game(secret_word: str, guessed_letters: list[str], lives_left: int, max_lives: int):
    
    print("\n" + "=" * 40)
    print(f"Word:   {build_display_word(secret_word, guessed_letters)}")
    print(f"Guessed: {', '.join(sorted(guessed_letters)) if guessed_letters else '(none)'}")
    print(f"Lives:   {'❤️ ' * lives_left}{'🖤 ' * (max_lives - lives_left)} ({lives_left}/{max_lives})")
    print("=" * 40)




def play_game(word_list: list[str], max_lives: int = 6):
    
    state = "START"          

    while state != "EXIT":
        if state == "START":
            
            secret_word = random.choice(word_list)
            guessed_letters = []
            lives_left = max_lives
            state = "PLAYING"
            print("\n🎮 NEW GAME – Guess the word!")

        elif state == "PLAYING":
            
            display_game(secret_word, guessed_letters, lives_left, max_lives)

            
            guess = get_valid_guess(guessed_letters)

            
            guessed_letters, lives_left = update_game_state(
                secret_word, guessed_letters, guess, lives_left
            )

            
            if is_word_guessed(secret_word, guessed_letters):
                state = "WON"
            elif lives_left <= 0:
                state = "LOST"

        elif state == "WON":
            display_game(secret_word, guessed_letters, lives_left, max_lives)
            print("🎉 CONGRATULATIONS! You guessed the word!")
            state = "REPLAY"

        elif state == "LOST":
            display_game(secret_word, guessed_letters, lives_left, max_lives)
            print(f"💀 GAME OVER – The word was '{secret_word}'.")
            state = "REPLAY"

        elif state == "REPLAY":
            answer = input("\nPlay again? (y/n): ").strip().lower()
            if answer == 'y' or answer == 'yes':
                state = "START"
            else:
                state = "EXIT"
                print("👋 Thanks for playing!")

def load_word_list(filename="words_alpha.txt"):
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            words = []
            for line in f:
                word = line.strip().lower()
                
                if word.isalpha() and len(word) > 0:
                    words.append(word)
            if not words:
                print(f"⚠️  No valid words found in {filename}. Using default word list.")
                return ["python", "java", "kotlin", "swift", "rust", "go", "typescript"]
            return words
    except FileNotFoundError:
        print(f"⚠️  Word list file '{filename}' not found. Using default word list.")
        return ["python", "java", "kotlin", "swift", "rust", "go", "typescript"]



if __name__ == "__main__":
    
    word_file = "words_alpha.txt"
    if len(sys.argv) > 1:
        word_file = sys.argv[1]

    word_list = load_word_list(word_file)
    print("🐍 WELCOME TO GUESS THE WORD (Hangman style)")
    print(f"Loaded {len(word_list)} words from {word_file}")
    play_game(word_list, max_lives=6)
