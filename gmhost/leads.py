# Copyright (c) 2026 West132.WL. All rights reserved.
"""Guidance turns (engine §13.6 STUCK): the player asks what to do, asks for options, or just says "continue" while nothing is in
progress. The host recognises these in code, hands the referee only what the player already knows, and insists on a short menu of
known leads. A model must never answer them by inventing what the character does next (§7: the player owns intent)."""
from __future__ import annotations
import re

_GUIDE = [
    r"我(?:现在)?(?:要|该|应该|可以|能|还能)(?:做|干)(?:些)?什么", r"(?:做|干)什么(?:好|呢|才好)?[?？]?$", r"接下来(?:要|该|应该|可以)?(?:做|干)?什么",
    r"怎么办", r"下一步(?:是|该|要)?(?:什么|怎么|做什么)?[?？]?$", r"有(?:什么|哪些)(?:选择|选项|线索|提示|建议|可以做)", r"(?:给我|给点|需要|想要)(?:一?点)?(?:提示|建议|选项|线索)",
    r"不知道(?:该|要|应该)?(?:做什么|怎么办|干什么|去哪)", r"卡住了",
    r"\bwhat (?:should|can|could|do|shall) (?:i|we) (?:do|try|pursue|focus)", r"\bwhat(?:'s| is) (?:next|my next)", r"\bwhat now\b", r"\bwhat next\b",
    r"\b(?:what are )?my options\b", r"\bany (?:hints?|ideas?|leads?|suggestions?)\b", r"\b(?:i'?m|i am) (?:stuck|lost)\b", r"\b(?:give me|need|want) (?:a )?(?:hint|options|suggestions?|ideas?)\b",
    r"\bwhere (?:do|should) i (?:go|start)\b",
]
_CONT = r"^(?:继续(?:吧|下去|游戏)?|接着(?:来|走)?|然后(?:呢)?|往下(?:走|继续)?|下一步|go on|continue|carry on|next|then what|and then|proceed|keep going)[.!。！？?\s]*$"
_RE_GUIDE = re.compile("|".join(_GUIDE), re.I)
_RE_CONT = re.compile(_CONT, re.I)
_CLOSED = ("closed", "done", "paid", "complete", "fulfilled", "ended", "void", "expired", "revoked", "cancel", "resolved", "settled", "failed", "abandon")


def is_guidance(text: str) -> bool:
    t = (text or "").strip()
    return 0 < len(t) <= 60 and bool(_RE_GUIDE.search(t))


def is_bare_continue(text: str) -> bool:
    return bool(_RE_CONT.match((text or "").strip()))


def needs_guidance(camp, text: str) -> bool:
    """True for a question about what to do, or a bare 'continue' with no plan, fight or pending roll to continue."""
    if is_guidance(text):
        return True
    return (is_bare_continue(text) and not (camp.session.get("plan") or "").strip()
            and not camp.session.get("combat") and not camp.session.get("pending_odds"))


def _text(v) -> str:
    return v if isinstance(v, str) else str(v)


def _is_open(status) -> bool:
    s = _text(status).strip().lower()
    return bool(s) and not any(w in s[:40] for w in _CLOSED)


def known_leads(camp, tree: dict | None = None, cap_index: int = 24) -> list[str]:
    """Lines the player may be told about: accepted quests still open, obligations with a next step still open, and the people and
    places the character knows (the index in Part A). Nothing hidden: the index is, by definition, what the player knows."""
    tree = tree if tree is not None else camp.tree()
    out = []
    for qid, q in (tree.get("quests") or {}).items():
        if isinstance(q, dict) and _text(q.get("status")).strip().lower().startswith("active"):
            out.append(f"open quest {qid}: {q.get('objective') or ''} (status: {_text(q.get('status'))[:80]})")
    for oid, o in (tree.get("rights_obligations") or {}).items():
        st = (o.get("state") if isinstance(o, dict) else None) or {}
        if isinstance(st, dict) and st.get("next") and _is_open(st.get("status")):
            out.append(f"open obligation {oid}: next — {_text(st['next'])[:140]}")
    idx = []
    for section, items in (camp.readable.get("index") or {}).items():
        if isinstance(items, dict):
            idx += [f"known {section}/{iid}: {_text(line)[:150]}" for iid, line in items.items()]
    out += idx[-cap_index:]                           # the newest entries are the most relevant; the index is in order learned
    return out


def guidance_directive(camp, text: str, tree: dict | None = None) -> str:
    leads = known_leads(camp, tree)
    return ("GUIDANCE TURN (engine §13.6 STUCK; the player owns intent, §7). The player asked what to do or said 'continue' with nothing in progress.\n"
            "- Do NOT act for the player character, move them, finish their work, or advance time. Roll nothing. Commit nothing.\n"
            "- Call close_round with opened_round=false. `visible` = 1-3 plain sentences restating where the character is, the time, and what is "
            "going on right now, using only facts already in the state below.\n"
            "- `decision` = {question: 'What do you want to do?', options: 3 to 6 numbered-style options}. Each option says WHAT, WHERE/WHO, and the "
            "rough cost or risk, built ONLY from the KNOWN list below. No hidden route, no new fact, no new person or place (I9). "
            "It is a menu, not a limit: free wording stays a normal action.\n"
            "- If the known list holds almost nothing, offer the obvious ordinary things the character could do from here and say plainly that no "
            "lead is pending.\n\nKNOWN TO THE PLAYER (the only facts you may use):\n" + ("\n".join(f"- {l}" for l in leads) or "- (nothing recorded)"))
