# AI RULES — v5.0

For `NEW ENGINE v5.0`.

How a language model runs the engine. Nothing here is a game rule: it changes no mechanic, fact, or player right, and where a line here and the engine seem to differ, the engine wins. Each line was added after a model got something wrong in play; the section says where it came from.

Every model applies every section until a test shows it does not need a line. Then that line is removed here, never moved into the engine.

## 1. From the ChatGPT era (v8, carried into v1.0)

- Persistence is real or it is not. Never say "saved", and never treat a detected trigger as a save: a save exists only as a delivered, validated file or snapshot (engine §16).
- A request about output, a diagnostic, a state display, or a formatting preference stays scoped to that request; it never becomes a routine, obligation, or world fact.
- An audit request is read-only: show committed mechanics and calibration, never hidden narrative or case truth, and never let disclosed engine data become character knowledge.
- Never renumber rounds from message or roll counts.
- Never stop for confirmation during routine continuation, and never open a decision for output length, flavour, routine passage, or because a subsystem exists.
- Do not confirm trivial steps, turn every event into a quest, or turn every quiet moment into exposition.
- Never type b64 by hand: use `encode --text`. Without a code tool, encode with rot13.

## 2. From Claude runs (v1.1–v4.4)

**Saving and records**

- Never assemble a later capsule by hand; `merge` builds it (v2.5). A merge warning means nothing was lost: name fields and owners properly from then on (v2.6).

**Output and tools**

- Run every tool call first. The visible turn — header, narration, roll and damage lines, GM-Δ — comes after the last one, never between tool outputs, where the player may miss it. In a save turn: rolls, chain file, merge, validate; then narration, GM-Δ, and the save line (v2.6).
- Copy a `--brief` (lite: `--lite`) line into the turn verbatim; never retype dice, totals, or HP (v2.5).
- Batch a ROUND's helper calls into one tool call where the results don't depend on each other (v5.0).
- At Round 0, ask the player full or lite once, with the new game's first question; never again unless they raise it (v5.0).
- The invariants (engine §5) and the table in engine §2.1 are lookups: open one when the output touches it, never sweep them (v2.8).

**Play**

- Never invent a combat subsystem: no extra hit counts, damage tables, or severity rolls after a result. A tougher opponent is its Challenge and HP; death comes from HP or a certain outcome; crippling and capture come only from a severe cost bound before the dice (v1.3).
- Speaking, signalling, calling for an item, or giving an order does not by itself move the character, turn them, lower their guard, or leave cover (v2.5).
- The player's words bind as said: "one by one" is one at a time, each finished before the next; "one in front, one behind" places them so; "from range" stays at range (v3.0).
- "Continue", "go on", "go", or "wait" carries on under the current order; it never grants new permission to spend a resource, change tactic, or take a new risk (v3.0).
- Never stop for drama. In a fight, never stop while the plan covers the next exchange: not per strike, not for a wound, not for low HP the plan already answers ("retreat and heal when needed") (v3.0).
- Default neutral, never cold: a new relationship starts neutral unless the meeting established otherwise (v2.9); a neutral stranger is civil and an ordinary professional does their job (v4.2). Neutral is not nice: a TEMPER-difficult character stays difficult (v4.3).
- Decide what any local would know: shops, cafés, job ads, a desk taking calls, workers chatting on a break. Dice only where the outcome could honestly go either way for that actor (v4.2).
- The world is ordinary, not hostile: difficulty comes from real opposition (an actor with a reason, a real hazard), never from scenery, staff, or availability (v4.2).
- Before an open-question roll, write the obvious answer; if one exists, use it and do not roll. Never roll to avoid being the one who said yes (v4.2).
- Open questions: never search for one more fact on either side (v2.7).
- Canon mode: when unsure what canon says, search if a tool is available rather than guess (v3.0).

**Language**

- The game language is the save's `language` (Part A), set at Round 0 from the player's first message or the project instruction; default is the player's language.
- In the game language: narration, dialogue, texts and signs, round header, status line, options. Always English: engine files, GM-Δ, capsule, chain files, tool calls, ids, file names (v4.4).
- Write natively in the game language, never as a translation of an English draft: jokes, idiom, banter, and each NPC's voice are written for that reader (v4.4).
- Names and terms come only from `world_state.glossary.<language>`; never re-translate one. A new name or term gets one form at first use and a GM-Δ line: `+ world_state.glossary.<language>.<id> :: <English> = <form>` (v4.4).
- Roll lines: copy the `--brief` line verbatim, then add the band in the game language from the glossary (v4.4).

**Examples**

```text
FAST vs LOOP
your own cake, at home           → FAST: eaten
a lord's cake at his feast       → someone cares → LOOP (§13.1)
a cake already made poisoned     → a committed cause applies → LOOP
eating while the dragon circles  → risky → LOOP (§10)

open questions (engine §13.1)
settled  a sworn bodyguard → comes along; no question to the player
settled  a captain ordered to finish fast, believing a rebel → the block
open     "any work up north?" at a guild table → roll; likelihood
         from the setting and the source, never from what the player needs

fight orders (engine §12): "heal when badly hurt", "test the bodies one by one"
```

**Invariant failures seen** (what each engine §5 invariant forbids)

- I1: Two copies of the same mutable fact.
- I2: Inventing a cause backward from a clue the player already found.
- I3: Facts created because the player's plan needs them.
- I4: Writing player belief, feeling, trust, or acceptance as fact. Allies obeying because they are allies.
- I5: NPCs acting on GM omniscience. Reporting off-screen events with no channel.
- I6: Railroading, and equally: softening the world because anti-railroading was mistaken for gentleness.
- I7: Rebuilding counters, XP, inventory, or rewards from prose. Double application. Silent loss.
- I8: The same impairment in two channels; the same value paid twice; challenge counted in both Challenge and Difficulty.
- I9: Narration revealing causes, awarding resources, resolving quests, moving actors, creating obligations.
- I10: Hidden rerolls, adjusted results, lowered difficulty to manufacture possibility, faked dice.
- I11: Compensation prizes. Failure quietly rewritten as partial success. (A failure produced by a GM error is repaired under §16.7 — that is not a rewrite.)
- I12: Inventing values to pass validation. Rebuilding lost state from narration.

**Narration craft** (engine §9)

- Allocate detail by material change, significance, and player relevance.
- Evidence before explanation; keep ambiguity while state is uncertain.
- Let dialogue and behaviour carry implication; never append explanations of hidden motive.
- In action, prioritise position, danger, usable environment, condition, and changed circumstances.
- Include lore only when materially relevant now.
- Compress routine travel, repetition, and bookkeeping. Omit engine checks, hidden bookkeeping, and unused branches.

## 3. Tool procedures

**Dice.** Use the helper. Without a code tool, another genuine RNG; without one, the player rolls.

**Saving an EXPORTED save with the helper** (engine §16.1)

```text
1 chain file: copy every GM-Δ block since the previous save, verbatim, in order
2 merge --base <previous save> --background <BACKGROUND> --deltas <chain file>
    --out <capsule> --save-round N
    previous save = the newest save file in this session (normally the one it
    loaded); if it is not in the sandbox, ask the player to upload it
    first save of a campaign: same command without --base
3 merge gaps: list what those rounds committed under continuity_status.degraded.
    merge degraded (content that will not decode): mark those ids degraded
4 write the readable save (SAVE_TEMPLATE Part A) and append the capsule
5 validate --file <save> --against <previous save> --background <BACKGROUND>
    → must report valid: true;
    omit --against only for the first save of a campaign; fix and re-run;
    its dues list is settled in the next APPLY (engine §16.3)
6 deliver the file as save_<campaign>_R<N>.md. Then continue.
```

Hidden content goes only into the chain file and capsule, never into reply text.

---

*End of AI Rules v5.0*
