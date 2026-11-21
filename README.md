# romannum

[![CI](https://github.com/eastyou/romannum/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/romannum/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

罗马数字小工具：1~3999 双向转换、严格校验标准写法，并生成可打印的 A4 练习纸。纯标准库、零依赖。

## 安装

```bash
pip install -e .
```

## 用法

```bash
# 数字转罗马数字
romannum to 1997          # MCMXCVII

# 罗马数字转数字（大小写与首尾空格都能处理）
romannum from mcmxcvii    # 1997

# 校验写法：合法退出码 0，非法 1
romannum check MCMXCVII
romannum check IIII       # 不是标准写法

# 生成 20 道混合练习（数字↔罗马数字交替）
romannum sheet -o 练习.html --count 20 --max 100 --seed 2026 --answers

# 只练「数字转罗马数字」
romannum sheet -o 练习.html --mode to-roman --max 1000
```

练习纸顶部附有常用对照表，题目分两栏排版，`--answers` 会在末尾附加答案页。

## 校验规则

- 只接受 1~3999，`MMMM` 及以上会被拒绝。
- 采用标准减法写法：`IV`、`IX`、`XL`、`XC`、`CD`、`CM`。
- 拒绝 `IIII`、`VV`、`IL`、`IC`、`VX` 等非标准写法：先求值，再检查是否能由标准算法还原。

## 项目结构

```text
romannum/
├── romannum/
│   ├── __init__.py
│   ├── __main__.py
│   ├── model.py      # 双向转换、校验与题目生成
│   ├── render.py     # A4 练习纸排版
│   └── cli.py        # 命令行入口
├── examples/
│   └── sample.html
└── tests/
    ├── test_model.py
    ├── test_render.py
    └── test_cli.py
```

## 测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © 2026 eastyou
