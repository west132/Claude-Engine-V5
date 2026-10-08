# Copyright (c) 2026 West132.WL. All rights reserved.
"""Languages offered by the app and the small amount of text the program itself writes in the game language
(round header, roll-result words, status lines). Narration is written by the model in the game language.
Terms follow the engine's glossary (BACKGROUND world_state.glossary.<language>): ROUND N = 第 N 回合; saved/save = 已存/下次存档;
YES,AND = 是，而且 ...; Success = 成功; HP = 生命."""
from __future__ import annotations
import re

LANGUAGES = {"en": "English", "zh_hans": "简体中文"}
DEFAULT = "en"

BANDS = {"YES, AND": "是，而且", "YES": "是", "NO, BUT": "否，但是", "NO, AND": "否，而且"}
OUTCOMES = {"Success": "成功", "Failure": "失败"}
STATS = [("HP", "生命"), ("MP", "魔力"), ("XP", "经验"), ("Fighting style", "战斗风格"), ("usage die", "用量骰"), ("money", "金钱"),
         ("level", "等级"), ("rest", "休息"), ("fatigue", "疲劳")]


def is_zh(lang: str) -> bool:
    return str(lang).startswith("zh")


def normalize(lang) -> str:
    return lang if lang in LANGUAGES else DEFAULT


def header_words(lang: str) -> dict:
    if is_zh(lang):
        return {"round": "第 {n} 回合", "saved": "已存", "save": "下次存档", "day": "第 {n} 天"}
    return {"round": "ROUND {n}", "saved": "saved", "save": "save", "day": "Day {n}"}


def glossary_form(glossary: dict, key: str, fallback: str) -> str:
    """'Hale Workshop = 黑尔工坊 (short)' -> '黑尔工坊'. Falls back to the English name."""
    raw = (glossary or {}).get(key)
    if not isinstance(raw, str) or "=" not in raw:
        return fallback
    form = raw.split(";")[0].split("=", 1)[1].strip()
    return re.sub(r"\s*\(.*?\)\s*$", "", form) or fallback


def localize_line(line: str, lang: str) -> str:
    """Roll and answer lines are the helper's output, verbatim; for Chinese the band/outcome word is added after it (AI_RULES)."""
    if not is_zh(lang):
        return line
    out = []
    for l in line.split("\n"):
        m = re.search(r"(Outcome: )(Success|Failure)\s*$", l)
        if m:
            l = l + f"（{OUTCOMES[m.group(2)]}）"
        else:
            m = re.search(r"→ (YES, AND|YES|NO, BUT|NO, AND)\s*$", l)
            if m: l = l + f"（{BANDS[m.group(1)]}）"
            else:
                m = re.search(r"→ (Success|Failure)\s*$", l)          # lite roll line
                if m: l = l + f"（{OUTCOMES[m.group(1)]}）"
        out.append(l)
    return "\n".join(out)


def localize_status(text: str, lang: str) -> str:
    if not is_zh(lang):
        return text
    for en, zh in STATS:
        text = re.sub(rf"(?<![A-Za-z]){re.escape(en)}(?![A-Za-z])", zh, text)
    return text
