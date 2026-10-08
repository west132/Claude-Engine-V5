"""Deterministic prose checks (no model involved)."""
from __future__ import annotations
import re

from .textutil import _CJK

_LEAKS = (re.compile(r"\bGM-Δ\b"), re.compile(r"^\s*ROUND \d+\s*\|", re.M), re.compile(r"\b\d*d\d+\b.*\bTotal\b", re.I),
          re.compile(r"\b2d10\b", re.I), re.compile(r"\b(Capability|Difficulty|Stakes):\s*[-+]?\d"))


def words(text: str) -> int:
    cjk = len(_CJK.findall(text))
    return cjk // 2 + len(re.findall(r"[A-Za-z0-9À-ÿ']+", text))


def check_prose(text: str, language: str, lite: bool, secret_terms: set[str], decision: bool) -> list[str]:
    issues = []
    if not text.strip():
        return ["the prose is empty"]
    for rx in _LEAKS:
        if rx.search(text):
            issues.append("mechanics leaked into the prose (header, dice, totals or GM-Δ): remove them; the host shows those")
            break
    low = text.lower()
    for t in sorted(secret_terms):
        if re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", low):
            issues.append(f"the prose contains the secret term {t!r}, which would reveal a hidden fact (I5, I9)")
    letters = re.findall(r"[^\W\d_]", text)
    if letters:
        cjk = len(_CJK.findall(text)) / len(letters)
        if language.startswith(("zh", "ja", "ko")) and cjk < 0.5:
            issues.append(f"the game language is {language}: write the prose natively in it")
        if language in ("en", "es", "fr", "de", "it", "pt", "ms") and cjk > 0.2:
            issues.append(f"the game language is {language}: the prose must be in that language")
    if lite and not decision and words(text) > 190:
        issues.append(f"lite profile: keep the prose to about 120 words (it is {words(text)})")
    if text.count("```") or re.search(r"^\s*#{1,3} ", text, re.M):
        issues.append("no markdown headings or code fences in prose")
    return issues
