# How the software splits the work

The engine text is unchanged (`engine/*.md`, `engine/engine_math_v5_0.py`; byte-identical to the originals). The host quotes it to the
model verbatim and takes over everything mechanical.

## Who does what

| Engine duty | Done by |
|---|---|
| Dice, check maths, odds, damage, soak, HP/MP maxima, XP, levels, skill evidence, tiers, clocks, time/date | **code** (via the engine's own helper) |
| Header, roll/damage/answer/odds lines | **code** (the helper's `--brief` output, verbatim) |
| Round numbers, checkpoint cadence S/T, odds-stop, attack budget, dues, one-XP-payout-per-scope, injury homes, temper roll, quest-shape / ambient dice | **code** |
| GM-Δ chain, `merge --background`, `validate --against`, save/load, journal, rollback | **code** |
| Judgement: triage, what is uncertain, challenge/conditions/stakes, what NPCs do, what is committed, what is visible | **referee model** |
| Prose | **narrator model** (sees only what the referee declared visible) |
| Audit of the prose against the invariants | **checker model** + deterministic checks (secret terms, leaked mechanics, language, length) |

## One turn
`triage → LOAD (state slice) → referee tool loop → narrator → checker → PERSIST → checkpoint`
- The referee answers with one JSON tool call at a time (`check`, `ask`, `commit`, `advance_time`, `award_xp`, `close_round`, …),
  constrained by a grammar built from the tool schemas. A tool that breaks an engine rule returns `REFUSED: <reason>` and the model fixes it.
- The turn is transactional: any failure before commit restores the campaign exactly.
- `close_round` is refused while the host still lists unresolved items (due plans/clocks, lasting injuries, temper).

## GM cards are never shortened
`gmhost/cards.py` cuts `NEW_ENGINE_v5_0.md` at its own headings. Always sent: Part 0 and AI_RULES §1–2. The §2.1 routing table is
parsed from the engine file; triage picks rows, the matching sections are inserted verbatim, and the referee can `open_cards` any other.
Persistence (§16) is run by code, so only §16.6/16.7 reach the model. If the context is too small the app refuses to start rather than trim.
`tests/test_cards.py` asserts every card is a verbatim slice.

## Truth lives once
`readable` (Part A) + capsule. The live capsule view is always computed by the helper's `merge` over previous save + chain, the same
computation a save performs, so play and save cannot drift. Saves are validated with `validate --against` before they are delivered.

## Known limits (v0.1)
- No real model was run during development (the build sandbox blocked model downloads); behaviour with real models is untested.
  The llama.cpp grammar compiler was verified to accept the tool schemas.
- Not implemented: §16.7 replay/undo, module B/C-specific code (their rules reach the model as cards), NPC skill growth,
  non-player participants' XP beyond companions with `capability.progression`.
- Incidental combatants live in memory only (engine: interaction state); a save mid-fight does not carry them.
