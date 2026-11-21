"""罗马数字与阿拉伯数字互转，以及练习纸题目生成。"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple

MIN_VALUE = 1
MAX_VALUE = 3999
MAX_COUNT = 40
MODES = ("to-roman", "to-number", "mixed")

NUMERALS: Tuple[Tuple[int, str], ...] = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

SYMBOL_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


class RomanError(ValueError):
    """罗马数字或参数非法。"""


def _as_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RomanError("%s 必须是整数" % name)
    return value


def to_roman(value: int) -> str:
    """把 1~3999 的整数转成标准罗马数字。"""

    value = _as_int(value, "value")
    if not MIN_VALUE <= value <= MAX_VALUE:
        raise RomanError("数值必须在 %d~%d 之间" % (MIN_VALUE, MAX_VALUE))
    remaining = value
    parts: List[str] = []
    for amount, symbol in NUMERALS:
        while remaining >= amount:
            parts.append(symbol)
            remaining -= amount
    return "".join(parts)


def from_roman(text: str) -> int:
    """把标准罗马数字转成整数；非标准写法（如 IIII、VX）会被拒绝。"""

    if not isinstance(text, str):
        raise RomanError("罗马数字必须是字符串")
    cleaned = text.strip().upper()
    if not cleaned:
        raise RomanError("罗马数字不能为空")
    if len(cleaned) > 15:
        raise RomanError("罗马数字过长")
    for char in cleaned:
        if char not in SYMBOL_VALUES:
            raise RomanError("包含非法字符：%s" % char)

    total = 0
    index = 0
    while index < len(cleaned):
        current = SYMBOL_VALUES[cleaned[index]]
        if index + 1 < len(cleaned):
            following = SYMBOL_VALUES[cleaned[index + 1]]
        else:
            following = 0
        if current < following:
            total -= current
        else:
            total += current
        index += 1

    if not MIN_VALUE <= total <= MAX_VALUE:
        raise RomanError("数值超出范围")
    if to_roman(total) != cleaned:
        raise RomanError("不是标准罗马数字写法：%s" % cleaned)
    return total


def is_valid_roman(text: str) -> bool:
    try:
        from_roman(text)
    except RomanError:
        return False
    return True


@dataclass(frozen=True)
class Question:
    value: int
    numeral: str
    direction: str

    def __post_init__(self) -> None:
        value = _as_int(self.value, "value")
        if not MIN_VALUE <= value <= MAX_VALUE:
            raise RomanError("数值超出范围")
        if self.direction not in ("to-roman", "to-number"):
            raise RomanError("题目方向必须是 to-roman 或 to-number")
        if self.numeral != to_roman(value):
            raise RomanError("题目中的罗马数字与数值不一致")

    @property
    def prompt(self) -> str:
        return str(self.value) if self.direction == "to-roman" else self.numeral

    @property
    def answer(self) -> str:
        return self.numeral if self.direction == "to-roman" else str(self.value)

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "numeral": self.numeral,
            "direction": self.direction,
            "prompt": self.prompt,
            "answer": self.answer,
        }


def make_questions(
    count: int,
    max_value: int = 100,
    seed: int = 0,
    mode: str = "mixed",
) -> List[Question]:
    """生成不重复数值的练习题。"""

    count = _as_int(count, "count")
    max_value = _as_int(max_value, "max_value")
    seed = _as_int(seed, "seed")
    if not 1 <= count <= MAX_COUNT:
        raise RomanError("题目数量必须在 1~%d 之间" % MAX_COUNT)
    if not MIN_VALUE <= max_value <= MAX_VALUE:
        raise RomanError("数值上限必须在 %d~%d 之间" % (MIN_VALUE, MAX_VALUE))
    if mode not in MODES:
        raise RomanError("模式必须是 %s" % "、".join(MODES))
    if count > max_value:
        raise RomanError("题目数量不能超过数值上限")

    rng = random.Random(seed)
    values = rng.sample(range(MIN_VALUE, max_value + 1), count)
    questions: List[Question] = []
    for index, value in enumerate(values):
        if mode == "to-roman":
            direction = "to-roman"
        elif mode == "to-number":
            direction = "to-number"
        else:
            direction = "to-roman" if index % 2 == 0 else "to-number"
        questions.append(
            Question(value=value, numeral=to_roman(value), direction=direction)
        )
    return questions
