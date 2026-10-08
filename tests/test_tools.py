import pytest

from gmhost import schema as sch
from gmhost.campaign import Entry
from gmhost.tools import REGISTRY
from gmhost.turnctx import TurnCtx, ToolError, Hurtable
from gmhost.cards import Engine


@pytest.fixture
def ctx(r120, cfg):
    """Tools run against the user's real campaign at R120 (Rin Hale, level 4, HP 16, MP 16)."""
    return TurnCtx(r120, "test", engine=Engine(cfg.engine_dir))


def call(ctx, tool_name, **args):
    t = REGISTRY[tool_name]
    errs = sch.validate(args, t.schema)
    if errs:
        raise ToolError("; ".join(errs))
    return t.fn(ctx, args)


def check_args(**over):
    a = dict(action="shoot the wolf", why_uncertain="moving target in poor light",
             capability={"mode": "numeric", "cmp": 4, "challenge": 3, "basis": "open ground"},
             conditions=[{"category": "sensory", "value": 1, "fact": "dim light before dawn"}],
             stakes={"cost": "setback", "cost_text": "the wolf closes the distance", "reach": "full", "reach_text": "the wolf is hit"},
             skills_exercised=["close_combat"])
    a.update(over)
    return a


def register(ctx, id="wolf1", **kw):
    args = dict(action="add", id=id, name=f"wolf {id}", side="foe", size="normal", v=2,
                damage_kind="creature", damage_size="man_sized", soak="none", attacks=1)
    args.update(kw)
    return call(ctx, "combat", **args)


# ---- check --------------------------------------------------------------------------------
def test_numeric_check_prints_the_helpers_own_line(ctx, dice):
    dice(5, 6)
    out = call(ctx, "check", **check_args())
    assert ctx.lines[0].startswith("2d10: 5+6 | Capability: +0 | Tool: +0 | Total: 11")
    assert "Difficulty: 11 [open ground] | Stakes: setback/full | Outcome: Success" in ctx.lines[0]
    assert "SUCCESS" in out


def test_challenge_gap_sets_capability_not_the_model(ctx, dice):
    dice(5, 6)
    call(ctx, "check", **check_args(capability={"mode": "numeric", "cmp": 9, "challenge": 3}, conditions=[]))
    assert "Capability: +4" in ctx.lines[0]


def test_host_computes_player_capability_from_skill_and_gear(ctx, dice):
    dice(5, 6)
    call(ctx, "check", **check_args(capability={"mode": "numeric", "skill_id": "close_combat", "challenge": 6}, conditions=[]))
    assert "Capability: +0" in ctx.lines[-1]                       # level 4 + T2 bonus 2 = 6 vs 6
    call(ctx, "check", **check_args(capability={"mode": "numeric", "skill_id": "close_combat", "challenge": 2}, conditions=[]))
    assert "Capability: +2" in ctx.lines[-1]                       # 6 vs 2: Δ+4
    out = call(ctx, "check", **check_args(capability={"mode": "numeric", "skill_id": "close_combat", "gear_item_id": "nightglass_blade", "challenge": 5}, conditions=[]))
    assert "Capability: +2" in ctx.lines[-1]                       # T2 blade +1: 7 vs 5 (without it 6 vs 5 = +0)
    with pytest.raises(ToolError, match="never also a ToolMod"):
        call(ctx, "check", **check_args(capability={"mode": "numeric", "skill_id": "close_combat", "gear_item_id": "nightglass_blade", "challenge": 5},
                                        tool={"fit": 1, "source": "good grip"}))


def test_numeric_mode_refuses_base_and_missing_facts(ctx):
    with pytest.raises(ToolError, match="drop capmod/base"):
        call(ctx, "check", **check_args(capability={"mode": "numeric", "cmp": 4, "challenge": 3, "base": 12}))
    with pytest.raises(ToolError, match="fact"):
        call(ctx, "check", **check_args(conditions=[{"category": "time", "value": 1, "fact": "x"}]))
    with pytest.raises(ToolError, match="counted twice"):
        call(ctx, "check", **check_args(conditions=[{"category": "time", "value": 1, "fact": "the bell is ringing"},
                                                    {"category": "time", "value": 1, "fact": "the gate closes soon"}]))


def test_odds_stop_then_resume_rolls_the_bound_check(ctx, dice):
    a = check_args(capability={"mode": "absolute", "capmod": 0, "base": 15}, conditions=[],
                   stakes={"cost": "severe", "cost_text": "you fall and are crippled", "reach": "full", "reach_text": "across"})
    out = call(ctx, "check", **a)
    assert ctx.stopped_for_odds and "ODDS STOP" in out and ctx.lines[0].startswith("shoot the wolf — about ")
    assert ctx.camp.session["pending_odds"]
    dice(9, 9)
    ctx.stopped_for_odds = False
    call(ctx, "resume_check")
    assert "Total: 18" in ctx.lines[-1] and ctx.camp.session["pending_odds"] is None


def test_no_odds_stop_when_an_order_covers_the_risk(ctx, dice):
    dice(1, 1)
    a = check_args(capability={"mode": "absolute", "capmod": 0, "base": 17}, conditions=[],
                   context={"covered_by_order": True})
    call(ctx, "check", **a)
    assert not ctx.stopped_for_odds and "Total: 2" in ctx.lines[0]


# ---- harm, attack budget -----------------------------------------------------------------------
def harm_args(cost="loss", **h):
    return check_args(stakes={"cost": cost, "cost_text": "the wolf bites", "reach": "partial", "reach_text": "a foothold", "harm": True},
                      harm=h, context={"in_combat": True, "covered_by_order": True})


def test_failed_check_costs_one_hit_with_soak_and_spends_the_attack(ctx, dice):
    register(ctx)
    dice(1, 1, 4)                                   # fail, then 1d6 = 4 ; leather = soak 1
    call(ctx, "check", **harm_args(source_id="wolf1"))
    assert any(l.startswith("Damage: 1d6 (4) − soak 1 = 3 | Rin Hale HP 16 → 13") for l in ctx.lines)
    assert ctx.camp.player["condition"]["hp"] == 13
    assert ctx.camp.session["combat"]["wolf1"]["attacks_left"] == 0
    with pytest.raises(ToolError, match="no attack left"):
        call(ctx, "damage", target_id="player", kind="creature", size="man_sized", source_id="wolf1", reason="second bite")


def test_severe_with_two_attackers_each_hit_once_lone_hits_twice(ctx, dice):
    register(ctx, "wolf1"); register(ctx, "wolf2")
    dice(1, 1, 4, 4)
    call(ctx, "check", **harm_args("severe", engaged_ids=["wolf1", "wolf2"]))
    assert ctx.camp.player["condition"]["hp"] == 16 - 3 - 3
    c2 = TurnCtx(ctx.camp, engine=ctx.engine)
    ctx.camp.player["condition"]["hp"] = 16
    ctx.camp.session["combat"].pop("wolf2")
    dice(1, 1, 4, 4)
    call(c2, "check", **harm_args("severe", source_id="wolf1"))
    assert ctx.camp.player["condition"]["hp"] == 16 - 3 - 3


def test_hit_on_success_damages_the_engaged_opponent(ctx, dice):
    register(ctx)
    dice(10, 10, 5)                                 # success, bow 1d8 = 5
    call(ctx, "check", **check_args(target_id="wolf1", attack={"kind": "weapon", "size": "bow"},
                                    stakes={"cost": "setback", "cost_text": "it closes in", "reach": "full", "reach_text": "wolf hit"},
                                    context={"in_combat": True, "covered_by_order": True}))
    assert ctx.camp.session["combat"]["wolf1"]["hp"] == 12 - 5     # V2 → 8+4


def test_unregistered_attacker_is_refused(ctx):
    with pytest.raises(ToolError, match="not registered"):
        call(ctx, "check", **harm_args(source_id="ghost"))


def test_lasting_injury_must_be_recorded_before_closing(ctx, dice):
    ctx.camp.player["condition"]["hp"] = 7
    dice(5)
    call(ctx, "damage", target_id="player", kind="hazard", size="grave", reason="a rockfall")   # 4d6 clamps to 5s = 20-1
    assert ctx.camp.player["condition"]["hp"] == 0 and "injury:player" in ctx.must_settle
    close = dict(opened_round=True, visible=["The ledge collapses and the rock crushes your leg."])
    with pytest.raises(ToolError, match="LASTING INJURY"):
        call(ctx, "close_round", **close)
    with pytest.raises(ToolError, match="home"):
        call(ctx, "player_update", kind="injury_add", data={"injury": "crushed leg", "effect": "slow"}, reason="rockfall")
    call(ctx, "player_update", kind="injury_add", data={"injury": "crushed leg", "home": "position",
                                                         "effect": "position +1 on footwork-dependent actions"}, reason="rockfall")
    assert call(ctx, "close_round", **close) == "closed"


def test_down_player_cannot_rest_and_dies_on_damage(ctx, dice):
    ctx.camp.player["condition"]["hp"] = 0
    with pytest.raises(ToolError, match="down"):
        call(ctx, "rest", hours=1, quality="short")
    dice(3)
    call(ctx, "damage", target_id="player", kind="weapon", size="light", reason="a stab")
    assert ctx.camp.session["ended"] and ctx.camp.player["status"] == "dead"


# ---- xp ---------------------------------------------------------------------------------------
def test_xp_is_paid_once_per_scope(ctx):
    out = call(ctx, "award_xp", kind="combat", scope_id="wolf_fight", scope="meaningful", challenges=[3, 3], participants=["player"])
    assert "XP +58" in out and ctx.camp.player["progression"]["state"]["xp"] == 221 + 58      # R3 vs level 4: ×0.75 each
    ctx.camp.commit_block(ctx.camp.make_block(ctx.camp.rnd + 1, list(ctx.entries)))
    ctx2 = TurnCtx(ctx.camp, engine=ctx.engine)
    with pytest.raises(ToolError, match="already paid"):
        call(ctx2, "award_xp", kind="combat", scope_id="wolf_fight", scope="meaningful", challenges=[3], participants=["player"])


def test_level_up_carries_xp(ctx):
    ctx.camp.player["progression"]["state"] = {"level": 4, "xp": 280}
    call(ctx, "award_xp", kind="event", scope_id="evt1", scope="meaningful", challenges=[3], participants=["player"])
    assert ctx.camp.player["progression"]["state"] == {"level": 5, "xp": 12}      # 280+29 = 309 - 297


# ---- commit ------------------------------------------------------------------------------------
def test_commit_rules(ctx, dice):
    with pytest.raises(ToolError, match="name the field"):
        call(ctx, "commit", entries=[{"op": "~", "id": "npcs.nadia_voss", "content": "now angry"}])
    with pytest.raises(ToolError, match="readable save"):
        call(ctx, "commit", entries=[{"op": "~", "id": "player.condition.hp", "content": "3"}])
    with pytest.raises(ToolError, match="not an engine owner"):
        call(ctx, "commit", entries=[{"op": "+", "id": "monsters.wolf", "content": "x"}])
    with pytest.raises(ToolError, match="identity fields"):
        call(ctx, "commit", entries=[{"op": "+", "id": "npcs.mira", "content": '{"name": "Mira"}'}])
    dice(10, 10)                                    # temper roll 20 ≥ 17: difficult
    out = call(ctx, "commit", entries=[{"op": "+", "id": "npcs.mira", "hidden": False, "content":
              '{"name": "Mira", "job": "ostler", "belongs": [], "gender": "female", "character": "tidy"}'}])
    assert "TEMPER" in out and "temper:npcs.mira" in ctx.must_settle
    call(ctx, "commit", entries=[{"op": "+", "id": "npcs.mira.temper", "content": "greedy: haggles over every coin"}])
    assert not ctx.must_settle
    assert ctx.get("npcs.mira")["name"] == "Mira"


def test_secret_terms_are_collected(ctx):
    call(ctx, "commit", entries=[{"op": "+", "id": "locked_case_truths.poison", "content": '{"cause": "arsenic in the well"}',
                                  "secret_terms": ["arsenic"]}])
    assert "arsenic" in ctx.secret_terms


# ---- time, dues, clocks -----------------------------------------------------------------------
def test_time_rolls_the_iso_date_and_day_index(ctx):
    assert ctx.camp.time["date"] == "2026-11-01" and ctx.camp.time["clock_minutes"] == 1300
    call(ctx, "advance_time", minutes=1470, activity="a long wait")                  # 21:40 + 24h30 -> 22:10 next day
    t = ctx.camp.time
    assert t["clock_minutes"] == 1330
    assert t["day_index"] == 27 and t["date"] == "2026-11-02"


def test_clock_due_fires_and_check_does_the_arithmetic(ctx):
    # the import repaired glass_spread: filled 4/6, due 2026-11-03 (it held prose before)
    assert ctx.get("active_world_pressures.glass_spread.clock.filled") == 4
    out = call(ctx, "advance_time", minutes=2 * 1440 + 180, activity="days pass")
    assert "clock:glass_spread" in ctx.must_settle
    with pytest.raises(ToolError, match="settle"):
        call(ctx, "close_round", opened_round=True, visible=["Time passes."])
    with pytest.raises(ToolError, match="future"):
        call(ctx, "clock_check", pressure_id="glass_spread", process_operated=False, next_due="2026-11-01 06:00", reason="x" * 6)
    out = call(ctx, "clock_check", pressure_id="glass_spread", process_operated=True, accelerated=True,
               next_due="2026-11-10 06:00", reason="stones moving again")
    assert "4 → 6/6" in out and "FULL" in out
    assert ctx.get("active_world_pressures.glass_spread.clock.filled") == 6
    assert "clock:glass_spread" not in ctx.must_settle


def test_non_iso_calendar_demands_a_date_on_rollover(ctx):
    ctx.camp.time["date"] = "Year 3, Frostmonth 2"
    with pytest.raises(ToolError, match="date"):
        call(ctx, "advance_time", minutes=1500, activity="a long journey")
    call(ctx, "advance_time", minutes=1500, activity="a long journey", date="Year 3, Frostmonth 3")
    assert ctx.camp.time["date"] == "Year 3, Frostmonth 3"


def test_rest_recovers_by_the_engine_rules(ctx):
    ctx.camp.player["condition"].update(hp=2, mp=3)
    call(ctx, "rest", hours=2, quality="short")
    assert ctx.camp.player["condition"]["hp"] == 2 + 4 + 4          # quarter of 16 = 4 per hour
    assert ctx.camp.player["condition"]["mp"] == 3                  # Ashfall MP is `fast`, but only when out of danger
    call(ctx, "rest", hours=1, quality="short", out_of_danger=True)
    assert ctx.camp.player["condition"]["mp"] == 16                 # fast: full after ~10 min out of danger
    call(ctx, "rest", hours=8, quality="full_night")
    assert ctx.camp.player["condition"]["hp"] == 16


# ---- player block -------------------------------------------------------------------------------
def test_money_resources_and_locations(ctx, dice):
    assert ctx.camp.player["money"]["cash_and_accessible_funds"] == 6588
    with pytest.raises(ToolError, match="not enough"):
        call(ctx, "player_update", kind="money", data={"delta": -99999}, reason="buying a car")
    call(ctx, "player_update", kind="money", data={"delta": -88}, reason="a night's room")
    assert ctx.camp.player["money"]["cash_and_accessible_funds"] == 6500
    dice(1)
    out = call(ctx, "player_update", kind="resource", data={"resource_id": "first_aid_supplies", "op": "draw"}, reason="a day's travel")
    assert "steps down to d4" in out and ctx.camp.player["resources"]["first_aid_supplies"]["usage_die"] == "d4"
    call(ctx, "player_update", kind="resource", data={"resource_id": "rounds", "op": "add", "name": "pistol rounds", "tracking": "exact", "amount": 18}, reason="bought a box")
    call(ctx, "player_update", kind="resource", data={"resource_id": "rounds", "op": "spend", "amount": 3}, reason="shooting")
    assert ctx.camp.player["resources"]["rounds"]["count"] == 15
    with pytest.raises(ToolError, match="unknown location"):
        call(ctx, "player_update", kind="location", data={"id": "pellam"}, reason="travel")
    call(ctx, "commit", entries=[{"op": "+", "id": "locations.pellam", "content": '{"name": "Pellam"}', "hidden": False}])
    with pytest.raises(ToolError, match="challenge_band"):
        call(ctx, "player_update", kind="location", data={"id": "pellam"}, reason="travel")
    call(ctx, "commit", entries=[{"op": "+", "id": "locations.pellam.challenge_band",
                                  "content": '{"min": 1, "max": 3, "basis": "small market town, one watch post"}'}])
    call(ctx, "player_update", kind="location", data={"id": "pellam"}, reason="travel")
    assert ctx.camp.readable["world_state"]["location"] == "pellam"


def test_cast_and_mp(ctx):
    out = call(ctx, "cast", tier="T1", power="a small surge")
    assert ctx.camp.player["condition"]["mp"] == 13 and "13/16" in out          # T1 costs 3
    call(ctx, "cast", tier="T2", power="demonic_surge")                         # T2 costs 6 and Rin's best MP skill is T2
    assert ctx.camp.player["condition"]["mp"] == 7
    with pytest.raises(ToolError, match="above the caster's tier"):
        call(ctx, "cast", tier="T3", power="greater surge")


def test_schema_validator_catches_bad_shapes():
    errs = sch.validate({"op": "x", "id": "a"}, REGISTRY["commit"].schema["properties"]["entries"]["items"])
    assert any("op" in e for e in errs) and any("content" in e for e in errs)
