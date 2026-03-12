"""Core state helper for the Hangman-style game.

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
    # Keep invariants intact even if caller sends bad inputs.
    safe_lives = max(0, lives)

    # ----- Defensive checks -----
    # Normalize and validate guess.
    guess = guess.strip().lower()
    if len(guess) != 1 or not (guess.isalpha() and guess.isascii()):
        return sorted(guessed_letters.copy()), safe_lives

    # ----- Duplicate check -----
    # Convert guessed_letters to a set for O(1) lookup
    guessed_set = set(guessed_letters)
    if guess in guessed_set:
        # No change: return a sorted copy and unchanged (clamped) lives.
        return sorted(guessed_letters.copy()), safe_lives

    # ----- Add new guess -----
    # Create new list with the guess appended (order preserved)
    new_guessed = guessed_letters.copy()
    new_guessed.append(guess)

    # ----- Update lives -----
    if guess in secret_word.lower():
        new_lives = safe_lives
    else:
        new_lives = max(0, safe_lives - 1)

    # (Optional) sort the list for consistent display – you can do this here or in UI
    new_guessed.sort()

    return new_guessed, new_lives