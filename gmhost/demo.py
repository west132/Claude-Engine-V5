"""A rule-based stand-in for a language model (config: backend = "mock").

It lets you click through the whole app — tools, dice, saves, UI — with no model installed,
and it is what the integration tests drive. It is deliberately dumb: it is NOT a game master.
"""
from __future__ import annotations
import json
import re

from .llm import Backend


class DemoBackend(Backend):
    name = "demo"
    n_ctx = 32768

    def chat(self, messages, *, max_tokens=1024, temperature=0.3, schema=None, on_token=None):
        sys0 = messages[0]["content"]
        if sys0.startswith("ROLE: NARRATOR"):
            out = self._narrate(messages[-1]["content"])
        elif sys0.startswith("ROLE: CHECKER"):
            out = json.dumps({"ok": True, "issues": []})
        elif schema and "triage" in (schema.get("properties") or {}):
            out = self._triage(messages[-1]["content"])
        else:
            out = json.dumps(self._step(messages))
        if on_token: on_token(out)
        return out

    @staticmethod
    def _narrate(user: str) -> str:
        m = re.search(r"WHAT THE PLAYER PERCEIVES.*?:\n(.*?)(?:\n\n|$)", user, re.S)
        facts = [l[2:].strip() for l in (m.group(1).splitlines() if m else []) if l.startswith("- ")]
        return " ".join(f.rstrip(".") + "." for f in facts) or "Nothing much happens."

    @staticmethod
    def _triage(user: str) -> str:
        t = re.search(r"PLAYER SAYS: (.*)", user).group(1).lower()
        if any(w in t for w in ("shoot", "attack", "fight", "hit ", "stab")):
            return json.dumps({"triage": "LOOP", "intent": t, "rows": ["r01", "r02", "r04", "r05", "r03"]})
        if any(w in t for w in ("rest", "sleep", "wait", "travel", "walk")):
            return json.dumps({"triage": "LOOP", "intent": t, "rows": ["r08", "r17"]})
        if t.endswith("?") or t.startswith(("ask", "talk", "speak")):
            return json.dumps({"triage": "LOOP", "intent": t, "rows": ["r07"]})
        return json.dumps({"triage": "FAST", "intent": t, "rows": []})

    def _step(self, messages):
        first = messages[1]["content"]
        results = [m["content"] for m in messages[2:] if m["role"] == "user"]
        done = [json.loads(m["content"])["tool"] for m in messages[2:] if m["role"] == "assistant" and m["content"].startswith("{")]
        said = (re.search(r"PLAYER SAYS: (.*)", first) or [None, ""])[1].lower()
        loc = (re.search(r"location `([^`]+)`", first) or [None, "here"])[1]
        def call(tool, **args): return {"tool": tool, "args": args}
        def close(opened, *visible, **kw): return call("close_round", opened_round=opened, visible=list(visible), **kw)
        if first.startswith("NEW GAME"):
            return close(False, f"It is early. You are at {loc.replace('_', ' ')}.", "The room is warm and noisy.")
        if any(w in said for w in ("shoot", "attack", "fight", "hit ", "stab")):
            if "combat" not in done:
                return call("combat", action="add", id="wolf1", name="a flat-wolf", side="foe", size="normal", v=1,
                            damage_kind="creature", damage_size="man_sized", soak="none", attacks=1)
            if "check" not in done:
                return call("check", action="shoot the wolf", why_uncertain="a moving target in poor light",
                            capability={"mode": "numeric", "cmp": 4, "challenge": 3, "basis": "open ground"},
                            conditions=[{"category": "sensory", "value": 1, "fact": "dim light before dawn"}],
                            stakes={"cost": "loss", "cost_text": "the wolf closes and bites", "reach": "full",
                                    "reach_text": "the wolf goes down", "harm": True},
                            harm={"source_id": "wolf1"}, attack={"kind": "weapon", "size": "bow", "item_id": "crossbow"},
                            target_id="wolf1", skills_exercised=["crossbow"],
                            context={"in_combat": True, "player_chosen_roll": True, "covered_by_order": True, "character_can_judge": True})
            last = results[-1] if results else ""
            if "REFUSED" in last:
                return close(True, "You hesitate and the moment passes.")
            if "SUCCESS" in last and "award_xp" not in done:
                return call("award_xp", kind="combat", scope_id=f"fight_{len(messages)}_{hash(said) % 9999}", scope="meaningful",
                            challenges=[3], participants=["player"])
            if ("player_update" not in done) and "must settle" in last.lower():
                pass
            return close(True, "A flat-wolf lunges out of the dark." if "FAILURE" in last else "The flat-wolf drops and lies still.",
                         "Your bolt flies true." if "SUCCESS" in last else "The wolf's jaws snap at you.", plan="")
        if any(w in said for w in ("rest", "sleep")):
            if "rest" not in done:
                return call("rest", hours=8, quality="full_night", out_of_danger=True)
            if "growth_boundary" not in done:
                return call("growth_boundary", reason="a full night's rest")
            return close(True, "You sleep through the night and wake rested.")
        if any(w in said for w in ("wait", "travel", "walk")):
            if "advance_time" not in done:
                return call("advance_time", minutes=60, activity="waiting")
            last = results[-1] if results else ""
            if "DUE NOW" in last:
                m = re.search(r"- (?:.*?)\((npcs|factions)\.([\w\-]+)\)", last)
                if m and "commit" not in done:
                    return call("commit", entries=[{"op": "~", "id": f"{m.group(1)}.{m.group(2)}.state.due",
                                                    "content": "none (incidental)", "hidden": True}])
            return close(True, "An hour passes.")
        if said.endswith("?") or said.startswith(("ask", "talk", "speak")):
            if "ask" not in done:
                return call("ask", question="Does the innkeeper know of any work?", label="Oda Brandt",
                            settle_test="the board lists work but the innkeeper's own knowledge is not recorded, so it is open",
                            likelihood=1, **{"for": ["she hears every caravan's news"], "against": []})
            return close(True, "Oda wipes the counter and answers.", dialogue=[{"who": "Oda Brandt", "gist": "answers about work"}])
        return close(False, f"You {said or 'wait'}.")
