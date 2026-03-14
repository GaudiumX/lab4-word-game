# My Original Thinking

## App States
I think of the game as a simple state machine. Here are the states I came up with:

- **START** – The game is ready to begin. The word has been chosen, lives are set, but no guesses have been made yet. (Maybe show a welcome message.)
- **PLAYING** – The main loop: player guesses letters, we update the display, check win/loss.
- **WON** – All letters guessed correctly. Celebrate, then ask if they want to play again.
- **LOST** – Lives hit zero. Reveal the word, then ask for replay.
- **REPLAY** – A “soft reset” that keeps the same word list but picks a new word and resets all variables.

I also considered an **ERROR** state if something unexpected happens (e.g., the word list is empty, or input validation fails catastrophically), but I’ll probably just handle errors gracefully inside PLAYING.

---

## App Variables
These are the pieces of data I need to track:

- `secret_word` (str): the word the player must guess.
- `word_list` (list[str]): the pool of possible words. Could be hardcoded or loaded from a file.
- `max_lives` (int): constant, default 6.
- `lives_left` (int): starts at `max_lives`, decreases on wrong guesses.
- `guessed_letters` (set[str]): letters already guessed (lowercase). Using a set automatically prevents duplicates.
- `incorrect_guesses` (list[str]): optional, just for displaying wrong guesses separately.
- `display_word` (list[str]): a list of characters showing the current masked word, e.g., `['_', 'a', '_', '_']`. I'll compute this from `secret_word` and `guessed_letters` after each guess.
- `game_active` (bool): True while the game is in PLAYING state; False when game ends (helps control the loop).
- `play_again` (bool): for the replay prompt.

I also took account storing a `score` or `games_won` count across sessions, but these functions are somewhat extraneous.

---

## App Rules and Invariants
These are the “laws” my game must always obey:

1. **One letter per guess**: Input must be a single alphabetic character. If it’s longer, empty, or non‑alphabetic, reject it without penalty.
2. **Case insensitivity**: Convert all guesses to lowercase before processing.
3. **No repeated guesses**: If a letter has already been guessed (whether correct or not), ignore it and prompt again. Do **not** deduct a life.
4. **Reveal all occurrences**: If the guessed letter appears multiple times in the secret word, all those positions become visible.
5. **Life deduction rule**: Only deduct a life if the guessed letter is **not** in the secret word **and** it hasn’t been guessed before.
6. **Lives never go below zero**: Once lives hit zero, the game ends immediately (LOST state).
7. **Win detection**: The player wins when every character in `secret_word` is present in `guessed_letters`. (i.e., no underscores remain.)
8. **Display consistency**: The `display_word` always has the same length as `secret_word`. Unguessed letters show as `'_'`, guessed letters show as themselves.
9. **State exclusivity**: The game cannot be in both WON and LOST at the same time. Once a terminal state is reached, no further guesses are processed.
10. **Reset integrity**: On replay, all game variables (except `word_list`) must be completely reset to their initial values. No leftover state from the previous game.

---

## App Bugs and Edge Cases
Things that could go wrong (and that I should test for):

- **Empty input**: Player just presses Enter. Should be ignored, not crash.
- **Multiple characters**: e.g., “ab”. Should be rejected without penalty.
- **Non‑alphabetic input**: Numbers, symbols, spaces. Same as above.
- **Uppercase vs lowercase**: If I forget to normalize, guessing ‘A’ won’t match ‘a’ in the word.
- **Repeated guess after win/loss**: Player might try to guess again after game ended. Loop should prevent that.
- **Repeated letter in secret word**: e.g., “apple”. Guessing ‘p’ should reveal **both** p’s. Off‑by‑one errors in display logic could miss one.
- **Win condition check timing**: If the last missing letter is guessed, win detection must happen **before** asking for next input, not after.
- **Lives off‑by‑one**: Starting at 6, first wrong guess should bring to 5, not 4. Common mistake.
- **Display lag**: After a correct guess, the masked word updates, but maybe the old display still shows for one turn.
- **Replay not resetting**: If I forget to reset `guessed_letters`, `lives_left`, etc., the new game will be corrupted.
- **Word list empty**: If the list is somehow empty (e.g., file missing), the game should show an error instead of crashing.
- **Very long word**: Display might wrap in the console, but that’s cosmetic; still works.
- **Guess after losing all lives**: The loop should exit immediately when lives hit 0; otherwise the player could keep guessing with negative lives.
- **Duplicate guess counting as wrong**: If player guesses the same wrong letter twice, my logic must **not** deduct another life. Using a `set` helps, but I need to check membership **before** processing.

I’ll keep these in mind when writing tests.

# CoPilot Suggestions

## App States
For a Hangman-style word game, these states are usually enough:

1. `INIT`  
Load words, choose the secret word, set lives, clear guessed letters.

2. `PLAYING`  
Main loop: accept guess, validate input, update guessed letters/lives/display, check for end conditions.

3. `WON`  
All letters are revealed. Show success message and final word.

4. `LOST`  
Lives reached 0. Reveal word and show game-over message.

5. `REPLAY_PROMPT`  
Ask whether the player wants another round.

6. `EXIT`  
End program if player declines replay.

Optional but useful:

1. `ERROR`  
For fatal setup issues (for example, empty word list or failed file load).

If you want, I can also give you a clean state-transition table (what events move from one state to another).

## App Variables
Great question. For a Hangman-style word game, track these as your core variables:

1. secret_word (string)  
The chosen word the player must guess.

2. word_list (list of strings)  
Pool of possible words for each round.

3. max_lives (int)  
Constant life limit, like 6.

4. lives_left (int)  
Current remaining lives this round.

5. guessed_letters (set of strings)  
All letters guessed so far (store lowercase).

6. display_word (list of strings, or computed string)  
Current masked view, like _ a _ _.

7. game_state (enum/string)  
Current state: START, PLAYING, WON, LOST, REPLAY_PROMPT, EXIT.

8. play_again (bool, or handled via state)  
Whether user wants another round.

Useful optional variables:

1. incorrect_guesses (list of strings)  
Only wrong guessed letters, useful for display.

2. correct_guesses (set of strings)  
Can make some checks clearer, though you can derive this from guessed_letters.

3. games_won and games_played (int)  
If you want session scoring.

4. last_message (string)  
Helpful for showing feedback like Invalid input or Already guessed.

If you want to keep it clean and minimal, the best starter set is:
secret_word, word_list, max_lives, lives_left, guessed_letters, game_state.  
Everything else can be derived or added later.

## App Rules and Invariants
For a Hangman-style word game, solid rules and invariants are:

1. One-letter input only  
Each guess must be exactly one alphabetic character.

2. Case-insensitive processing  
Normalize guesses to lowercase before any checks.

3. No penalty for invalid input  
Empty, multi-character, or non-letter input is rejected without losing a life.

4. No penalty for repeated guesses  
If a letter was guessed before, ignore it and prompt again.

5. Correct-guess reveal rule  
A correct letter reveals all matching positions in the secret word.

6. Wrong-guess penalty rule  
Deduct one life only when the guessed letter is new and not in the secret word.

7. Lives lower bound  
Lives never drop below 0.

8. Win condition  
Player wins iff every unique letter in the secret word has been guessed.

9. Loss condition  
Player loses immediately when lives reach 0.

10. State exclusivity  
Game can be in only one state at a time (`PLAYING`, `WON`, `LOST`, etc.), and terminal states stop further guesses.

11. Display consistency  
Displayed mask length always equals secret-word length; each position is either `_` or the actual letter.

12. Reset integrity on replay  
Starting a new round resets all per-round data (`secret_word`, `lives_left`, guesses, display) while persistent data (like `word_list` or score) stays intentional.

If you want, I can convert these into assert-style checks you can paste directly into tests.

## App Bugs and Edge Cases
Common bugs in Word Guess/Hangman implementations:

1. Input validation bugs  
- Empty input accepted as a guess  
- Multiple characters treated as one guess  
- Digits/symbols accidentally accepted  
- Leading/trailing spaces not trimmed before validation

2. Case-handling bugs  
- Uppercase guesses not normalized, so A does not match a  
- Mixed-case secret words compared inconsistently

3. Repeated-guess bugs  
- Re-guessing a letter still deducts a life  
- Repeated guesses counted again in history/statistics  
- Duplicate entries shown in guessed-letter display

4. Life counter bugs  
- Off-by-one on initialization or decrement (starts wrong or decrements twice)  
- Lives can drop below 0  
- Loss checked too late, allowing extra guess after reaching 0

5. Reveal logic bugs  
- Correct guess reveals only first occurrence, not all occurrences  
- Wrong index mapping reveals incorrect positions  
- Display string/list not updated immediately after a correct guess

6. Win/loss detection bugs  
- Win condition checks only length or first match, not all letters  
- Win check runs after next input instead of right after the guess  
- Game can enter both WON and LOST due to bad condition ordering

7. State-machine bugs  
- Guesses still processed in terminal states  
- Replay starts without resetting all round-specific state  
- Replay keeps old guessed letters or old display mask

8. Data-structure bugs  
- Using list instead of set for guessed letters causes duplicate logic errors  
- Incorrect guesses and all guesses drift out of sync  
- Mutating shared default containers between games/functions

9. Word-source bugs  
- Empty word list crashes random selection  
- Word contains punctuation/hyphen and validation logic cannot handle it  
- Hidden newline/whitespace in loaded words breaks matching

10. UI/feedback bugs  
- Showing stale board after a guess  
- Not informing user why input was rejected  
- Incorrectly displayed guessed letters (unsorted/confusing order)

11. Control-flow bugs  
- Infinite loop on invalid input path  
- Break/continue in wrong branch skips critical checks  
- End-of-game prompt not handling unexpected responses properly

12. Testing gaps that let bugs slip through  
- No tests for repeated letters in secret word (example: apple)  
- No tests for duplicate wrong guesses  
- No tests for boundary cases (1 life left, last missing letter, empty input)

Quick high-value tests to catch most of these:
1. Guess same wrong letter twice and verify lives drops once.  
2. Guess letter with multiple occurrences and verify all positions reveal.  
3. Guess final missing letter and verify immediate win.  
4. Hit 0 lives and verify no further guesses are processed.  
5. Replay and verify guessed letters, lives, and display are fully reset.

# Observation
# My Observations

## On App States
Copilot’s list was very similar to mine, but they explicitly separated `INIT` and `EXIT`, and included `REPLAY_PROMPT` as a distinct state. I had combined some of these into `START` and `REPLAY`. I think having a dedicated `REPLAY_PROMPT` state makes sense to clearly separate asking the player from the game‑over display. Also, `EXIT` is a clean way to end the program instead of just quitting abruptly. Copilot’s suggestion of an `ERROR` state (which I also considered) is good for robustness, though I’ll probably keep error handling inside `PLAYING` for simplicity. Overall, Copilot helped me think about a more structured state machine.

## On App Variables
Copilot’s list was comprehensive and matched mine closely. They emphasized `game_state` as an enum/string, which I had as `game_active` boolean but a state variable is more flexible. They also suggested `last_message` for feedback, which I hadn’t thought of; that could be useful to display messages like “Invalid input” without cluttering the UI logic. Their minimal set (`secret_word`, `word_list`, `max_lives`, `lives_left`, `guessed_letters`, `game_state`) is a good reminder that many things can be derived. I might adopt `game_state` instead of a boolean and add `last_message` for better user feedback.

## On App Rules and Invariants
Copilot’s rules were very detailed, almost like a specification. I had 10 rules; they had 12, adding “No penalty for invalid input” (which I had implicitly) and “Lives lower bound” (which I had as rule 6). They also phrased win condition more precisely: “every unique letter in the secret word has been guessed” I had “every character”, but that could be misinterpreted; unique letters is correct because repeated letters don’t need multiple guesses. Their rule about “State exclusivity” was clearer. I think converting these into assert‑style checks for tests is a great idea. I’ll try to write some tests based on these invariants.

## On App Bugs and Edge Cases
Copilot’s list was exhaustive, covering many edge cases I missed. I had 14 items; they added categories like “Data‑structure bugs”, “Word‑source bugs”, “UI/feedback bugs”, “Control‑flow bugs”, and “Testing gaps”. Specifically, I hadn’t considered:
- Leading/trailing spaces not trimmed (good catch)
- Using list vs set for guessed letters causing duplicates (I already use set, but good to note)
- Word containing punctuation/hyphen. my word list will be simple, but if I load from file, that’s a risk.
- Not informing user why input was rejected. I should add that.
- Infinite loop on invalid input. I need to ensure my loop doesn’t get stuck.
- The list of high‑value tests is very helpful; I’ll definitely test duplicate wrong guess, multiple occurrences, final guess, zero lives, and replay reset.

Overall, Copilot’s suggestions complemented my own thinking and gave me practical ideas for implementation and testing. I feel more confident about tackling the code now.
