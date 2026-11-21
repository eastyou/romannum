"""命令行入口：罗马数字互转、校验与练习纸生成。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .model import MODES, RomanError, from_roman, is_valid_roman, make_questions, to_roman
from .render import render_sheet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="romannum",
        description="罗马数字工具：互转、校验，或生成可打印的 A4 练习纸。",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    to_cmd = sub.add_parser("to", help="阿拉伯数字转罗马数字")
    to_cmd.add_argument("value", type=int)

    from_cmd = sub.add_parser("from", help="罗马数字转阿拉伯数字")
    from_cmd.add_argument("numeral")

    check = sub.add_parser("check", help="检查罗马数字写法是否标准")
    check.add_argument("numeral")

    sheet = sub.add_parser("sheet", help="生成 A4 练习纸")
    sheet.add_argument("-o", "--output", default="romannum-sheet.html")
    sheet.add_argument("--count", type=int, default=20, help="题目数量，默认 20")
    sheet.add_argument("--max", type=int, default=100, help="数值上限，默认 100")
    sheet.add_argument("--seed", type=int, default=0)
    sheet.add_argument("--mode", choices=list(MODES), default="mixed")
    sheet.add_argument("--answers", action="store_true")
    sheet.add_argument("--title", default="罗马数字练习")
    return parser


def _write(path: str, content: str) -> int:
    try:
        target = Path(path)
        if target.parent and not target.parent.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    except OSError as exc:
        print("写入失败：%s" % exc, file=sys.stderr)
        return 1
    print("已生成 %s" % path)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "to":
            print(to_roman(args.value))
            return 0

        if args.command == "from":
            print(from_roman(args.numeral))
            return 0

        if args.command == "check":
            if is_valid_roman(args.numeral):
                print("标准写法：%s = %d" % (args.numeral.strip().upper(), from_roman(args.numeral)))
                return 0
            print("不是标准写法：%s" % args.numeral)
            return 1

        if args.command == "sheet":
            questions = make_questions(args.count, args.max, args.seed, args.mode)
            content = render_sheet(questions, title=args.title, answers=args.answers)
            return _write(args.output, content)
    except RomanError as exc:
        print("参数错误：%s" % exc, file=sys.stderr)
        return 2

    print("未知命令", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
