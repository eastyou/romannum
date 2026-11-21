"""模型层测试：互转、标准写法校验与题目生成。"""

from __future__ import annotations

import unittest

from romannum.model import (
    Question,
    RomanError,
    from_roman,
    is_valid_roman,
    make_questions,
    to_roman,
)


class ToRomanTest(unittest.TestCase):
    def test_known_values(self) -> None:
        cases = {
            1: "I",
            4: "IV",
            9: "IX",
            14: "XIV",
            40: "XL",
            44: "XLIV",
            90: "XC",
            99: "XCIX",
            400: "CD",
            444: "CDXLIV",
            900: "CM",
            1990: "MCMXC",
            2026: "MMXXVI",
            3999: "MMMCMXCIX",
        }
        for value, numeral in cases.items():
            self.assertEqual(to_roman(value), numeral)

    def test_all_values_roundtrip(self) -> None:
        for value in range(1, 4000):
            self.assertEqual(from_roman(to_roman(value)), value)

    def test_reject_zero(self) -> None:
        with self.assertRaises(RomanError):
            to_roman(0)

    def test_reject_negative(self) -> None:
        with self.assertRaises(RomanError):
            to_roman(-1)

    def test_reject_above_limit(self) -> None:
        with self.assertRaises(RomanError):
            to_roman(4000)

    def test_reject_bool(self) -> None:
        with self.assertRaises(RomanError):
            to_roman(True)  # type: ignore[arg-type]

    def test_reject_string(self) -> None:
        with self.assertRaises(RomanError):
            to_roman("12")  # type: ignore[arg-type]


class FromRomanTest(unittest.TestCase):
    def test_lowercase_and_spaces(self) -> None:
        self.assertEqual(from_roman("  mcmxcvii "), 1997)

    def test_simple_symbols(self) -> None:
        self.assertEqual(from_roman("MMXXVI"), 2026)

    def test_reject_empty(self) -> None:
        with self.assertRaises(RomanError):
            from_roman("")

    def test_reject_non_string(self) -> None:
        with self.assertRaises(RomanError):
            from_roman(1987)  # type: ignore[arg-type]

    def test_reject_unknown_character(self) -> None:
        with self.assertRaises(RomanError):
            from_roman("ABC")

    def test_reject_four_repeats(self) -> None:
        with self.assertRaises(RomanError):
            from_roman("IIII")

    def test_reject_non_canonical_subtraction(self) -> None:
        for text in ("VX", "IL", "IC", "IIX", "VV"):
            with self.assertRaises(RomanError):
                from_roman(text)

    def test_reject_overflow(self) -> None:
        with self.assertRaises(RomanError):
            from_roman("MMMM")

    def test_reject_too_long(self) -> None:
        with self.assertRaises(RomanError):
            from_roman("M" * 20)


class ValidTest(unittest.TestCase):
    def test_valid(self) -> None:
        self.assertTrue(is_valid_roman("MCMXCVII"))

    def test_invalid(self) -> None:
        self.assertFalse(is_valid_roman("IIII"))

    def test_non_string(self) -> None:
        self.assertFalse(is_valid_roman(None))  # type: ignore[arg-type]


class QuestionTest(unittest.TestCase):
    def test_to_roman_prompt_and_answer(self) -> None:
        question = Question(38, "XXXVIII", "to-roman")
        self.assertEqual(question.prompt, "38")
        self.assertEqual(question.answer, "XXXVIII")

    def test_to_number_prompt_and_answer(self) -> None:
        question = Question(38, "XXXVIII", "to-number")
        self.assertEqual(question.prompt, "XXXVIII")
        self.assertEqual(question.answer, "38")

    def test_mismatched_numeral_rejected(self) -> None:
        with self.assertRaises(RomanError):
            Question(38, "XXXIX", "to-roman")

    def test_bad_direction_rejected(self) -> None:
        with self.assertRaises(RomanError):
            Question(38, "XXXVIII", "spell")

    def test_to_dict(self) -> None:
        data = Question(4, "IV", "to-number").to_dict()
        self.assertEqual(data["prompt"], "IV")
        self.assertEqual(data["answer"], "4")


class MakeQuestionsTest(unittest.TestCase):
    def test_count_and_uniqueness(self) -> None:
        questions = make_questions(20, 100, seed=5)
        self.assertEqual(len(questions), 20)
        self.assertEqual(len({item.value for item in questions}), 20)

    def test_reproducible(self) -> None:
        first = [item.to_dict() for item in make_questions(12, 50, seed=9)]
        second = [item.to_dict() for item in make_questions(12, 50, seed=9)]
        self.assertEqual(first, second)

    def test_values_within_limit(self) -> None:
        for item in make_questions(15, 20, seed=2):
            self.assertGreaterEqual(item.value, 1)
            self.assertLessEqual(item.value, 20)

    def test_to_roman_mode(self) -> None:
        questions = make_questions(6, 100, mode="to-roman")
        self.assertTrue(all(item.direction == "to-roman" for item in questions))

    def test_to_number_mode(self) -> None:
        questions = make_questions(6, 100, mode="to-number")
        self.assertTrue(all(item.direction == "to-number" for item in questions))

    def test_mixed_mode_alternates(self) -> None:
        questions = make_questions(6, 100, mode="mixed")
        self.assertEqual(
            [item.direction for item in questions],
            ["to-roman", "to-number"] * 3,
        )

    def test_reject_bad_count(self) -> None:
        with self.assertRaises(RomanError):
            make_questions(0, 100)

    def test_reject_count_above_pool(self) -> None:
        with self.assertRaises(RomanError):
            make_questions(20, 10)

    def test_reject_bad_limit(self) -> None:
        with self.assertRaises(RomanError):
            make_questions(5, 4000)

    def test_reject_bad_mode(self) -> None:
        with self.assertRaises(RomanError):
            make_questions(5, 100, mode="spell")


if __name__ == "__main__":
    unittest.main()
