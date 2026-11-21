"""命令行测试：互转、校验与练习纸。"""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from romannum.cli import main


class ConvertCommandTest(unittest.TestCase):
    def test_to_roman(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(["to", "1997"])
        self.assertEqual(code, 0)
        self.assertEqual(buffer.getvalue().strip(), "MCMXCVII")

    def test_to_roman_out_of_range(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["to", "0"])
        self.assertEqual(code, 2)
        self.assertIn("参数错误", error.getvalue())

    def test_from_roman(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(["from", "mcmxcvii"])
        self.assertEqual(code, 0)
        self.assertEqual(buffer.getvalue().strip(), "1997")

    def test_from_roman_invalid(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["from", "IIII"])
        self.assertEqual(code, 2)


class CheckCommandTest(unittest.TestCase):
    def test_valid_numeral(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(["check", "MCMXCVII"])
        self.assertEqual(code, 0)
        self.assertIn("标准写法", buffer.getvalue())
        self.assertIn("1997", buffer.getvalue())

    def test_invalid_numeral(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = main(["check", "IIII"])
        self.assertEqual(code, 1)
        self.assertIn("不是标准写法", buffer.getvalue())


class SheetCommandTest(unittest.TestCase):
    def test_writes_sheet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "out" / "sheet.html"
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = main(
                    ["sheet", "-o", str(target), "--count", "8", "--max", "50"]
                )
            self.assertEqual(code, 0)
            content = target.read_text(encoding="utf-8")
            self.assertEqual(content.count('<li class="q">'), 8)
            self.assertIn("已生成", buffer.getvalue())

    def test_answers_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sheet.html"
            main(["sheet", "-o", str(target), "--count", "4", "--answers"])
            self.assertIn("参考答案", target.read_text(encoding="utf-8"))

    def test_seed_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "a.html"
            second = Path(tmp) / "b.html"
            main(["sheet", "-o", str(first), "--seed", "11", "--answers"])
            main(["sheet", "-o", str(second), "--seed", "11", "--answers"])
            self.assertEqual(
                first.read_text(encoding="utf-8"),
                second.read_text(encoding="utf-8"),
            )

    def test_to_roman_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sheet.html"
            main(
                [
                    "sheet",
                    "-o",
                    str(target),
                    "--count",
                    "3",
                    "--mode",
                    "to-roman",
                ]
            )
            content = target.read_text(encoding="utf-8")
            self.assertEqual(content.count("写成罗马数字"), 3)
            self.assertNotIn("写成阿拉伯数字", content)

    def test_bad_count(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["sheet", "--count", "0"])
        self.assertEqual(code, 2)

    def test_bad_max(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            code = main(["sheet", "--max", "5000"])
        self.assertEqual(code, 2)

    def test_custom_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sheet.html"
            main(["sheet", "-o", str(target), "--title", "罗马数字小测"])
            self.assertIn("罗马数字小测", target.read_text(encoding="utf-8"))


class ParserTest(unittest.TestCase):
    def test_help_exits_zero(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--help"])
        self.assertEqual(caught.exception.code, 0)

    def test_missing_command_exits(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                main([])


if __name__ == "__main__":
    unittest.main()
