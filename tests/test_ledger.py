from gmhost.campaign import Campaign, Entry


def test_initial_vitals_come_from_the_engine_tables(camp):
    c = camp.player["condition"]
    assert (c["hp"], c["mp"]) == (14, 10)            # level 3: 8+2*3 ; MP 2*3 + 4*T1(1)


def test_overlay_is_the_helpers_merge(camp):
    b = camp.make_block(1, [Entry("~", "npcs.corvin_hale.state.position", "marrowgate_cracked_pot", False),
                            Entry("+", "locked_case_truths.pack", '{"cause": "hungry", "state": {}}')])
    assert camp.get("npcs.corvin_hale.state.position", b) == "marrowgate_cracked_pot"
    assert camp.get("npcs.corvin_hale.state.position") == "marrowgate_salt_gate"      # not committed yet
    camp.commit_block(b)
    assert camp.get("locked_case_truths.pack")["cause"] == "hungry"
    assert camp.records()["npcs.corvin_hale.state.position"].startswith("R1:")


def test_retired_background_paths_stay_gone(camp):
    camp.commit_block(camp.make_block(1, [Entry("-", "npcs.oda_brandt", "left town for good")]))
    assert camp.get("npcs.oda_brandt") is None
    assert "npcs.oda_brandt" in [r for r, _ in camp._merge_view(None)[1]]


def test_keyed_record_under_a_background_list(camp):
    camp.commit_block(camp.make_block(1, [Entry("+", "world_state.material_history.xp_fight1", "paid 38")]))
    assert "xp_fight1" in camp.get("world_state.material_history")


def test_block_headers_name_the_previous_round(camp):
    camp.commit_block(camp.make_block(1, [Entry("+", "trackers.t1", '{"name": "x", "current": 0, "target": 3}')]))
    camp.commit_block(camp.make_block(2, []))
    txt = camp.chain_text()
    assert "GM-Δ 1 ⟵ 0" in txt and "GM-Δ 2 none" in txt


def test_journal_roundtrip(cfg, camp):
    camp.commit_block(camp.make_block(1, [Entry("+", "trackers.t1", '{"name": "x", "current": 0, "target": 3}')]))
    camp.write_journal()
    again = Campaign.open(cfg, "t")
    assert again.get("trackers.t1")["target"] == 3 and again.readable == camp.readable


def test_encoded_chain_still_merges(cfg, example_text):
    c = Campaign.create(cfg, "enc", example_text, encoding="b64")
    c.commit_block(c.make_block(1, [Entry("+", "trackers.t1", '{"name": "x", "current": 0, "target": 3}')]))
    assert "enc:b64" in c.chain_text()
    assert c.get("trackers.t1")["name"] == "x"
