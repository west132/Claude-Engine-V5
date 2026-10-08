# Copyright (c) 2026 West132.WL. All rights reserved.
"""Engine "cards": verbatim slices of the engine files.

Nothing here rewrites engine text. Sections are cut at their own headings, and
the §2.1 routing table is read from the engine file itself, so replacing the
engine files with a newer version just works as long as the layout holds.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path

from .textutil import est_tokens

# §10 is the action-resolution card; vitals (§10.5) has its own routing row and is large.
PLAIN_EXCLUDES = {"10": {"10.5"}}
# §16 is persistence: the host runs it in code. Only its judgement subsections reach the model.
HOST_ONLY_PLAIN = {"16"}

_SEC = re.compile(r"^## (\d+|[A-D])\.\s")
_SUB = re.compile(r"^### (\d+\.\d+|[A-D]\.\d+)\s")
_ANY12 = re.compile(r"^#{1,2} ")
_ANY123 = re.compile(r"^#{1,3} ")
_REF = re.compile(r"§\s*([0-9]+(?:\.[0-9]+)?|[A-D](?:\s*[–-]\s*[A-D])?(?:\.[0-9]+)?)")


@dataclass
class Route:
    id: str
    description: str
    refs: list[str]


@dataclass
class Card:
    ref: str
    title: str
    text: str
    rows: list[str] = field(default_factory=list)

    @property
    def tokens(self) -> int:
        return est_tokens(self.text)


def _expand(ref: str) -> list[str]:
    m = re.fullmatch(r"([A-D])\s*[–-]\s*([A-D])", ref)
    if m:
        return [chr(c) for c in range(ord(m.group(1)), ord(m.group(2)) + 1)]
    return [ref.strip()]


class Engine:
    def __init__(self, engine_dir: Path):
        files = sorted(engine_dir.glob("NEW_ENGINE_v*.md"))
        if not files:
            raise FileNotFoundError(f"no NEW_ENGINE_v*.md in {engine_dir}")
        self.path = files[-1]
        self.version = re.search(r"_v(\d+_\d+)", self.path.name).group(1).replace("_", ".")
        self.text = self.path.read_text(encoding="utf-8")
        self.lines = self.text.splitlines()
        self._index()
        rules = sorted(engine_dir.glob("AI_RULES_v*.md"))
        self.rules_text = rules[-1].read_text(encoding="utf-8") if rules else ""
        self.rules_lines = self.rules_text.splitlines()
        self.routes = self._parse_routes()

    # ---- indexing -------------------------------------------------------------------
    def _index(self):
        L = self.lines
        self.sec: dict[str, tuple[int, int]] = {}
        self.sub: dict[str, tuple[int, int]] = {}
        self.part0 = (0, len(L))
        p0 = p1 = None
        for i, l in enumerate(L):
            if l.startswith("# PART 0"): p0 = i
            elif l.startswith("# PART 1") and p1 is None: p1 = i
        if p0 is not None and p1 is not None:
            self.part0 = (p0, p1)
        for i, l in enumerate(L):
            m = _SEC.match(l)
            if m:
                j = next((k for k in range(i + 1, len(L)) if _ANY12.match(L[k])), len(L))
                self.sec[m.group(1)] = (i, j)
            m = _SUB.match(l)
            if m:
                j = next((k for k in range(i + 1, len(L)) if _ANY123.match(L[k])), len(L))
                self.sub[m.group(1)] = (i, j)

    def _slice(self, a: int, b: int) -> str:
        out = self.lines[a:b]
        while out and (not out[-1].strip() or out[-1].strip() == "---"):
            out.pop()
        return "\n".join(out)

    def _parse_routes(self) -> list[Route]:
        if "2.1" not in self.sub:
            return []
        a, b = self.sub["2.1"]
        block, inside = [], False
        for l in self.lines[a:b]:
            if l.startswith("```"):
                if inside: break
                inside = True
                continue
            if inside: block.append(l)
        routes: list[Route] = []
        for l in block:
            if not l.strip():
                continue
            if "§" not in l:
                if routes: routes[-1].description += " " + l.strip()
                continue
            desc, _, refs_txt = l.partition("§")
            refs = [r for m in _REF.finditer("§" + refs_txt) for r in _expand(m.group(1))]
            routes.append(Route(f"r{len(routes) + 1:02d}", re.sub(r"\s+", " ", desc).strip(), refs))
        return routes

    # ---- always-on text -------------------------------------------------------------
    def part0_text(self) -> str:
        return self._slice(*self.part0)

    def section_text(self, key: str, exclude: set[str] | None = None) -> str:
        """Verbatim text of a `## N.` section (with its `###` subsections), or of one `### N.M`."""
        if key in self.sub:
            return self._slice(*self.sub[key])
        if key not in self.sec:
            raise KeyError(key)
        a, b = self.sec[key]
        subs = sorted((v[0], k) for k, v in self.sub.items() if a < v[0] < b)
        if not exclude or not subs:
            return self._slice(a, b)
        keep, cursor = [], a
        for start, k in subs:
            if k in exclude:
                keep.append(self._slice(cursor, start))
                end = self.sub[k][1]
                cursor = end
        keep.append(self._slice(cursor, b))
        return "\n".join(x for x in keep if x.strip())

    def title_of(self, key: str) -> str:
        a, _ = self.sub.get(key) or self.sec[key]
        return self.lines[a].lstrip("# ").strip()

    def in_part0(self, key: str) -> bool:
        a, b = self.sub.get(key) or self.sec.get(key) or (None, None)
        return a is not None and self.part0[0] <= a < self.part0[1]

    # ---- AI_RULES ---------------------------------------------------------------------
    def rules_section(self, n: str) -> str:
        L = self.rules_lines
        a = next((i for i, l in enumerate(L) if l.startswith(f"## {n}.")), None)
        if a is None:
            return ""
        b = next((k for k in range(a + 1, len(L)) if L[k].startswith("## ") or L[k].strip() == "---"), len(L))
        return "\n".join(L[a:b]).rstrip()

    def rules_block(self, label: str) -> str:
        """A bold-labelled block inside AI_RULES §2, e.g. 'Language' or 'Narration craft'."""
        L = self.rules_lines
        a = next((i for i, l in enumerate(L) if l.startswith(f"**{label}")), None)
        if a is None:
            return ""
        b = next((k for k in range(a + 1, len(L)) if L[k].startswith("**") or L[k].startswith("## ")), len(L))
        return "\n".join(L[a:b]).rstrip()

    # ---- routing ------------------------------------------------------------------------
    def routing_table(self) -> str:
        return "\n".join(f"{r.id}: {r.description}" for r in self.routes)

    def cards_for(self, row_ids: list[str], enabled_modules: dict | None = None) -> list[Card]:
        enabled = enabled_modules or {}
        mod_of = {"A": "numeric_level_xp", "B": "equipment_power_tiers",
                  "C": "bounded_scenario_endings", "D": "flexible_item_entitlement"}
        want: dict[str, list[str]] = {}
        order: list[str] = []
        rid_set = set(row_ids)
        for r in self.routes:
            if r.id not in rid_set:
                continue
            for ref in r.refs:
                if self.in_part0(ref) or ref in HOST_ONLY_PLAIN:
                    continue
                if ref in mod_of and not enabled.get(mod_of[ref]):
                    continue
                if ref not in self.sec and ref not in self.sub:
                    continue
                want.setdefault(ref, []).append(r.id)
                if ref not in order: order.append(ref)
        def sort_key(ref):
            head = ref.split(".")[0]
            return (1, head) if head.isalpha() else (0, int(head), ref)
        order.sort(key=lambda r: (sort_key(r), r))
        cards: list[Card] = []
        covered: set[str] = set()
        for ref in order:
            if ref in self.sec:
                text = self.section_text(ref, set(PLAIN_EXCLUDES.get(ref, ())))
                covered |= {k for k in self.sub if k.startswith(ref + ".") and k not in PLAIN_EXCLUDES.get(ref, ())}
            else:
                if ref in covered:
                    continue
                text = self.section_text(ref)
            cards.append(Card(ref, self.title_of(ref), text, want[ref]))
        return cards

    def module_cards(self, enabled_modules: dict) -> list[Card]:
        return self.cards_for([r.id for r in self.routes if any(x in "ABCD" for x in r.refs)], enabled_modules)

    def card_by_ref(self, ref: str) -> Card:
        ref = ref.strip().lstrip("§")
        if ref in self.sec:
            return Card(ref, self.title_of(ref), self.section_text(ref, set(PLAIN_EXCLUDES.get(ref, ()))))
        if ref in self.sub:
            return Card(ref, self.title_of(ref), self.section_text(ref))
        raise KeyError(f"no engine section {ref!r}")
