# BACKGROUND — the_salt_road (example, original setting)

```yaml
background_id: the_salt_road_v1
provenance: authored
requested: []

setting:
  world: The Salt Road, a low-magic trade frontier of walled market towns and salt flats
  era: late-medieval analogue; caravans, guild charters, no gunpowder
  starting_region: Marrowgate, a caravan town on the western end of the salt flats
  mode: original
  allowed_deviations: anything play can change; no outcome is protected

setting_anchors:
  peoples_or_species: [humans only; flatlanders, townsfolk, hill clans]
  powers_or_supernatural_rules: [rare hedge-charms that need a rested body (draw MP); no open magic]
  technology: [iron tools, crossbows, carts, lamps, ink and paper]
  institutions: [Caravan Wardens Guild, Marrowgate Watch, salt-tax collectors]
  religions_or_beliefs: [Lady of Small Mercies shrines, road superstitions]
  economics_or_trade: [salt, wool, iron, silver pennies; guild fees]
  law_and_social_structure: [guild charters set road law; the Watch keeps the town]
  creatures_or_threats: [bandits, flat-wolves, brine fever, sandstorms]
  norms:
    law_and_outlaws: [theft on the road is a guild matter; killing inside walls is Watch business]
    morale:
      bandit: breaks when the leader falls or a third are down
      watchman: holds for the town, withdraws when badly outnumbered
      flat-wolf: withdraws when hurt, fights to the death only when guarding pups
  mp_powers:
    draws_mp: [hedge_charm]
    recovery: rest_only
    notes: charms are small tricks; no power above the caster's tier

enabled_modules:
  numeric_level_xp: true
  equipment_power_tiers: false
  bounded_scenario_endings: false
  flexible_item_entitlement: false

player:
  identity:
    name: Ilsa Venn
    age: 27
    origin: Marrowgate, daughter of a salt-weigher
    history: [two seasons as a Wardens Guild outrider, left the guild after a dispute over unpaid wages]
  archetype: caravan guard
  job: freelance guard
  belongs: []
  gender: female
  character: dry-humoured, careful with money, hates being owed
  status: unemployed, lodging at the Cracked Pot inn
  starting_activity: eating breakfast in the Cracked Pot common room, looking at the job board
  skills:
    crossbow: {class: ELITE, tier: T1, growth_evidence: 0, ceiling_evidence: 0, abilities: []}
    shortsword: {class: ELITE, tier: T1, growth_evidence: 0, ceiling_evidence: 0, abilities: []}
    road_lore: {class: NORMAL, tier: T1, growth_evidence: 0, ceiling_evidence: 0, abilities: []}
    hedge_charm: {class: NORMAL, tier: T1, growth_evidence: 0, ceiling_evidence: 0, abilities: []}
  traits: [steady nerves]
  expertise:
    established: [caravan routes west of the flats]
    limitations: [cannot read the old salt-grant script]
  progression:
    system: numeric_level_xp
    state: {level: 3, xp: 0}
  equipment:
    - {item_id: shortsword, name: shortsword, type: weapon, capability_domain: melee, condition: serviceable, special_properties: [], abilities: []}
    - {item_id: crossbow, name: light crossbow, type: weapon, capability_domain: ranged, condition: serviceable, special_properties: [], abilities: []}
    - {item_id: leathers, name: boiled-leather jerkin, type: armour, capability_domain: defence, condition: worn, special_properties: [light armour], abilities: []}
  money: {silver: 14, copper: 20}
  resources:
    bolts: {name: crossbow bolts, tracking: exact, count: 18}
    rations: {name: trail rations, tracking: usage_die, usage_die: d6}
  routines: {}
  fighting_style: []
  knowledge:
    facts: {job_board: the board in the Cracked Pot lists caravan escort work}
    channels: [inn gossip, the job board]

locations:
  marrowgate_cracked_pot:
    name: The Cracked Pot (inn, Marrowgate)
    conditions: {crowded: morning, hearth: lit}
    challenge_band: {min: 1, max: 4, basis: busy caravan town; ordinary work, occasional brawl}

npcs:
  oda_brandt:
    name: Oda Brandt
    job: innkeeper
    belongs: [Marrowgate townsfolk]
    gender: female
    character: shrewd, fair, tired
    state: {status: present, position: marrowgate_cracked_pot, plan: run the inn through the morning rush, due: none (incidental)}
    drives: {wants: a quiet inn and paid-up guests}
    relationships:
      player: {tie: landlady, attitude: neutral, credit: [], grievance: []}
    knowledge: {facts: {}, channels: [inn gossip]}
    capability: {}
    discovered_information: {}
  corvin_hale:
    name: Corvin Hale
    job: caravan master
    belongs: [Caravan Wardens Guild]
    gender: male
    character: brusque, honest about prices
    state: {status: at the Salt Gate yard, position: marrowgate_salt_gate, plan: hire guards for a wool run to Pellam, due: 2026-03-02 08:00}
    drives: {wants: a loaded caravan out before the brine winds, fears: another ambush}
    relationships: {}
    knowledge: {facts: {}, channels: [guild runners]}
    capability: {}
    discovered_information: {}

active_world_pressures:
  brine_winds:
    name: The brine winds are coming
    origin: seasonal shift on the salt flats
    state: {stage: early gusts}
    actors: []
    trajectory: flat crossings become dangerous within weeks
    clock: {name: Brine winds close the flats, segments: 6, filled: 1, pace: every 5 days while the season holds, due: 2026-03-06 06:00, on_fill: flat crossings are closed until the winds pass}
    discovered_information: {}

world_state:
  location: marrowgate_cracked_pot
  time: {season: early spring, day_index: 0, date: 2026-03-01, clock_minutes: 450, daypart: morning, precision: exact}
  environment: {weather: cold and clear, light: dawn through shutters}
  material_history: []
  unowned_facts: {visible: [], hidden: []}
  glossary: {}

narrative_theme:
  initial: {tone: "grounded, wry, a little weary", style: "plain concrete prose with short exchanges"}
  current: {tone: "grounded, wry, a little weary", style: "plain concrete prose with short exchanges"}
```
