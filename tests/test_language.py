# Copyright (c) 2026 West132.WL. All rights reserved.
import pytest

from gmhost import i18n
from gmhost.app import App
from gmhost.campaign import CampaignError


def test_default_is_english_and_unset(cfg):
    p = App(cfg).prefs()
    assert p == {"language": "en", "language_set": False}


def test_choice_is_remembered_across_restart(cfg):
    App(cfg).set_language("zh_hans")
    p = App(cfg).prefs()
    assert p == {"language": "zh_hans", "language_set": True}
    assert App(cfg).info()["defaults"]["language"] == "zh_hans"


def test_only_english_and_chinese(cfg):
    assert set(i18n.LANGUAGES) == {"en", "zh_hans"}
    with pytest.raises(CampaignError):
        App(cfg).set_language("fr")


def test_chinese_line_and_status_follow_glossary():
    assert i18n.localize_line("… → NO, BUT", "zh_hans").endswith("（否，但是）")
    assert i18n.localize_line("… → NO, BUT", "en") == "… → NO, BUT"
    s = i18n.localize_status("HP 16 → 11/16", "zh_hans")
    assert "生命" in s and "HP" not in s
