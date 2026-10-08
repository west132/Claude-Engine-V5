import pytest

from gmhost import schema as sch
from gmhost.campaign import Entry
from gmhost.tools import REGISTRY
from gmhost.turnctx import TurnCtx, ToolError, Hurtable
from gmhost.cards import Engine


@pytest.fixture
def ctx(camp, cfg):
    return TurnCtx(camp, "test", engine=Engine(cfg.engine_dir))


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
             skills_exercised=["crossbow"])
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
    assert any(l.startswith("Damage: 1d6 (4) − soak 1 = 3 | Ilsa Venn HP 14 → 11") for l in ctx.lines)
    assert ctx.camp.player["condition"]["hp"] == 11
    assert ctx.camp.session["combat"]["wolf1"]["attacks_left"] == 0
    with pytest.raises(ToolError, match="no attack left"):
        call(ctx, "damage", target_id="player", kind="creature", size="man_sized", source_id="wolf1", reason="second bite")


def test_severe_with_two_attackers_each_hit_once_lone_hits_twice(ctx, dice):
    register(ctx, "wolf1"); register(ctx, "wolf2")
    dice(1, 1, 4, 4)
    call(ctx, "check", **harm_args("severe", engaged_ids=["wolf1", "wolf2"]))
    assert ctx.camp.player["condition"]["hp"] == 14 - 3 - 3
    c2 = TurnCtx(ctx.camp, engine=ctx.engine)
    ctx.camp.player["condition"]["hp"] = 14
    ctx.camp.session["combat"].pop("wolf2")
    dice(1, 1, 4, 4)
    call(c2, "check", **harm_args("severe", source_id="wolf1"))
    assert ctx.camp.player["condition"]["hp"] == 14 - 3 - 3


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
    assert "XP +76" in out and ctx.camp.player["progression"]["state"]["xp"] == 76
    ctx.camp.commit_block(ctx.camp.make_block(1, list(ctx.entries)))
    ctx2 = TurnCtx(ctx.camp, engine=ctx.engine)
    with pytest.raises(ToolError, match="already paid"):
        call(ctx2, "award_xp", kind="combat", scope_id="wolf_fight", scope="meaningful", challenges=[3], participants=["player"])


def test_level_up_carries_xp(ctx):
    ctx.camp.player["progression"]["state"] = {"level": 3, "xp": 200}
    call(ctx, "award_xp", kind="event", scope_id="evt1", scope="meaningful", challenges=[3], participants=["player"])
    assert ctx.camp.player["progression"]["state"] == {"level": 4, "xp": 18}      # 238 - 220


# ---- commit ------------------------------------------------------------------------------------
def test_commit_rules(ctx, dice):
    with pytest.raises(ToolError, match="name the field"):
        call(ctx, "commit", entries=[{"op": "~", "id": "npcs.oda_brandt", "content": "now angry"}])
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
def test_time_rolls_the_iso_date_and_fires_dues(ctx):
    out = call(ctx, "advance_time", minutes=1470, activity="a long wait")
    assert ctx.camp.time["date"] == "2026-03-02" and ctx.camp.time["clock_minutes"] == 480
    assert "Corvin Hale" in out and "due:npcs.corvin_hale" in ctx.must_settle
    with pytest.raises(ToolError, match="settle"):
        call(ctx, "close_round", opened_round=True, visible=["Time passes."])
    call(ctx, "commit", entries=[{"op": "~", "id": "npcs.corvin_hale.state.due", "content": "2026-03-04 08:00"}])
    assert call(ctx, "close_round", opened_round=True, visible=["Time passes."]) == "closed"


def test_clock_check_does_the_arithmetic(ctx):
    call(ctx, "advance_time", minutes=5 * 1440, activity="days pass")
    assert "clock:brine_winds" in ctx.must_settle
    out = call(ctx, "clock_check", pressure_id="brine_winds", process_operated=True, accelerated=True,
               next_due="2026-03-11 06:00", reason="winds keep rising")
    assert "1 → 3/6" in out
    assert ctx.get("active_world_pressures.brine_winds.clock.filled") == 3
    with pytest.raises(ToolError, match="future"):
        call(ctx, "clock_check", pressure_id="brine_winds", process_operated=False, next_due="2026-03-01 06:00", reason="x" * 6)


def test_non_iso_calendar_demands_a_date_on_rollover(ctx):
    ctx.camp.time["date"] = "Year 3, Frostmonth 2"
    with pytest.raises(ToolError, match="date"):
        call(ctx, "advance_time", minutes=1500, activity="a long journey")
    call(ctx, "advance_time", minutes=1500, activity="a long journey", date="Year 3, Frostmonth 3")
    assert ctx.camp.time["date"] == "Year 3, Frostmonth 3"


def test_rest_recovers_by_the_engine_rules(ctx):
    ctx.camp.player["condition"].update(hp=2, mp=3)
    call(ctx, "rest", hours=2, quality="short")
    assert ctx.camp.player["condition"]["hp"] == 2 + 3 + 3          # quarter of 14, rounded down = 3 per hour
    assert ctx.camp.player["condition"]["mp"] == 3                  # rest_only: no short-rest MP
    call(ctx, "rest", hours=8, quality="full_night")
    assert ctx.camp.player["condition"]["hp"] == 14 and ctx.camp.player["condition"]["mp"] == 10


# ---- player block -------------------------------------------------------------------------------
def test_money_resources_and_locations(ctx, dice):
    with pytest.raises(ToolError, match="not enough"):
        call(ctx, "player_update", kind="money", data={"delta": {"silver": -99}}, reason="buying a horse")
    call(ctx, "player_update", kind="money", data={"delta": {"silver": -4}}, reason="a night's room")
    assert ctx.camp.player["money"]["silver"] == 10
    dice(1)
    out = call(ctx, "player_update", kind="resource", data={"resource_id": "rations", "op": "draw"}, reason="a day's travel")
    assert "steps down to d4" in out and ctx.camp.player["resources"]["rations"]["usage_die"] == "d4"
    call(ctx, "player_update", kind="resource", data={"resource_id": "bolts", "op": "spend", "amount": 3}, reason="shooting")
    assert ctx.camp.player["resources"]["bolts"]["count"] == 15
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
    out = call(ctx, "cast", tier="T1", power="hedge-charm of warmth")
    assert ctx.camp.player["condition"]["mp"] == 7 and "7/10" in out
    with pytest.raises(ToolError, match="above the caster's tier"):
        call(ctx, "cast", tier="T2", power="greater charm")


def test_schema_validator_catches_bad_shapes():
    errs = sch.validate({"op": "x", "id": "a"}, REGISTRY["commit"].schema["properties"]["entries"]["items"])
    assert any("op" in e for e in errs) and any("content" in e for e in errs)
