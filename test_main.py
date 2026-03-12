import unittest

from main import update_game_state


class UpdateGameStateTests(unittest.TestCase):
    def test_invalid_empty_guess_is_ignored(self) -> None:
        guessed, lives = update_game_state("apple", ["a"], "   ", 5)
        self.assertEqual(guessed, ["a"])
        self.assertEqual(lives, 5)

    def test_invalid_multi_character_guess_is_ignored(self) -> None:
        guessed, lives = update_game_state("apple", ["a"], "ab", 5)
        self.assertEqual(guessed, ["a"])
        self.assertEqual(lives, 5)

    def test_invalid_non_ascii_guess_is_ignored(self) -> None:
        guessed, lives = update_game_state("apple", ["a"], "é", 5)
        self.assertEqual(guessed, ["a"])
        self.assertEqual(lives, 5)

    def test_duplicate_guess_does_not_change_state(self) -> None:
        guessed, lives = update_game_state("apple", ["p", "a"], "p", 4)
        self.assertEqual(guessed, ["a", "p"])
        self.assertEqual(lives, 4)

    def test_correct_new_guess_keeps_lives(self) -> None:
        guessed, lives = update_game_state("apple", ["a"], "p", 6)
        self.assertEqual(guessed, ["a", "p"])
        self.assertEqual(lives, 6)

    def test_wrong_new_guess_decrements_life_once(self) -> None:
        guessed, lives = update_game_state("apple", ["a"], "z", 6)
        self.assertEqual(guessed, ["a", "z"])
        self.assertEqual(lives, 5)

    def test_lives_never_go_below_zero(self) -> None:
        guessed, lives = update_game_state("apple", ["a"], "z", 0)
        self.assertEqual(guessed, ["a", "z"])
        self.assertEqual(lives, 0)

    def test_negative_input_lives_are_clamped(self) -> None:
        guessed, lives = update_game_state("apple", ["b", "a"], "c", -3)
        self.assertEqual(guessed, ["a", "b", "c"])
        self.assertEqual(lives, 0)


if __name__ == "__main__":
    unittest.main()
