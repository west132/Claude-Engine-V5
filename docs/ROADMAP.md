# Roadmap

Copyright (c) 2026 West132.WL. All rights reserved.

Ideas for later versions. None of this is built yet. Do it only after the base game has been tested with a 7B+ instruct model.

## Role agents: NPCs and the world as separate AI calls

Today one referee call does most of the judging. The idea is to split the thinking into smaller roles that each see only what they should, then merge their proposals in the main GM step.

### Who gets an agent

Not every NPC is worth a model call. Three tiers, decided by code, not by the AI:

| Tier | Who | Treatment |
|---|---|---|
| Principals | The NPCs marked as main in the BACKGROUND (see "Who is a main NPC" below) | Own agent when they act or speak, plus off-screen plans advanced when time passes |
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

**2. Death at 0 HP, with a switch for important NPCs.** No extra dice. Two settings, chosen in the world settings and asked again at the start of a game:
- **Protect important NPCs: open or closed.** "Important" means the main NPCs recorded in the BACKGROUND. Default for existing worlds: closed, so they behave as today.
  - **Open:** an important NPC at 0 HP is down, not dead, and keeps the one-hour window that the engine already has. Help or treatment within that hour stabilises them; the engine's existing rule decides what happens if none comes (§10.5). The mission still counts as open, so the story can go on.
  - **Closed:** an important NPC is treated like everyone else.
- **The player's choice overrides protection: yes or no. Default yes.** With yes, anyone the player character tries to attack or kill has no buffer, however important, even when protection is open. The mission fails if they die (the engine records that). With no, protection also holds against the player.
- **Everyone else at 0 HP is dying** and is killed unless someone helps at once.
- The player's own character is not covered by these settings.
- It also settles injuries on incidental actors: they are ordinary NPCs, so the dying rule applies and no record is needed.
- To confirm when this is built: that the engine's existing one-hour 2d10 roll (wake at 1 HP on 11+, else die) stays as the rule after the hour.

**2b. Who is a main NPC.** The engine has no such mark. §13.1 keeps a persistent record for any NPC who "recurs or matters", which includes minor ones, so "recorded" is not the same as "main". Both the death-protection setting and the role-agent tiers need an explicit field, for example `importance: main` on an NPC in the BACKGROUND, set by the author or by the generator at world creation. Without it, "important NPC" would wrongly cover every recorded NPC.

**3. Saves.**
- Keep the readable text save and capsule as the export and exchange format, because it is what chat saves and your 120-round campaign use.
- Under it, keep a structured save that the host owns. Today `journal.json` is written after every turn and replaced safely (written to a temporary file first). It holds the current state, the GM-Δ chain and the pending entries, plus only the last 40 chat messages. Missing: a schema version, a checksum, automatic backups, and a per-round history. Industry practice for game saves is a versioned structured format with migrations, plus backups, and that is what this adds.
- "As detailed as possible" is best met by the history, not by a bigger text save: every round's player message, tool calls with their dice results, GM-Δ, narration and a snapshot of the state. That is what makes undo, replay and audits possible, and the journal does not keep it today.
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
- Checkpoints every 10 rounds also drive the review rules (dues, audit at R20, R40). The host already writes its journal after each turn, so the only open question is whether the review cycle should stay at 10 rounds.

### Size

The engine and AI rules together are about 85,000 characters (about 21,000 tokens). The part always sent is about 6,000 tokens (Part 0, AI rules §1-2 and the routing table); the rest is routed per turn. No change proposed unless a 7B+ test shows the turn overflowing 32K.

### Game design

- Undo and replay from a save is not built. The journal makes it possible; the engine should define what is rolled back.
- A few rarely used engine options are not covered by the host. I have not listed them yet; that needs a pass through the engine against the tool list.

### Not an issue (West132.WL)

- Migrating saves older than v5.0 (§16.5). Only v5.0 saves matter.
- Module C, bounded scenario endings. Not used by the example worlds; it can stay as written.

### Planned fixes

**A. Revising generated Round-0 truth (§16.6).** The rule: a fact the AI generated for the BACKGROUND may be revised while it is still provisional, for a world reason, but never once established, and never to help or hurt the player.
- **Mark the origin.** When a world is created, the host records whether the BACKGROUND is authored (the person wrote it), generated, or mixed. An authored one changes only when the person changes it. In generated or mixed ones, everything the person did not request is provisional.
- **Track what is established.** The host keeps a status per field: provisional or established. A field becomes established when the player observes it or learns it, when a roll, an actor's decision, evidence, a payout or a committed fact uses it, or when the person confirms it. Code can detect this from the ledger entries and tool calls that name the field. When code cannot tell, it treats the field as established, which is the safe side.
- **A `revise_round0` tool for the referee.** Arguments: the field, the new value, the reason. The code refuses unless the field is provisional, the reason is one the engine allows (contradicts canon or anchors or another fact; implausible for its place, actor or band; forces later invention; the person asked), and no unresolved roll is bound to it. The reasons the engine forbids are not selectable: the player's plan, danger, pacing, or a player theory. The smallest change that fixes the problem is the one accepted.
- **Recording.** Before the first round, the BACKGROUND file is rewritten. After that, the file stays and the host writes one ledger entry: `+ continuity_status.round0_revisions.<field> :: was <was> → now <now> — <reason> (R<round>)`. The overlay applies it.
- **The person can ask.** An "Edit the world" screen lists provisional fields only, and asks the person to confirm. Established facts change only in the story, or through the correction in B.

**B. Repairing a GM error: undo and replay (§16.7).** The rule: a real GM error is repaired; a risky choice that lost, or an unfavourable roll, stands. The player never pays for a cost the engine caused.
- **Record each round in full.** The structured history keeps, per round: the player's message, each tool call with its arguments and dice results, the entries committed, the narration, and a snapshot of the state after the round closed. Nothing else is needed to rebuild a round.
- **Report.** A "Something is wrong" button lets the player name the round and describe the problem. `audit` findings can raise the same report automatically.
- **Decide.** The referee classifies it as a GM error or as a rule working as written, using the engine's own lists (§16.7). The player sees the verdict and can accept it or ask to reload. Code never lets the AI quietly dismiss a report.
- **Repair without replay.** If no later outcome changed, one correction entry is written in place and play continues.
- **Repair with replay.** If a later outcome changed: restore the snapshot of the round before the earliest changed one; replay the player's later messages from there. Rounds reuse their numbers (§8). A roll whose bound context the fix did not change keeps its recorded dice and result (invariant I10); a roll whose context did change is rolled fresh. Narration is regenerated.
- **Chain and saves.** The host owns the GM-Δ chain, so it cuts the chain at the restore point and re-emits the entries that still hold. This is equivalent to the engine's voiding rule (a block with a round at or before an earlier block voids it). Saves written after the restore point stop being the newest valid save. The host adds `continuity_status.player_corrected.<round> :: <error> → <fix>` and shows one line (restore point, fix).
- **Build order.** First the per-round history (needed for the structured save anyway), then in-place correction, then rollback and replay, then the button and the verdict screen.
- **Test.** Replay your 120-round campaign, inject a deliberate error at one round, repair it, and confirm the later saves match what the engine's rules say they should.

### Order

1. Decide which of these changes you want in a new engine version.
2. Update the host to match, keeping v5.0 saves importable.
3. Re-run the replay test on your real 120-round campaign. It must still reproduce every save.
