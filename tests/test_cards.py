from gmhost.cards import Engine, PLAIN_EXCLUDES


def eng(cfg): return Engine(cfg.engine_dir)


def test_routing_table_is_read_from_the_engine(cfg):
    e = eng(cfg)
    assert len(e.routes) == 22
    assert e.routes[0].description == "player attempts something material" and e.routes[0].refs == ["10"]
    assert next(r for r in e.routes if "module" in r.description).refs == ["A", "B", "C", "D"]


def test_every_card_is_a_verbatim_slice_of_the_engine_file(cfg):
    e = eng(cfg)
    cards = e.cards_for([r.id for r in e.routes], {"numeric_level_xp": True, "equipment_power_tiers": True,
                                                     "bounded_scenario_endings": True, "flexible_item_entitlement": True})
    assert len(cards) > 12
    for c in cards:
        if c.ref not in PLAIN_EXCLUDES:
            assert c.text in e.text, f"card §{c.ref} is not verbatim"
    assert e.part0_text() in e.text


def test_part0_is_whole_and_has_the_invariants(cfg):
    p0 = eng(cfg).part0_text()
    assert p0.startswith("# PART 0") and "I12 DEGRADE HONESTLY" in p0 and "## 9. Narration" in p0
    assert "# PART 1" not in p0


def test_vitals_card_is_routed_separately_from_action_resolution(cfg):
    e = eng(cfg)
    assert "### 10.5" not in e.card_by_ref("10").text
    assert "### 10.5" in e.card_by_ref("10.5").text


def test_module_cards_only_when_enabled(cfg):
    e = eng(cfg)
    assert e.cards_for(["r22"], {}) == []
    assert [c.ref for c in e.cards_for(["r22"], {"numeric_level_xp": True})] == ["A"]


def test_host_only_persistence_section_is_not_sent_to_the_model(cfg):
    e = eng(cfg)
    assert e.cards_for(["r18"], {}) == []
    assert [c.ref for c in e.cards_for(["r19", "r20"], {})] == ["16.6", "16.7"]


def test_ai_rules_blocks(cfg):
    e = eng(cfg)
    assert "game language is the save's `language`" in e.rules_block("Language")
    assert "Allocate detail by material change" in e.rules_block("Narration craft")
    assert "I9: Narration revealing causes" in e.rules_block("Invariant failures seen")
