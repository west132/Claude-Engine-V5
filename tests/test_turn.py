# Copyright (c) 2026 West132.WL. All rights reserved.
import json
import threading
import urllib.request

import pytest

from gmhost import saves
from gmhost.app import App
from gmhost.campaign import Campaign
from gmhost.demo import DemoBackend
from gmhost.llm import ScriptedBackend
from gmhost.turn import Game, TurnError, header


def step(tool, **args): return json.dumps({"tool": tool, "args": args})
TRIAGE = json.dumps({"triage": "LOOP", "intent": "x", "rows": ["r01"]})
OK = json.dumps({"ok": True, "issues": []})


def scripted(*replies):
    """Replies in call order: triage, referee steps…, narrator, checker."""
    return ScriptedBackend(list(replies))


def test_rollback_on_failure_leaves_state_untouched(cfg, camp):
    b = scripted(TRIAGE, step("player_update", kind="money", data={"delta": -40}, reason="a room"), "garbage", "garbage",
                 "garbage", "garbage", "garbage")
    g = Game(cfg, b)
    cfg.game.max_referee_steps = 3
    with pytest.raises(TurnError):
        g.play(camp, "I pay for a room")
    assert camp.player["money"]["cash_and_accessible_funds"] == 1950 and camp.rnd == 0


def test_refusal_is_fed_back_and_turn_completes(cfg, camp):
    b = scripted(TRIAGE,
                 step("player_update", kind="money", data={"delta": -99999}, reason="a car"),
                 step("player_update", kind="money", data={"delta": -40}, reason="a room"),
                 step("close_round", opened_round=True, visible=["You pay forty dollars for a room."]),
                 "You count forty dollars onto the counter and the clerk pockets it.", OK)
    r = Game(cfg, b).play(camp, "I pay for a room")
    assert camp.player["money"]["cash_and_accessible_funds"] == 1910 and r.round == 1
    assert r.header == "ROUND 1 | 2026-10-06 | 19:40 | Hale Workshop, Morrow Ward | saved R0 · save R10"
    assert "REFUSED: not enough money" in json.dumps(b.calls[2]["messages"])
    assert r.gm_delta == "GM-Δ 1 none"


def test_secret_terms_never_reach_the_player(cfg, camp):
    b = scripted(TRIAGE,
                 step("commit", entries=[{"op": "+", "id": "locked_case_truths.well", "content": '{"cause": "arsenic"}', "secret_terms": ["arsenic"]}]),
                 step("close_round", opened_round=True, visible=["The water tastes flat."]),
                 "The water tastes of arsenic.", "It tastes of arsenic again.", "Arsenic, plainly.")
    r = Game(cfg, b).play(camp, "I drink from the well")
    assert "arsenic" not in r.narration.lower() and r.narration == "The water tastes flat."
    assert any("plain facts" in w for w in r.warnings)
    assert "[hidden" in r.gm_delta and "arsenic" not in r.gm_delta
    assert "arsenic" in camp.chain_text()                      # kept in the capsule chain


def test_checker_issue_triggers_a_rewrite(cfg, camp):
    bad = json.dumps({"ok": False, "issues": [{"kind": "new_fact", "quote": "a dragon", "why": "not in the facts"}]})
    b = scripted(TRIAGE, step("close_round", opened_round=False, visible=["The fire crackles."]),
                 "A dragon lands outside.", bad, "The fire crackles.", OK)
    r = Game(cfg, b).play(camp, "I look around")
    assert r.narration == "The fire crackles." and r.round is None
    assert "new_fact" in json.dumps(b.calls[-2]["messages"])


def test_lite_header_and_profile(cfg, camp):
    camp.readable["profile"] = "lite"
    assert header(camp, 3) == "R 3 | 2026-10-06 19:40 | Hale Workshop, Morrow Ward | save R10"


def test_checkpoint_at_round_10_validates_and_survives_next_save(cfg, example_text, dice):
    dice(10)
    app = App(cfg, DemoBackend())
    app.create("cp", example_text)
    app.opening()
    for i in range(10):
        r = app.play("I shoot the wolf" if i == 0 else "I wait an hour")
    assert r["save"]["valid"] and r["save"]["round"] == 10
    c = app.camp
    assert c.S == 10 and c.T == 20 and c.blocks == []
    for i in range(10):
        r = app.play("I wait an hour")
    assert r["save"]["round"] == 20 and r["save"]["valid"]
    # a fresh process resumes from the journal and from the save
    again = Campaign.open(cfg, "cp")
    assert again.rnd == 20 and again.player["condition"]["hp"] == c.player["condition"]["hp"]
    text = (c.saves / "save_cp_R20.md").read_text(encoding="utf-8")
    c2 = saves.import_save(cfg, "cp2", text, (c.dir / "background.md").read_text(encoding="utf-8"))
    assert c2.player == c.closed_readable["player"] and c2.get("world_state.material_history")


def test_save_failure_blocks_until_retry_or_one_unsaved_round(cfg, example_text, monkeypatch):
    app = App(cfg, DemoBackend())
    app.create("sf", example_text); app.opening()
    real = saves.build_save
    monkeypatch.setattr(saves, "build_save", lambda c: (_ for _ in ()).throw(saves.SaveFailure("disk full")))
    for _ in range(10):
        r = app.play("I wait an hour")
    assert r["save"]["failed"]
    assert app.play("I wait an hour")["blocked"] == "save_due"
    app.continue_unsaved()
    assert app.play("I wait an hour")["round"] == 11
    assert app.play("I wait an hour")["blocked"] == "save_due"
    monkeypatch.setattr(saves, "build_save", real)
    assert app.save()["valid"]
    assert app.play("I wait an hour")["round"] == 12


def test_hidden_state_can_be_encoded_in_saves(cfg, example_text, dice):
    dice(10)
    app = App(cfg, DemoBackend())
    app.create("b64", example_text, encoding="b64"); app.opening()
    for _ in range(10):
        r = app.play("I shoot the wolf" if _ == 0 else "I wait an hour")
    assert r["save"]["valid"]
    txt = (app.camp.saves / "save_b64_R10.md").read_text(encoding="utf-8")
    assert "encoding: b64" in txt and "enc:b64" in txt and "paid {" not in txt


def test_import_refuses_a_save_for_a_different_background(cfg, example_text):
    app = App(cfg, DemoBackend())
    app.create("a", example_text); app.opening()
    for _ in range(10): app.play("I wait an hour")
    save = (app.camp.saves / "save_a_R10.md").read_text(encoding="utf-8")
    other = example_text.replace("ashfall_hunter_gemini_combined_v4_4", "another_world_v1")
    with pytest.raises(Exception, match="points at BACKGROUND"):
        saves.import_save(cfg, "x", save, other)


def test_small_context_is_refused_not_truncated(cfg):
    with pytest.raises(TurnError, match="too small"):
        Game(cfg, ScriptedBackend([], n_ctx=8192))


def test_server_roundtrip_and_csrf_guard(cfg, example_text):
    from gmhost.server import make_handler
    from http.server import ThreadingHTTPServer
    app = App(cfg, DemoBackend())
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    def post(path, body, hdr=True):
        req = urllib.request.Request(base + path, json.dumps(body).encode(), {"Content-Type": "application/json", **({"X-GM": "1"} if hdr else {})})
        return urllib.request.urlopen(req).read().decode()
    with pytest.raises(urllib.error.HTTPError) as e:
        post("/api/play", {"text": "hi"}, hdr=False)
    assert e.value.code == 403
    ev = [json.loads(l[5:]) for l in post("/api/create", {"name": "web", "background": example_text}).split("\n\n") if l.startswith("data:")]
    assert ev[-1]["type"] == "done"
    post("/api/open", {"name": "web"})
    post("/api/opening", {})
    evs = [json.loads(l[5:]) for l in post("/api/play", {"text": "I ask Nadia about her brother?"}).split("\n\n") if l.startswith("data:")]
    done = evs[-1]["payload"]
    assert done["round"] == 1 and any("YES" in l or "NO" in l for l in done["lines"])
    snap = json.loads(urllib.request.urlopen(base + "/api/campaign").read())
    assert snap["status"]["round"] == 1
    httpd.shutdown()


def test_host_guard_allows_only_local_and_tailnet_names():
    from gmhost.server import host_allowed
    for ok in ("127.0.0.1:8765", "localhost", "[::1]:8765", "100.101.102.103:8765", "pc.tail1234.ts.net"):
        assert host_allowed(ok), ok
    for bad in ("evil.com", "192.168.1.5:8765", "100.200.1.1", "10.0.0.1", ""):
        assert not host_allowed(bad), bad
    assert host_allowed("my.lan", ["my.lan"])


def test_access_token_gates_the_server(cfg, example_text):
    from gmhost.server import make_handler
    from http.server import ThreadingHTTPServer
    import http.client
    cfg.server.token = "s3cret"
    app = App(cfg, DemoBackend())
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    port = httpd.server_address[1]
    def get(path, cookie=None):
        c = http.client.HTTPConnection("127.0.0.1", port); c.request("GET", path, headers={"Cookie": cookie} if cookie else {}); r = c.getresponse(); r.read(); return r
    assert get("/api/info").status == 401
    r = get("/?token=wrong"); assert r.status == 401
    r = get("/?token=s3cret"); assert r.status == 302 and "gm_token=s3cret" in r.getheader("Set-Cookie")
    assert get("/api/info", "gm_token=s3cret").status == 200
    c = http.client.HTTPConnection("127.0.0.1", port); c.request("POST", "/api/save", "{}", {"X-GM": "1", "Content-Type": "application/json"})
    assert c.getresponse().status == 403
    httpd.shutdown()


# ---- guidance turns: "what should I do" / bare "continue" must give a menu, never an invented action --------------
def test_guidance_words_in_both_languages():
    from gmhost import leads
    for t in ["我要做什么", "我现在该做什么？", "接下来怎么办", "有什么线索吗", "what should I do?", "I'm stuck", "any hints"]:
        assert leads.is_guidance(t), t
    for t in ["我去找 Nadia 谈谈", "I walk to the door and continue north", "attack the wolf"]:
        assert not leads.is_guidance(t) and not leads.is_bare_continue(t), t
    for t in ["继续", "继续吧", "continue", "go on"]:
        assert leads.is_bare_continue(t), t


def test_guidance_turn_opens_no_round_and_ends_in_a_menu(cfg, camp):
    game = Game(cfg, DemoBackend())
    r0 = camp.rnd
    for text in ("what should I do?", "continue"):
        res = game.play(camp, text)
        assert camp.rnd == r0 and res.round is None and not res.lines
        assert res.decision and len(res.decision["options"]) >= 2
        assert res.narration


def test_continue_with_a_plan_in_force_is_not_a_guidance_turn(camp):
    from gmhost import leads
    camp.session["plan"] = "walk the route to the docks"
    assert not leads.needs_guidance(camp, "continue")
    camp.session["plan"] = ""
    assert leads.needs_guidance(camp, "continue")


def test_known_leads_use_only_what_the_player_knows(r120):
    from gmhost import leads
    out = "\n".join(leads.known_leads(r120))
    assert "known npcs/teodor_varga" in out and "Jo's blade" in out
    assert "locked_case_truths" not in out and "hidden" not in out.lower()


def test_encoding_can_be_switched_mid_campaign_and_saves_stay_valid(cfg, camp):
    app = App(cfg); app.camp = camp
    app.set_options(encoding="b64")
    assert camp.encoding == "b64"
    with pytest.raises(Exception):
        app.set_options(encoding="rot26")
    r = saves.build_save(camp)
    assert r["round"] == camp.rnd
