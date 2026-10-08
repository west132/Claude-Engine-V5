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
