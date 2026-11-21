"""罗马数字练习纸的 A4 排版。"""

from __future__ import annotations

import html
from typing import List, Sequence

from .model import MAX_COUNT, Question, RomanError, to_roman

LEGEND = (
    "I=1　V=5　X=10　L=50　C=100　D=500　M=1000；"
    "左减右加：IV=4　IX=9　XL=40　XC=90　CD=400　CM=900"
)


def render_sheet(
    questions: Sequence[Question],
    title: str = "罗马数字练习",
    answers: bool = False,
) -> str:
    """生成可打印的 A4 练习纸。"""

    if not questions:
        raise RomanError("至少需要一道题")
    if len(questions) > MAX_COUNT:
        raise RomanError("一张练习纸最多 %d 道题" % MAX_COUNT)
    for question in questions:
        if not isinstance(question, Question):
            raise RomanError("questions 只能包含 Question")

    safe_title = html.escape(title)
    items: List[str] = []
    for index, question in enumerate(questions, start=1):
        hint = "写成罗马数字" if question.direction == "to-roman" else "写成阿拉伯数字"
        items.append(
            '<li class="q"><span class="no">%d</span>'
            '<span class="prompt">%s</span>'
            '<span class="arrow">→</span><span class="blank"></span>'
            '<span class="hint">%s</span></li>'
            % (index, html.escape(question.prompt), hint)
        )

    answer_block = ""
    if answers:
        rows = "".join(
            "<tr><td>%d</td><td>%d</td><td>%s</td></tr>"
            % (index, question.value, question.numeral)
            for index, question in enumerate(questions, start=1)
        )
        answer_block = (
            '<section class="answers"><h2>参考答案</h2>'
            "<table><thead><tr><th>序号</th><th>阿拉伯数字</th>"
            "<th>罗马数字</th></tr></thead><tbody>%s</tbody></table></section>" % rows
        )

    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>
  @page { size: A4; margin: 10mm; }
  * { box-sizing: border-box; }
  body { margin: 0; background: #f3f1ec; color: #2a2620;
         font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif; }
  .sheet { width: 190mm; margin: 0 auto; background: #fff; padding: 8mm;
           box-shadow: 0 2px 12px rgba(0,0,0,.12); }
  h1 { font-size: 21px; margin: 0 0 2mm; }
  .legend { font-size: 11px; color: #6b5b3e; background: #faf6ea;
            border: 1px solid #e8dfc8; padding: 2mm 3mm; border-radius: 3px;
            margin-bottom: 3mm; line-height: 1.7; }
  .meta { font-size: 12px; display: flex; gap: 8mm; margin-bottom: 4mm; }
  ol.quiz { list-style: none; padding: 0; margin: 0;
            columns: 2; column-gap: 8mm; }
  li.q { break-inside: avoid; page-break-inside: avoid; display: flex;
         align-items: baseline; gap: 2mm; padding: 2.2mm 0;
         border-bottom: 1px dashed #ddd; font-size: 14px; }
  .no { color: #999; font-size: 12px; width: 5mm; }
  .prompt { font-family: Georgia, "Times New Roman", serif; font-weight: 600;
            min-width: 26mm; }
  .arrow { color: #9a8350; }
  .blank { flex: 1; border-bottom: 1px solid #333; height: 14px; }
  .hint { font-size: 10px; color: #bbb; white-space: nowrap; }
  .answers { margin-top: 6mm; page-break-before: always; }
  .answers h2 { font-size: 17px; margin: 0 0 3mm; }
  .answers table { width: 70%%; border-collapse: collapse; font-size: 13px; }
  .answers th, .answers td { border: 1px solid #d5d0c4; padding: 1.5mm 2mm;
                             text-align: center; }
  .answers th { background: #faf6ea; }
  @media print { body { background: #fff; } .sheet { box-shadow: none;
                 width: auto; padding: 0; } }
</style>
</head>
<body>
<div class="sheet">
  <h1>%s</h1>
  <div class="legend">%s</div>
  <div class="meta"><span>姓名：____________</span><span>班级：____________</span>
    <span>日期：____________</span></div>
  <ol class="quiz">%s</ol>
  %s
</div>
</body>
</html>
""" % (safe_title, safe_title, LEGEND, "".join(items), answer_block)


def reference_chart() -> List[str]:
    """返回常用数值与罗马数字的对照，便于课堂板书。"""

    values = (1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000)
    return ["%d = %s" % (value, to_roman(value)) for value in values]
