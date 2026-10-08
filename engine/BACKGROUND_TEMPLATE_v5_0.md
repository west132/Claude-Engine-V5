# BACKGROUND TEMPLATE — v5.0

For `NEW ENGINE v5.0`.

This file defines **Round-0 truth**: the setting, the character's starting state, and whatever the world already contains before play begins.

Once play begins this file is history. Played events change the Ledger, never this file. Detail the engine generated stays provisional until play relies on it, and may be corrected for a real reason (engine §16.6). Field names match the engine's owners (§6) and the save template, so Round-0 state imports without translation.

Fill in only what the game actually uses. Never create an empty category to satisfy the template, and never grant unstated capability, gear, or connections because they might be useful later.

---

## 0. Identity and provenance

```yaml
background_id:        # required; every save's background_ref points here
provenance:           # authored | generated | mixed
requested: []         # generated or mixed: what the person asked for, in their terms
```

`authored` means the person wrote all of it: every fact is theirs and only they change it. In a `generated` or `mixed` background, `requested` lists what the person actually asked for — those facts are fixed like authored ones. Everything else was filled in by the engine and is provisional until play establishes it (engine §16.6). Record requests as the person gave them; do not widen them.

---

## 1. Setting

```yaml
setting:
  world:
  era:
  starting_region:
  mode:                 # canon | historical | original | alternate
  canon_scope:          # canon: history before the start is fixed; after it, canon's
                        # main course is the actors' default plans (Canon course)
  allowed_deviations:   # what play may change; no canon outcome is protected
```

### Canon course — only when `mode: canon`

The bones of the main quest and major questlines, written as the plans of the actors who drive them: settled intent, not scenes, dates, or outcomes (engine §13.1, Canon mode). Each step needs its actors' knowledge, means, and time; play can delay, divert, or end any of them. Leave detail to canon: anything this file leaves out comes from the game or source itself.

```yaml
canon_course:
  actor_or_group_id:
    - <step of their default plan, in order>
  later_steps:          # optional: "as in the game — …"
```

## 2. Setting anchors

Record only the anchors needed to stop incompatible generation. Every new setting element in play must trace back to one of these, to established canon, or to in-world development (I3).

```yaml
setting_anchors:
  peoples_or_species: []
  powers_or_supernatural_rules: []
  technology: []
  institutions: []
  religions_or_beliefs: []
  economics_or_trade: []
  law_and_social_structure: []
  creatures_or_threats: []
  norms:
    law_and_outlaws: []     # whom the law protects; what people care about (engine §13.7)
    morale:                 # how readily each common kind of combatant breaks (engine §12)
      kind_of_combatant:
  mp_powers:                # only if the setting has MP-drawing powers (engine §10.5)
    draws_mp: []
    recovery:               # fast | slow | rest_only
    notes:
```

`norms` holds the setting's own standards where they differ from a generic modern sense of right, and how readily each common kind of foe breaks. Morale is settled from these, never rolled; without an entry, self-preservation decides (engine §12).

### Calibration notes — optional

Map the engine's scales to this setting where the mapping is not obvious.

```yaml
skill_tiers:          {T1: , T2: , T3: , T4: }
class_sources:        {ELITE: , LEGENDARY: }
equipment_tiers:      {T1: , T2: , T3: , T4: }       # when equipment_power_tiers is enabled
weapon_and_armour_classes: {}
```

## 3. Player

```yaml
player:
  identity:
    name:
    age:
    origin:
    history: []
  appearance:
  archetype:
  job:
  belongs: []
  gender:
  character:
  status:
  starting_activity:
```

### Capability

```yaml
  skills:
    skill_id:
      class: NORMAL | ELITE | LEGENDARY     # advancement ceiling
      tier: T1 | T2 | T3 | T4               # current mastery
      growth_evidence: 0
      ceiling_evidence: 0
      class_source:
      abilities: []
  traits: []
  expertise:
    established: []
    limitations: []
  growth_period: {opened: 0, credited: []}
  progression:                    # when numeric_level_xp is enabled
    system: numeric_level_xp
    state: {level: , xp: 0}
  vitality:                       # only when numeric_level_xp is disabled:
                                  # ordinary | seasoned | veteran | exceptional | heroic | legendary
  starting_item_points: {points: 0, basis: }   # when flexible_item_entitlement is enabled
```

`class` is the ceiling, `tier` is where they are now. Trained but unremarkable competence starts at T1; a higher start needs mastery evidence in the history. `growth_evidence` starts at 0 unless prior qualifying learning is actually established. Level comes from established experience, and the history must support it.

`starting_item_points` is required when `flexible_item_entitlement` is on, including an explicit `0`. Derive it from material circumstances, never from level: `0 none · 1 limited · 2 ordinary professional · 4 well-resourced · 8 elite or wealthy · 12 exceptional · 16+ extraordinary` (engine §D.2). Reasonable background possessions are separate and never consume it.

### Condition and possessions

```yaml
  condition:
    hp:                           # current; the maximum is derived (engine §10.5)
    mp:                           # current; omit if no MP-drawing skill
    injuries: []                  # {injury: , home: , effect: }
    fatigue:
    last_rest:
  equipment:
    - item_id:
      name:
      type:
      capability_domain:
      condition: serviceable | worn | damaged | critical
      special_properties: []
      tier:                       # when equipment_power_tiers is enabled
      abilities: []
  money:
  resources:
    resource_id: {name: , tracking: exact | usage_die, count: , usage_die: }
  routines: {}
  fighting_style: []
  knowledge:
    facts: {}
    channels: []
```

`hp` and `mp` start at the derived maximum unless the history says otherwise. `fighting_style` holds combat habits the player has stated for this character, in their words — what a resource is kept for, how a fight opens, how a danger is tested, where allies stand. Leave it empty if they have stated none; only the player adds or changes it (engine §7). `routines` holds only established in-world recurring behaviour. `channels` are how this character actually receives information (engine §13.1).

## 4. What this campaign depicts

```yaml
content_bounds:
  depicts: []
  excludes: []
  notes:
```

## 5. Optional modules

```yaml
enabled_modules:
  numeric_level_xp: false
  equipment_power_tiers: false
  bounded_scenario_endings: false
  flexible_item_entitlement: false
```

Enable a module only when the campaign uses it. A save preserves activation and never enables a module later.

## 6. Locations

```yaml
locations:
  location_id:
    name:
    conditions: {}
    challenge_band: {min: , max: , basis: }
```

A band constrains what causes can plausibly exist in a place; its `basis` says why. Record only places the opening actually needs; a place first entered in play gets its band then (engine §13.4).

## 7. Rights and obligations

```yaml
rights_obligations:
  right_id: {type: , parties: [], state: {}}
active_commitments: []             # references to right_ids only
```

Ownership held by someone else, custody, contracts, duties, authority and its limits.

## 8. Actors and factions

```yaml
npcs:
  npc_id:
    name:                          # name, job, belongs, gender, character are required;
    job:                           # use unknown where it is not established
    belongs:
    gender:
    character:
    state: {}                      # status, position, current HP/MP when below max, plan, due (a time or registered trigger), what they do if blocked
    drives: {}                     # wants, fears, loyalties, values
    relationships:
      toward_id: {tie: , attitude: , credit: [], grievance: [], believes_identity: }
                                   # romantic_interest: only once established (engine §13.1)
    knowledge: {facts: {}, channels: []}
    capability: {}
    discovered_information: {}

factions:
  faction_id:
    name:
    role:
    state: {}
    drives: {}
    relationships: {}
    knowledge: {facts: {}, channels: []}
    capability: {}
    discovered_information: {}
```

Populate only material fields. `attitude` is a few plain words; a first meeting starts neutral unless state says otherwise, never friendly by default. `credit` is what the other party did for this actor; `grievance` is what this actor holds against them. `believes_identity` holds a false or partial belief about who someone is. A canon actor's canon plan goes in `canon_course`, not here.

## 9. Quests, threads, trackers, pressures

```yaml
quests: {}
development_threads: {}
trackers: {}

active_world_pressures:
  pressure_id:
    name:
    origin:
    state: {}
    actors: []
    trajectory:                    # expected direction if conditions continue, not a locked future
    clock: {name: , segments: , filled: 0, pace: every <interval> while <condition>, due: <first check time>, on_fill: }
    discovered_information: {}
```

Set `segments` and `pace` together so the whole span fits the process: a world-scale pressure moves in weeks or months, never one segment a night (engine §13.5). `on_fill` is what the world does if nobody interferes, never an event aimed at the player. Zero pressures is valid.

## 10. Hidden truth at Round 0 — optional

A campaign that begins with something already true and unknown records it here. It is hidden state from the first round: it belongs in the capsule, never in the readable save.

```yaml
locked_case_truths:
  case_id:
    cause:
    prior_events: []
    state: {}
    evidence: {}
    trajectory:
    discovered_information: {}

open_suspicions:
  suspicion_id:
    description:
    held_by:
    concerns_act:
    attached_to:        # null while it belongs to no particular person
```

Commit the cause here and the evidence follows from it. Never write evidence whose cause is left to be decided later. Each case tied to a quest lists its routes and must pass engine §13.6 SOLVABLE.

## 11. World state

```yaml
world_state:
  location:
  time:
    season:
    day_index: 0
    date:
    clock_minutes:
    daypart:
    precision: exact | daypart | degraded
  environment: {}
  material_history: []
  unowned_facts:
    visible: []
    hidden: []
  glossary: {}                   # optional, per language: {zh_hans: {<id>: <English> = <form>}} (AI_RULES Language)
```

## 12. Presentation

```yaml
narrative_theme:
  initial: {tone: , style: }
  current: {tone: , style: }
```

A style seed only: it never adds facts, and the initial theme never regenerates on reload (engine §16.2).

## 13. Ending conditions — only when `bounded_scenario_endings` is enabled

```yaml
ending_conditions:
  core_conditions: []
  hidden_conditions: []
  closed: []
```

Open-world play needs none (engine §C).

---

*End of Background Template v5.0*
