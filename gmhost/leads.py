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
_RECAP = [
    r"发生(?:了)?什么", r"发生过什么", r"(?:之前|刚才|前面|上次|前情|目前|现在)(?:的)?(?:事|情况|剧情|进展)", r"回顾", r"总结(?:一下)?", r"前情(?:提要)?",
    r"(?:我们|我)(?:都)?(?:做|干)了(?:些)?什么", r"到哪(?:了|里了)", r"什么情况", r"(?:提醒|告诉)我",
    r"\bwhat (?:has |have |had )?(?:happened|i done|i been doing|did i do)\b", r"\bwhat(?:'s| is) (?:going on|the situation|happening)\b", r"\brecap\b",
    r"\bsummar(?:y|ise|ize)\b", r"\bcatch me up\b", r"\bwhere (?:are we|was i|am i at)\b", r"\bremind me\b", r"\bso far\b",
]
_CONT = r"^(?:继续(?:吧|下去|游戏)?|接着(?:来|走)?|然后(?:呢)?|往下(?:走|继续)?|下一步|go on|continue|carry on|next|then what|and then|proceed|keep going)[.!。！？?\s]*$"
_RE_GUIDE = re.compile("|".join(_GUIDE), re.I)
_RE_CONT = re.compile(_CONT, re.I)
_RE_RECAP = re.compile("|".join(_RECAP), re.I)
_CLOSED = ("closed", "done", "paid", "complete", "fulfilled", "ended", "void", "expired", "revoked", "cancel", "resolved", "settled", "failed", "abandon")


def is_guidance(text: str) -> bool:
    t = (text or "").strip()
    return 0 < len(t) <= 60 and bool(_RE_GUIDE.search(t))


def is_recap(text: str) -> bool:
    t = (text or "").strip()
    return 0 < len(t) <= 80 and bool(_RE_RECAP.search(t))


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


def known_leads(camp, tree: dict | None = None) -> list[str]:
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
    caps = {"npcs": 12, "locations": 6, "factions": 4, "quests": 0}
    for section, items in (camp.readable.get("index") or {}).items():
        if not isinstance(items, dict): continue
        rows = [(iid, _text(line)) for iid, line in items.items()]
        if section == "rights_obligations":
            rows = [(i, l) for i, l in rows if _is_open(l)]
        out += [f"known {section}/{iid}: {line[:150]}" for iid, line in rows[-caps.get(section, 4):] if caps.get(section, 4)]
        # the index is in the order learned, so the newest entries (the last ones) are the most relevant
    return out


_CUES = re.compile(r"offer|phoned|texts?\b|calls?\b|owes?\b|wants?\b|forging|results|recover|appointment|deadline|\bdue\b|pending|waiting|arrang|missing|looking for|sells|commission", re.I)
_DEAD = re.compile(r"killed|\bdead\b|died|arrested|job done|found;", re.I)


def options(camp, tree: dict | None = None, limit: int = 6) -> list[str]:
    """The menu, built in code from what the player knows: open quests, open obligations, then the people the character knows who
    have something pending. Every option is taken from a recorded line, so none can be invented (I9)."""
    from . import i18n
    tree = tree if tree is not None else camp.tree()
    zh, g = camp.language == "zh_hans", camp.glossary()
    out = []
    for qid, q in (tree.get("quests") or {}).items():
        if isinstance(q, dict) and _text(q.get("status")).strip().lower().startswith("active") and q.get("objective"):
            out.append((f"我继续推进任务：{q['objective']}" if zh else f"I carry on with the quest: {q['objective']}"))
    for oid, o in (tree.get("rights_obligations") or {}).items():
        st = (o.get("state") if isinstance(o, dict) else None) or {}
        if isinstance(st, dict) and st.get("next") and _is_open(st.get("status")):
            out.append(f"我处理：{_text(st['next'])[:120]}" if zh else f"I deal with this: {_text(st['next'])[:120]}")
    people = list(((camp.readable.get("index") or {}).get("npcs") or {}).items())
    ranked = []
    for pos, (iid, line) in enumerate(people):
        line = _text(line)
        if _DEAD.search(line) or not _is_open(line): continue
        ranked.append((0 if _CUES.search(line) else 1, -pos, iid, line))
    for _, _, iid, line in sorted(ranked):
        if len(out) >= limit: break
        name, _, note = line.partition(" — ")
        name = i18n.glossary_form(g, iid, name.strip()) if zh else name.strip()
        out.append((f"我去找 {name}" + (f"（{note[:90]}）" if note else "")) if zh else (f"I follow up with {name}" + (f" ({note[:90]})" if note else "")))
    if not out:
        out = ["我先环顾四周，看看情况", "我先休息，等等看有什么动静"] if zh else ["I look around and take stock of where I am", "I rest and wait to see what turns up"]
    return out[:limit]


def menu(camp, tree: dict | None = None) -> dict:
    """A guidance turn answered entirely by code: where you are, when it is, and what you know you could pursue."""
    from . import i18n, timeutil
    zh = camp.language == "zh_hans"
    loc = camp.readable["world_state"].get("location")
    place = i18n.glossary_form(camp.glossary(), str(loc), camp.location_name()) if zh else camp.location_name()
    when = f"{timeutil.date_label(camp.time, camp.language)} {timeutil.clock_label(camp.time)}"
    if zh:
        text = f"你在{place}。现在是 {when}。\n没有什么事情逼着你做。下面是你已知、可以去做的事；你也可以直接输入自己想做的事。"
        question = "你想做什么？"
    else:
        text = (f"You are at {place}. It is {when}.\nNothing is forcing your hand. Here is what you know you could pursue; "
                "or type anything else you want to do.")
        question = "What do you want to do?"
    return {"narration": text, "decision": {"question": question, "options": options(camp, tree)}}


_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})(?: (\d{2}:\d{2}))?")


def recap_facts(camp, tree: dict | None = None, limit: int = 12) -> list[str]:
    """What the player already knows about recent events, from the places the save keeps it: the turns just played (live play),
    dated quest and obligation outcomes, and the facts the character has learned. Nothing from hidden records, plans or truths."""
    tree = tree if tree is not None else camp.tree()
    out = []
    for h in (camp.session.get("history") or [])[-3:]:
        if h.get("narration"):
            out.append(f"Just played — you said: {h.get('player')}. What happened: {h['narration'][:500]}")
    dated = []
    for section, label in (("quests", "quest"), ("rights_obligations", "agreement")):
        for rid, v in (tree.get(section) or {}).items():
            st = v.get("status") if isinstance(v, dict) and "status" in v else ((v.get("state") or {}).get("status") if isinstance(v, dict) else None)
            m = _DATE.search(_text(st or ""))
            if m and not _text(st).lstrip().startswith("{"):
                name = (v.get("objective") if isinstance(v, dict) and v.get("objective") else rid.replace("_", " "))
                dated.append((m.group(1) + " " + (m.group(2) or "00:00"), f"{m.group(1)}{' ' + m.group(2) if m.group(2) else ''} — {label} ({_text(name)[:70]}): {_text(st)[:150]}"))
    out += [t for _, t in sorted(dated)[-8:]]
    facts = ((camp.player.get("knowledge") or {}).get("facts") or {})
    if isinstance(facts, dict):
        out += [f"You learned: {_text(v)[:220]}" for v in list(facts.values())[-4:]]
    return out[-limit:]
