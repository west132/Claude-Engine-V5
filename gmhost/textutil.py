# Copyright (c) 2026 West132.WL. All rights reserved.
from __future__ import annotations
import json
import re

_CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]")
_THINK = re.compile(r"<think>.*?</think>", re.S | re.I)


def est_tokens(text: str) -> int:
    """Cheap token estimate used for budgeting when no tokenizer is available."""
    cjk = len(_CJK.findall(text))
    return cjk + int((len(text) - cjk) / 3.4) + 1


def strip_think(text: str) -> str:
    text = _THINK.sub("", text)
    if "</think>" in text:                       # opening tag was cut off
        text = text.split("</think>", 1)[1]
    return text.strip()


def extract_json(text: str):
    """First balanced JSON object in model output (tolerates fences and chatter)."""
    text = strip_think(text)
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if fence:
        text = fence.group(1)
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in output")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
            continue
        if ch == '"': in_str = True
        elif ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("unterminated JSON object")


def one_line(s) -> str:
    return re.sub(r"\s+", " ", str(s)).strip()


LANG_NAMES = {"en": "English", "zh_hans": "Simplified Chinese (简体中文)",
              "zh_hant": "Traditional Chinese (繁體中文)", "ja": "Japanese (日本語)",
              "ko": "Korean (한국어)", "es": "Spanish", "fr": "French", "de": "German",
              "ru": "Russian", "pt": "Portuguese", "it": "Italian", "ms": "Malay"}


def lang_name(code: str) -> str:
    return LANG_NAMES.get(code, code)
