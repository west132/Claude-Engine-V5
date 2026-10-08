# Roadmap

Copyright (c) 2026 West132.WL. All rights reserved.

Ideas for later versions. None of this is built yet. Do it only after the base game has been tested with a 7B+ instruct model.

## Role agents: NPCs and the world as separate AI calls

Today one referee call does most of the judging. The idea is to split the thinking into smaller roles that each see only what they should, then merge their proposals in the main GM step.

### Who gets an agent

Not every NPC is worth a model call. Three tiers, decided by code, not by the AI:

| Tier | Who | Treatment |
|---|---|---|
| Principals | The main NPCs built in the BACKGROUND (the recorded ones) | Own agent when they act or speak, plus off-screen plans advanced when time passes |
| Of interest | NPCs the player character shows interest in: asked about, spoken to repeatedly, investigated, followed, named in the player's actions | Promoted to an agent after code sees enough interest (a simple counter, or the player says so). Promotion creates a proper NPC record |
| Everyone else | Crowds, clerks, passers-by | No agent. The referee and narrator handle them in the scene |

### Roles

- **NPC agent:** sees only that NPC's card (goals, knowledge, relationships) and the visible scene. Returns what they say and do, and what they would try. Does not know the player's secrets or other NPCs' secrets.
- **World agent:** runs only when time advances. Moves factions, clocks and off-screen events. Proposes, never decides.
- **Main GM (referee):** collects proposals, decides what is uncertain and what is at stake, then calls the dice and tools. Resolves contradictions between agents.
- **Code:** rolls dice, applies damage, XP, time, clocks and saves. Unchanged.
- **Narrator and checker:** unchanged. The checker is the last guard against invented facts and leaked secrets.

### Why it should fit

- Each agent gets a small context (one card plus the scene), so 32K is plenty.
- The same model can play every role with a different prompt, so no extra video memory.
- It matches the engine's rule that characters act only on what they know.

### Costs and risks

- Every agent is another model call, so turns get slower. Limit calls to NPCs who act or speak in the scene, and the world agent to time passing.
- Agents can contradict each other or invent facts. The referee must reconcile, and the checker stays on.
- Small models will write weak NPC replies; test on 7B+ first.

### Suggested order

1. Principal NPC agents when they are in the scene.
2. Interest counter and promotion of NPCs the player cares about.
3. World agent when time advances.
4. Parallel calls, if the backend supports them.

## Engine changes for software use (proposed, to decide)

The engine was written for a chat page, where one AI does everything. These are the places where I found, by reading the engine and running it against your 120-round campaign, that a software edition could be clearer or safer. Each item says what I checked. The five files in `engine/` stay untouched until you approve a new version.

### Gaps in the engine text

- **Round header wording per language.** AI_RULES says the round header is written in the game language, and the glossary covers names, terms and roll bands, but nothing defines the header's own words (ROUND, saved, save). The host picked 第 N 回合 / 已存 / 下次存档 itself. Add these labels to the glossary.
- **Which skill draws MP, and what MP a skill gives.** Max MP is `2V + 4 × tier bonus` of "the best MP-drawing skill" (§10.5), and the BACKGROUND lists `mp_powers.draws_mp` as free text. Nothing says how a skill is marked as MP-drawing, so the host matches names against skill ids and ability text. Decision from West132.WL: skills have a class (normal, elite, legendary) and levels, and MP should follow them, with a small dice roll allowed (for example +1d3). One hard rule: a low-level skill must never become unusable for a high-level player. See "Design decisions" below.
- **Injury on an unrecorded actor.** §10.5 says a hit of half max HP or more, or reaching 0 HP, adds an injury record with a home and effect. §13.1 says incidental actors have no persistent record. The text does not say what happens when an incidental actor takes such a hit. Covered by the death rule below.
- **Readable lint does not check types.** `validate` checks enum values, duplicate keys, missing NPC identity fields and injuries without a home. It does not check that numeric or date fields actually hold numbers or dates. Your imported chat saves had words in such fields, which the host repairs on import. Add type checks to the lint.
- **Capsule scanner reads `id:` as a record.** The helper treats a line that starts with `id:` as a capsule record. The save template avoids this by writing `background_ref: {id: }` on one line; I confirmed that writing it on two lines is read as a record named after the id. The fix, suggested by West132.WL, is the usual one in code: explicit open and close markers. See "Design decisions" below.

### Design decisions (from West132.WL, to be written into a new engine version)

**1. Skills and MP.**
- MP comes from the skill's class (NORMAL / ELITE / LEGENDARY) and level. A one-time dice bonus (for example 1d3, rolled when the skill is gained or grows) is allowed. Because §10.5 says max MP is derived and never stored, the rolled bonus must be stored once.
- Floor rule: powers are costed by their own tier, not by the player's level, and the engine must guarantee that a low-tier power stays castable by a higher-level player (for example: any caster can always afford at least a few uses of a power at or below their tier).
- `draws_mp` should list skill ids so there is no guessing.

**2. Essential NPCs and death (borrowed from Skyrim).**
- Main NPCs are marked essential until their mission ends (for example `essential_until: <quest id>` in the BACKGROUND). While the mission is open, an essential NPC at 0 HP is down, captured, fleeing or yielding, never dead.
- When the mission ends the mark is removed, and from then on all NPCs follow the same rule: at 0 HP they are dying and are killed unless someone helps at once.
- This is a change from the current engine, where 0 HP is "down" and an untreated actor gets a survival roll after an hour (§10.5), and from the README's "nobody has plot armour". It should be an opt-in world setting so existing worlds behave as before. The player is not essential.
- It also settles injuries on incidental actors: they are ordinary NPCs, so the normal death rule applies and no record is needed.

**3. Saves.**
- Keep the readable text save and capsule as the export and exchange format, because it is what chat saves and your 120-round campaign use.
- Under it, keep a structured save that the host owns: JSON or SQLite with a schema version, a checksum, safe writing (write to a temporary file, then replace) and automatic backups. Industry practice for game saves is a versioned structured format with migrations, plus backups, and that is what this adds.
- "As detailed as possible" is best met by the history, not by a bigger text save: every round's rolls, GM-Δ, narration and tool results. That is what makes undo, replay and audits possible. The host already keeps a journal per round; this would make it a documented format.
- The text save keeps the engine's rule that nothing is held twice and no fact exists only in the save.

**4. Capsule scanner and explicit markers.**
- Today a record starts wherever a line begins with `id:`, which is fragile (it misread a perfectly valid two-line reference in my test). That is good to fix, and your suggestion is the standard answer: mark where each record opens and closes.
- Proposal: every capsule record sits between explicit begin and end markers, for example `BEGIN RECORD <id>` and `END RECORD`, or a fenced block per record. The scanner reads only inside markers. Old v5.0 saves stay importable, because the scanner can fall back to the current rule when it finds no markers.

### Already covered (checked, so no change proposed)

- The helper's `--brief` lines are copied verbatim (AI_RULES). Only the round header is composed by the GM.
- The glossary already holds names, terms and roll bands per language.
- Tier boosts for gear are already a table (§B).
- ENCODING is opt-in and hides capsule and GM-Δ records from a player reading the save, which still matters in software.
- PROFILE lite is an output-length choice for the player, not a workaround for context size.
- Checkpoints every 10 rounds also drive the review rules (dues, audit at R20, R40). The host already autosaves a journal each round, so the only open question is whether the review cycle should stay at 10 rounds.

### Size

The engine and AI rules together are about 85,000 characters (about 21,000 tokens). The part always sent is about 6,000 tokens (Part 0, AI rules §1-2 and the routing table); the rest is routed per turn. No change proposed unless a 7B+ test shows the turn overflowing 32K.

### Game design

- Undo and replay from a save is not built. The journal makes it possible; the engine should define what is rolled back.
- A few rarely used engine options are not covered by the host. I have not listed them yet; that needs a pass through the engine against the tool list.

### Order

1. Decide which of these changes you want in a new engine version.
2. Update the host to match, keeping v5.0 saves importable.
3. Re-run the replay test on your real 120-round campaign. It must still reproduce every save.
