"""渲染层测试：题目行、答案页与排版约束。"""

from __future__ import annotations

import unittest

from romannum.model import Question, make_questions
from romannum.render import reference_chart, render_sheet


class SheetTest(unittest.TestCase):
    def test_question_rows(self) -> None:
        questions = make_questions(12, 100, seed=3)
        html = render_sheet(questions)
        self.assertEqual(html.count('<li class="q">'), 12)

    def test_direction_hints(self) -> None:
        html = render_sheet([Question(38, "XXXVIII", "to-roman")])
        self.assertIn("写成罗马数字", html)
        self.assertIn(">38<", html)

    def test_to_number_hint(self) -> None:
        html = render_sheet([Question(38, "XXXVIII", "to-number")])
        self.assertIn("写成阿拉伯数字", html)
        self.assertIn(">XXXVIII<", html)

    def test_legend_present(self) -> None:
        html = render_sheet([Question(4, "IV", "to-roman")])
        self.assertIn("X=10", html)
        self.assertIn("CM=900", html)

    def test_answers_hidden(self) -> None:
        html = render_sheet([Question(38, "XXXVIII", "to-roman")])
        self.assertNotIn("参考答案", html)
        self.assertNotIn("XXXVIII", html)

    def test_answers_page(self) -> None:
        html = render_sheet([Question(38, "XXXVIII", "to-roman")], answers=True)
        self.assertIn("参考答案", html)
        self.assertIn("XXXVIII", html)
        self.assertIn("38", html)

    def test_title_escaped(self) -> None:
        html = render_sheet([Question(4, "IV", "to-roman")], title="<b>罗马</b>")
        self.assertIn("&lt;b&gt;", html)
        self.assertNotIn("<b>罗马</b>", html)

    def test_empty_rejected(self) -> None:
        with self.assertRaises(ValueError):
            render_sheet([])

    def test_wrong_type_rejected(self) -> None:
        with self.assertRaises(ValueError):
            render_sheet(["IV"])  # type: ignore[list-item]

    def test_too_many_questions(self) -> None:
        questions = [Question(value, _numeral(value), "to-roman") for value in range(1, 42)]
        with self.assertRaises(ValueError):
            render_sheet(questions)

    def test_print_css(self) -> None:
        html = render_sheet([Question(4, "IV", "to-roman")])
        self.assertIn("@page", html)
        self.assertIn("@media print", html)


class ReferenceChartTest(unittest.TestCase):
    def test_contains_key_values(self) -> None:
        chart = reference_chart()
        self.assertIn("1 = I", chart)
        self.assertIn("1000 = M", chart)
        self.assertEqual(len(chart), 13)


def _numeral(value: int) -> str:
    from romannum.model import to_roman

    return to_roman(value)


if __name__ == "__main__":
    unittest.main()
