# SAVE — Ashfall: Hunter — R90

For `NEW ENGINE v4.4` · background `BACKGROUND_ASHFALL_HUNTER_v4_4.md`

# PART A — READABLE

## 1. Current state

```yaml
background_ref: {id: ashfall_hunter_gemini_combined_v4_4}
language: en
round:
  last_completed_round: 90
  saved_completed_round: 90
world_state:
  location: city_risk_office
  time:
    season: autumn
    day_index: 16
    date: '2026-10-22'
    clock_minutes: 615
    daypart: morning
    precision: exact
  environment:
    weather: dry, cold
    office: Room 3-14; Mara frightened by the runner footage
    rin: ordinary clothes; Southport camera card in pocket; Varga at 15:00
```

## 2. Player

```yaml
player:
  identity:
    name: Rin Hale
    age: 22
    origin: Ashfall City
    history:
    - Raised in Ashfall by a human guardian who refused to explain much about Rin's absent biological parent.
    - At sixteen, survived an encounter with a nonhuman attacker and learned that the family warning about demonic
      blood was literal.
    - Spent the following years doing night courier and recovery work in rough districts, earned a private investigator
      licence at nineteen, and opened Hale Workshop three years ago; Rin is good at the work and known for finding
      people; odd jobs with real demons in them reach Rin through Pike's bar.
    - Has survived several minor demonic encounters and learned controlled use of one short demonic surge, but does
      not know the full origin, ceiling, or future expression of the bloodline.
  appearance: Human-passing young adult; practical dark street clothes and riding gear. During heavy demonic exertion,
    the eyes can briefly show an ember-like change.
  archetype: demon-blooded urban hunter-investigator
  job: licensed private investigator and recovery agent; night courier shifts when cases are thin
  belongs: []
  gender: male
  character: quick-mouthed, dry humour, calm in a fight and careless with money; protective of bystanders; does
    not assume an occult explanation without evidence
  status: healthy; independent; poor but owes nobody; a good PI with a local name for finding people and things;
    a few regulars know Rin takes stranger jobs
  starting_activity: Closing the rented workshop for the night while hearing a prospective client, Nadia Voss, explain
    that her transit-worker brother disappeared during a night maintenance call.
  skills:
    close_combat:
      class: ELITE
      tier: T2
      growth_evidence: 0
      ceiling_evidence: 0
      class_source: years of practical training and repeated dangerous field work
      abilities: []
    mobility:
      class: ELITE
      tier: T2
      growth_evidence: 0
      ceiling_evidence: 0
      class_source: years of urban courier work, climbing, pursuit, and evasive movement
      abilities: []
    investigation:
      class: ELITE
      tier: T2
      growth_evidence: 0
      ceiling_evidence: 0
      class_source: 'three years of licensed PI work: traces, records, interviews, surveillance'
      abilities: []
    streetwise:
      class: NORMAL
      tier: T2
      growth_evidence: 0
      ceiling_evidence: 0
      class_source: night work and repeated contact with Ashfall's service alleys, clubs, contractors, and informal
        networks
      abilities: []
    occult_lore:
      class: ELITE
      tier: T1
      growth_evidence: 0
      ceiling_evidence: 0
      class_source: direct exposure to genuine demonic incidents plus fragmented private research
      abilities: []
    demonic_channeling:
      class: LEGENDARY
      tier: T2
      growth_evidence: 0
      ceiling_evidence: 0
      class_source: rare demon-blood lineage combined with several years of controlled practice under real danger
      abilities:
      - demonic_surge — T2 MP-drawing power. Costs 6 MP. For one exchange, established demon-blood physiology can
        make clearly superhuman force, speed, or movement physically feasible; the relevant skill still resolves
        the action normally. It grants no automatic success, extra attack, or automatic extra damage.
    security_bypass:
      class: NORMAL
      tier: T1
      growth_evidence: 0
      ceiling_evidence: 0
      class_source: years of recovery work getting into places to get property back
      abilities: []
    disguise:
      class: NORMAL
      tier: T1
      growth_evidence: 0
      ceiling_evidence: 0
      class_source: surveillance and recovery work blending in as worker, rider, or tenant
      abilities: []
  traits:
  - Demon-blooded and human-passing. The lineage permits supernatural progression but grants no unstated ability,
    resistance, regeneration, knowledge, authority, or immunity.
  - Rin can recognize strong demonic resonance as supernatural when directly exposed to something comparable to
    prior experience, but cannot identify an unfamiliar demon, ritual, weakness, or lineage on sight.
  - Normal sleep, food, injury, fatigue, law, money, equipment limits, and social consequences still apply unless
    an established power changes one of them.
  expertise:
    established:
    - 'standard PI work: skip traces, records and licence checks, canvassing, interviews, surveillance, serving
      papers'
    - moving through Ashfall at night and finding practical access routes
    - recovering people or property through interviews, observation, and legwork
    - distinguishing a handful of genuine demonic traces from ordinary urban damage when enough evidence is present
    limitations:
    - no police authority
    - no formal ritual-magic training
    - no comprehensive demon taxonomy
    - no knowledge of the full bloodline origin or ceiling
    - no automatic ability to detect hidden demons through walls, crowds, or distance
  growth_period:
    opened: 16
    credited: []
  progression:
    system: numeric_level_xp
    state:
      level: 4
      xp: 195
  condition:
    hp: 16
    mp: 16
    injuries: []
    fatigue: rested
    last_rest: nights of Oct 17–21 at the workshop
  equipment:
  - item_id: nightglass_blade
    name: Nightglass Blade
    type: one-handed occult-treated blade
    capability_domain: close_combat
    condition: serviceable
    special_properties:
    - Demon-reactive alloy; legal status depends on where and how it is carried.
    tier: T2
    abilities:
    - Demon-reactive edge — remains physically effective against manifested demon bodies that would resist an ordinary
      untreated edge; it does not bypass armour, wards, distance, unique resistances, or the need to hit.
  - item_id: riding_jacket
    name: Reinforced Riding Jacket
    type: protective clothing
    capability_domain: physical_protection
    condition: serviceable
    special_properties:
    - Counts as light armour where its coverage is relevant.
    tier: T1
    abilities: []
  - item_id: motorcycle
    name: Used Street Motorcycle
    type: transport
    capability_domain: urban_mobility
    condition: worn
    special_properties: []
    tier: T1
    abilities: []
  - item_id: smartphone
    name: Smartphone
    type: communications and records access
    capability_domain: information_access
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: first_aid_kit
    name: Compact First-Aid Kit
    type: medical supplies
    capability_domain: first_aid
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: work_disguise
    name: 'Work disguise: grey utility jacket, hi-vis vest, beanie, work boots, clipboard'
    type: clothing
    capability_domain: disguise
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: eli_flat_key
    name: Spare key to Eli Voss's Lowfield flat (Nadia's)
    type: key
    capability_domain: access
    condition: serviceable
    special_properties:
    - Nadia's spare, lent to Rin
    tier: T1
    abilities: []
  - item_id: eli_badge
    name: Eli Voss's Transit badge
    type: ID badge
    capability_domain: identification
    condition: serviceable
    special_properties:
    - Eli's property
    tier: T1
    abilities: []
  - item_id: red_line_map
    name: Red Line service map, RED SPUR (CLOSED) circled
    type: document
    capability_domain: information_access
    condition: serviceable
    special_properties:
    - Eli's, from his desk
    tier: T1
    abilities: []
  - item_id: clip_camera
    name: Clip-on camera with night mode (cyclist body cam)
    type: camera
    capability_domain: surveillance
    condition: serviceable
    special_properties:
    - long battery
    tier: T1
    abilities: []
  - item_id: paperwork
    name: 'Paperwork: city contract copy, chain-of-custody receipt, Haller''s knife receipt, RM-12 slip'
    type: documents
    capability_domain: records
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: haller_knives
    name: Two Haller-treated 4-inch fixed knives (one small-of-back sheath, one left boot)
    type: light blade
    capability_domain: close_combat
    condition: serviceable
    special_properties:
    - oil weekly; keep dry
    tier: T2
    abilities:
    - Haller-treated edge — bites on lesser demons (cinderlings and similar small things); otherwise a good knife;
      no effect on wards or larger demons beyond a normal blade
  - item_id: parent_letter
    name: Parent's letter in a plastic sleeve (signed with a sigil like a closed eye crossed by a line)
    type: document
    capability_domain: records
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: rusk_footage
    name: Camera footage of Rusk at the Halden gate (saved in three places)
    type: video evidence
    capability_domain: records
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: padlock_keys
    name: 'Keys: hut 3 chain padlock, Wren Bridge cash box, Lina Dalen''s spare flat key, wharf room key on a fisherman''s
      float'
    type: keys
    capability_domain: access
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: clean_phone
    name: 'Clean prepaid phone (off; numbers: Ada, Mara, Eli)'
    type: phone
    capability_domain: communications
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  money:
    cash_and_accessible_funds: 1299
    currency: USD
    note: 'Plus $400 hidden in the wharf go-bag. Owed to Rin: $2,000 from the city by Fri 23 Oct (Unit 9 $1,500
      + Tanner Lane bonus $500). Halden job ($1,500) still open.'
  resources:
    first_aid_supplies:
      name: first-aid supplies
      tracking: usage_die
      usage_die: d6
  routines:
    pi_legwork:
      action: standard PI legwork on an active case (records searches, phone work, canvassing, interviews, setting
        up surveillance) carried out competently without step-by-step orders
      recurrence: whenever Rin is working a case
      condition: continues until a real decision, danger, or something the routine does not cover
      status: active
    outfall_check:
      action: swap the Southport footbridge camera battery and card; pull footage
      recurrence: every second day, a different disguise each time
      condition: while the camera is in place
      status: active; last 2026-10-22 (litter-picker); next 2026-10-24
  fighting_style: []
  knowledge:
    facts:
      demons_real: Demons are real and some use the underground city as cover or territory.
      own_blood: Rin is partly demonic and can channel a limited demonic surge.
      surface_secrecy: Most ordinary people do not know the supernatural explanation behind Ashfall's strangest
        incidents.
      nightglass: Ada gave Rin the Nightglass Blade at sixteen, saying only it came from 'someone who'd want you
        to have it'. Maker unknown.
      dangerous_underground: Some abandoned or restricted underground routes have a genuine supernatural reputation,
        but Rin has no complete map of them.
      ada_2004: 'Ada told Rin on Oct 10: he was born spring 2004. In autumn 2004 something old under the Red Line
        nearly got out, and his parent, one of the beings below who broke from a ''court'', sealed it. Ada was there.
        The parent gave infant Rin to her to raise away from the Red Line and vanished; fate unknown. The Nightglass
        Blade was the parent''s, left for him. Letters from the parent are in a deposit box at Harland''s Bank,
        Wexley. Ada takes him Monday 12 Oct at 09:30. She begged him not to go near the tunnel before reading them.'
      shard: 'Eli''s shard: thumb-sized dark glass with a red core, always warm, heats any container. Now in a closed
        steel biscuit tin on the workshop shelf. Rin could not reliably sense any resonance from it.'
      charms: Mara holds four stones (two laundromat, Lucy's, Imran's) with chain-of-custody receipts. Eli's shard
        is in a steel box at the Wren Bridge tollkeeper's hut. Hut 3 is empty but chained.
      warren: 'Lucy Warren (about 23), Suds & Spin part-timer, held the Choir box for $200 and wore a charm ~11
        days. She gave it to Rin on Oct 8. M cut her loose Oct 11 07:02 (''keep the $200… good luck''). Bellamy
        clinic exam Oct 11 (Rin paid $200): low core temperature, low BP, fast pulse, dehydration, weight loss,
        a healing burn-like mark below the throat where the stone hung; bloods back Wed 14 Oct with a signed report.
        She''s slowly improving; chills and ''furnace'' dreams; felt lucky while wearing it, unlucky now.'
      ada_call: 'Oct 7: told Ada about the glass. She went flat and frightened, told Rin to put it far away and
        forget it, hung up, and said she is coming up Saturday for lunch.'
      pike_kestrel: Pike says Jo Kestrel is the one for detectors and theory about strange materials.
      kiosk: 'The Ferris Yard kiosk owner: the back half of the yard goes dark 2–3 nights a week lately, Merrow
        vans come down Halden 01:00–02:00, Transit staff get locked out for "Merrow works". Bernie the night guard
        walks the fence about hourly and buys coffee around midnight.'
      eli_found: Found Eli Voss alive in relay hut 3 on the Canal Street embankment, Oct 6. Clinic stitched his
        arm and strapped the ankle on Oct 7; he is staying at Nadia's flat.
      eli_account: 'Eli says: Red Line blackout windows ran 1–2 hours past sign-out with no Transit order; on Oct
        4 he followed a Merrow van into Halden Lane behind Ferris Yard and saw Jonas Rusk (Merrow night supervisor)
        and men carrying crates out of service door 7-B into the sealed Red Spur; he took a shard from an open crate,
        was chased, fell on the service stairs. His phone holds photos, including a blurry shape on the far platform.'
      cinderling: A dog-sized slag-and-ember creature had been scratching at hut 3, drawn to the area; Rin killed
        it. Burned rats and three-toed tracks were its signs.
      haller: 'Dutch Haller: knife-grinder at the Fishmarket Arcade by the wharf; treats steel for hunters at night
        (salt, iron, a secret); doesn''t forge; cash, vouched clients only. Jo will mention Rin. Met Oct 8: he recognised
        the description, saw some once years ago, won''t touch it. Talks only at the arcade''s back loading door
        after 21:00 with Kestrel''s word or $100; never bring the glass near his stall. Examined the Nightglass:
        not forged, no layers, one material through, glass-dark, ~20 years old by the grip wear; won''t treat it.
        Honed a nick ($20). Two treated 4-inch knives ordered: $600, $300 paid, ready Sun 11 Oct after 21:00 at
        his back door; bring the paper receipt. On raw glass (Oct 19): straight out of a wall; ''what you take from
        below, below comes looking for''; keep it cold, closed, away from people, never sold back.'
      pike_warned: Warned Pike on Oct 8 that his name is in the charm people's messages; he'll watch his door.
      exposure_plan: Eli advises reporting to the City Risk Management Office (not Transit, which works with Merrow
        daily; press only as backup). Nadia is against the press.
      mara: 'Mara Quill (City Risk Management) hired Rin on a signed contract: $750 for the report and the charms
        (bank transfer by Wed 14 Oct); $1,500 for a documented Halden window from outside (no entry through 7-B).
        Merrow told her the Ferris outage was aging equipment; she''s requested Transit''s original sign-out sheets.
        She''ll protect Eli: reference number, a whistleblower letter to her Transit Safety liaison after a signed
        statement, $150 fee. Statement Sat 10 Oct 10:00, room 3-14, Rin present. Sunday reply: keep the camera running,
        write down your exact words to Orin, send the medical report Wednesday, don''t let the holder near the stone,
        and do not take a job from Orin.'
      photos: 'Rin''s phone: hut 3 slag and claw marks (Oct 6), Suds & Spin basement damage and slag (Oct 7), 3
        screenshots of Warren''s M (Choir) thread, the OX-9 carton; plus Jo''s 4 photos of the courier.'
      courier: 'Choir courier: big man, forties, broad face, flattened nose, scar through one eyebrow, long hooded
        parka; dark grey Nissan hatchback, dented rear bumper, plate KT 72 VRN. Came at 22:00 Oct 8, said the people
        he carries for want their property back and will make it worth Rin''s trouble. Rin said they know where
        to find him. He drove off toward the ring road.'
      jo: Jo dropped her client's retrieval job (kept $750 as a kill fee) after Rin admitted the receipt was a bluff
        and sent the thread screenshots. Rin hired her for $200 cash to photograph the pickup; she did. $200 owed
        to her. She also said Gallo's pawnshop in Lowfield sells stones like these under the counter.
      q3_summary: 'City Q3 interruptions summary: three ''cause undetermined'', incl. Ferris Yard Sept 15 overnight.'
      ember_glass: 'Haller calls it ''ember glass''. A chip on his bench softened nearby steel edges, drew rats
        and something bigger; he threw it off the pier. Old trade talk: it sweats out of the walls at old bricked-up
        breaches where heat comes up from below.'
      gallo: 'Gallo checks parked cars, upper windows and the bus-stop corner before every smoke: afraid of being
        watched, not waiting for a delivery. On Oct 13 he carried a small bag to 14 Tanner Lane and came back without
        it. Jo''s detector clicked behind his counter Oct 9.'
      orin: 'A man calling himself Orin, ''a dealer in old things'', phoned Fri 9 Oct 18:00: $2,000 for the ''two
        small pieces'' and steady work ''with very little paperwork''. Rin refused and said twenty years isn''t
        old. Orin laughed, said keep them, the job offer never expires, ''careful people live a long time in this
        city''.'
      jo_camera: Jo will recover the Halden camera only after dark, after Bernie's 21:00 walk, if Rin pays the $200
        owed plus $100 for the climb, cash, before she climbs.
      parent_letter: 'Parent''s letter (read Oct 12): they were of the court below and left it. After Rin''s birth
        they sealed the old way under the Red Line with their own mark. It holds while nobody takes from it, weakens
        if dug at. The mark knows their blood and Rin''s: if Rin calls up his power near the old stones or near
        the black glass from them, those below feel the blood is alive and close (not his name or face). Walking
        right up to the seal wakes it regardless. The blade is made from what the parent was and won''t break against
        them. They don''t know if Rin could mend the mark.'
      rusk_footage: 'Rin''s camera: Rusk in a white Merrow pickup checked the Halden service-door padlock 16:20
        Sun 11 Oct (face, plate). Mara: useful, not the job; she needs vans and crates.'
      sheets_verdict: 'Mara (Oct 14): Transit''s original sheets show Eli''s seven windows booked 1 hour and signed
        out inside it; Merrow''s copies show 2–3 hours with a fake Transit code. She''s asking Transit Safety to
        suspend Merrow''s after-hours Halden access and writing to Merrow compliance.'
      trading_standards: 'Trading Standards searched Gallo''s shop Fri 16 Oct 10:00: nothing found, ledger copies
        taken, notice served. Mara is preparing a magistrate''s warrant application for 14 Tanner Lane (Monday at
        the earliest).'
      plate_trace: KT 72 VRN is registered to Brannock Freight Services Ltd, Unit 9, Exchange Yard, Old Exchange
        (OX-9). Director Aidan Brannock. M's number is an unregistered prepaid SIM.
      imran: Imran Dalen moved from high-dependency to a general ward Oct 19; knew the date, asked for tea and his
        cab; still talks the unknown language in his sleep. Lina recorded 4 minutes of it (3-4 clipped words repeated
        like directions); Mara said not to play it to anyone else. Lina gave her signed sale statement Oct 19.
      pike_cover: 'Someone in a nice coat asked Pike (Oct 12) how long Rin''s been around and his parents'' names.
        Pike will give the cover story: in Ashfall ~5 years, parents country farm people.'
      bolt_hole: 'Bolt-hole ready: Mrs Agnieszka Wolak''s back room above the old chandlery on the wharf, held to
        16 Nov ($150 paid); go-bag in the wardrobe with $400 sewn in; clean phone.'
      tanner_collection: 'Fri 16 Oct 23:20, 14 Tanner Lane: the courier and a shaven-headed bully in a leather jacket
        took Gallo''s zipped bag and a ledger-sized notebook and papers; the bully jabbed and threatened Gallo.
        Rin filmed it all from 90 m, tailed the grey Nissan unseen to Exchange Yard, Old Exchange, and filmed Unit
        9: shelving, OX-9 cartons, an older thin man in a cardigan taking the bag and notebook.'
      eli_closed: Eli paid $375 ('Rin, for everything'); case closed. Back on light duties Monday with Transit Safety's
        protection. Offered his Red Line schedule and tunnel knowledge any time. Tomas says Halden is locked after
        hours, Merrow's night crew is off it, there's audit talk, and Rusk is off 'sick'.
      halden_suspended: Transit Safety suspended Merrow's after-hours access to Halden on Oct 14; Merrow compliance
        has the falsified sheets; Rusk dodged the compliance meeting.
      unit9_seizure: Trading Standards seized 72 charms on cords and a warm wooden crate of fist-sized raw black
        glass with Merrow Utility tape from Unit 9 on Mon 19 Oct. The keeper said nothing; Brannock summoned. Mara
        keeps it all in steel, two locks, a cold windowless room. Police want the shaven-headed man.
      xp_and_pay: Mara is paying $1,500 for the Unit 9 surveillance and $500 for the Tanner Lane footage (Fri 23
        Oct); the Halden job stays open. She proposed a regular retainer; Rin said 'why not'.
      mercer_route: 'Eli: the old Red Spur drained south to the Mercer flood pump (still working, Transit''s). Service
        stairs from the pump room go down into old drainage galleries once linked to the spur''s outer galleries;
        overflow runs by culvert to the Southport outfall on the canal. Eli watches Mercer''s sump on the yard telemetry
        board and texts Rin the level; he promised not to go near it.'
      runner: 'Rin''s Southport camera, Wed 21 Oct 04:06–04:13 at low water (Mercer sump 9%): the Choir courier
        waited at the outfall; a cat-sized slag creature with glowing cracks came out between the grate bars, gave
        him a tiny red glinting chip, took a folded paper message wrapped round something, and went back in. Mara
        has seen it; she''s requesting the sealed part of her 2004 file and asking Transit Safety for vermin mesh
        on the outfall grate and the Mercer sump screen.'
      varga: 'Teodor Varga, ironworker in his seventies, Ironside Lane, Lower Docks (green door): did city contract
        work in 2004 making iron fittings for a job under the Red Line. Agreed by handwritten letter to see Rin
        Thu 22 Oct 15:00: ''Tell the young man I kept my notebook.'''
      brannock: 'Brannock Freight: grey Nissan KT 72 VRN and white Transit van AF 19 KXT; only premises Unit 9;
        director Aidan Brannock lives in Saltgate.'
      lucy: Lucy Warren is eating again, no dreams, cold hands; Rosa gave her shifts back.
    channels:
    - direct observation
    - phone and internet
    - public records
    - client interviews
    - ordinary city contacts established through play
    - Nadia and Eli Voss
  starting_item_points:
    points: 1
    basis: 'limited: poor freelance PI, but a workshop full of salvage, old case kit, and favours owed in small
      ways'
```

## 3. Modules and theme

```yaml
enabled_modules:
  numeric_level_xp: true
  equipment_power_tiers: true
  bounded_scenario_endings: false
  flexible_item_entitlement: true
narrative_theme:
  initial:
    tone: stylish demon-hunter PI action and banter; traceable clues lead toward active dangers and hard decisions,
      not a chain of office errands; calm scenes and nonviolent solutions remain possible
    style: rain, neon, flooded pump galleries, occult freight and ordinary shop work; sharp personal dialogue, consequential
      physical investigation, clear cinematic non-graphic demon fights when actors meet and conflict actually arises.
      No scene or fight is guaranteed and no named NPC has plot armour.
  current:
    tone: stylish demon-hunter PI action and banter; traceable clues lead toward active dangers and hard decisions,
      not a chain of office errands; calm scenes and nonviolent solutions remain possible
    style: rain, neon, flooded pump galleries, occult freight and ordinary shop work; sharp personal dialogue, consequential
      physical investigation, clear cinematic non-graphic demon fights when actors meet and conflict actually arises.
      No scene or fight is guaranteed and no named NPC has plot armour.
```

## 4. Index

```yaml
index:
  npcs:
    nadia_voss: Nadia Voss — Eli's sister, client, paid in full
    eli_voss: Eli Voss — Transit tech, found; at the workshop, sprained ankle
    tomas_reyes: Tomas Reyes — Eli's friend from work (name only)
    jonas_rusk: Jonas Rusk — Merrow night supervisor; Eli saw him at 7-B
    pike_adeyemi: Pike Adeyemi — owner of The Last Stop, job broker
    jo_kestrel: Jo Kestrel — rival hunter
    ada_hale: Ada Hale — Rin's guardian, Wexley
    mrs_okafor: Grace Okafor — landlady upstairs
    suds_and_spin_owner: Rosa Fenn — Suds & Spin owner, paid
    l_warren: Lucy Warren — Suds & Spin part-timer; ex-holder; recovering, results Wed
    laundromat_cinderling: cinderling in the Suds & Spin basement — killed
    kiosk_owner: kiosk owner at Ferris Yard corner — chatty, crosswords
    embankment_cinderling: cinderling at the Canal embankment — killed
    choir_contact_m: M (Choir) — texts Warren; arranges holds and pickups
    choir_courier: Choir courier — big, eyebrow scar; grey Nissan KT 72 VRN
    dutch_haller: Dutch Haller — blade treater, Fishmarket Arcade; back door after 9pm
    mara_quill: Mara Quill — City Risk Management analyst; Rin's client
    gallo_pawnbroker: Sal Gallo — Gallo Pawn & Loan, Lowfield; sells the stones (per Jo)
    orin_sable: Orin — "a dealer in old things"; phoned with an offer
    bellamy_doctor: the Bellamy Street doctor — Rin's GP contact
    lina_dalen: Lina Dalen — Imran's wife; night-diner server
    imran_dalen: Imran Dalen — recovering on a general ward
    agnieszka_wolak: Agnieszka Wolak — wharf landlady, cash room
    brannock_heavy: shaven-headed bully — Brannock/Choir muscle
    unit9_keeper: older man in a cardigan — keeps Unit 9
    ashfall_general_er: Ashfall General ER staff
    teodor_varga: Teodor Varga — ironworker, 2004 city job; meeting Thu 15:00
    court_runner: small slag creature — came out of the Southport grate
    police_sergeant_tip: police sergeant (Mara's contact)
  factions:
    merrow_utility_solutions: Merrow Utility Solutions — infrastructure contractor
    ashfall_transit_authority: Ashfall Transit Authority — runs the Red Line
    ash_choir: the Choir — name on M's contact; moves the charms
    brannock_freight: Brannock Freight Services — Unit 9, Exchange Yard (the courier's car)
  locations:
    hale_workshop: Hale Workshop, Morrow Ward
    the_last_stop: The Last Stop
    lowfield: Lowfield
    canal_embankment: Canal Street embankment relay huts
    kettering_laundromat: Suds & Spin laundromat, Kettering
    ferris_yard: Ferris Yard and Halden Lane
    sealed_red_spur: Sealed Red Spur (known by name and from Eli)
    bellamy_clinic: walk-in clinic, Bellamy Street
    wren_bridge_toll_hut: old tollkeeper's hut, Wren Bridge
    hartley_allotments: Hartley allotments, Kettering edge
    fishmarket_arcade: Fishmarket Arcade, wharf district
    city_risk_office: City Risk Management Office, Municipal Annex
    gallo_pawn: Gallo Pawn & Loan, Lowfield
    exchange_yard_unit9: Unit 9, Exchange Yard, Old Exchange
    signal_box_pub: The Signal Box, Ferris Road
    lowfield_cab_rank: Lowfield taxi rank and night diner
    exchange_yard: Exchange Yard, Old Exchange
    wharf_room: Mrs Wolak's back room (bolt-hole)
    ashfall_general: Ashfall General Hospital
    ironside_lane: Ironside Lane, Lower Docks
    southport_outfall: Southport outfall (Rin's camera)
    mercer_pump: Mercer flood pump (known from Eli)
    marisols_grill: Marisol's grill, Lowfield
  quests:
    find_eli_voss: Find Eli Voss and get him somewhere safe — completed
    laundromat_job: Clear whatever is in the Suds & Spin basement; $400 via Pike — completed
    ash_beneath: Find out what happened to Eli Voss and who is sending crews below the Red Line — available
  rights_obligations:
    workshop_lease: leasehold — Rin, Mrs Okafor
    pi_licence: licence — Rin, City of Ashfall
    voss_trace: contract — Rin, Nadia (completed, paid)
    laundromat_deal: brokered job — Rin, Pike, Rosa Fenn (closed, paid)
    eli_clinic_promise: informal promise — Rin, Nadia (closed, repaid)
    eli_case: contract — Rin, Eli (closed, paid $375)
    jo_cover_job: hire — Rin, Jo ($200 owed to Jo)
    city_contract: contract — Rin, City ($750 paid; $2,000 due Fri; Halden $1,500 open)
    charm_custody: chain of custody — Rin to Mara (two charms)
    eli_statement: appointment — Eli, Mara, Rin (done Sat; letter Mon)
    haller_knives: commission — Rin, Haller (completed)
    mara_meeting: appointment — Rin, Mara (held Oct 9)
    ada_bank_visit: appointment — Rin, Ada (Harland's Bank, Mon 09:30)
    warren_medical: paid service — Rin, Bellamy doctor, Lucy (report Wed)
    charm_custody_2: chain of custody — Rin to Mara (Lucy's charm)
    lucy_consent: consent — Lucy to Rin (medical report, name withheld)
    charm_custody_3: chain of custody — Rin to Mara (Imran's stone + footage)
    wharf_room_hold: room rental — Rin, Mrs Wolak (to 16 Nov)
    mara_retainer: proposed retainer — Rin, Mara
    varga_meeting: appointment — Rin, Varga (Thu 15:00)
    footage_custody: chain of custody — Rin to Mara (Tanner/Unit 9 footage)
```

---

# PART B — CAPSULE

```yaml
capsule:
  save_round: 90
  encoding: plain
  supersedes_deltas_through: 90
  records:
    active_world_pressures.glass_spread.actors :: ["orin_sable", "gallo_pawnbroker", "imran_dalen", "l_warren"]
    active_world_pressures.glass_spread.clock.filled :: R82: 4 — 2026-10-14 (3, Imran still wearing until 23:05 and stock moving; missed at the time) and 2026-10-18 (4, cell stock still moving via Mercer/Southport)
    active_world_pressures.glass_spread.clock.name :: Lowfield hollowing
    active_world_pressures.glass_spread.clock.on_fill :: If at least one wearer remains exposed, a still-exposed wearer reaches an acute danger point at their actual location. Otherwise a genuinely moving contaminated batch draws lesser demons only at its actual destination. Resolve witnesses and actors from state without inventing an affected buyer or automatically creating a public crisis; replace or retire this pressure only if its operating cause changes.
    active_world_pressures.glass_spread.clock.pace :: every 4 days while someone continues wearing contaminated glass or new stock actually circulates; repairs, isolation and destroyed stock may halt or reverse exposure
    active_world_pressures.glass_spread.clock.segments :: 6
    active_world_pressures.glass_spread.discovered_information :: {}
    active_world_pressures.glass_spread.name :: Luck stones in Lowfield
    active_world_pressures.glass_spread.origin :: Orin distributes cinder-glass stock via Gallo, a small Ash Choir handoff at Suds & Spin and couriers; these are connected to the Red Spur and can attract predators
    active_world_pressures.glass_spread.state.current :: R70: Imran's stone removed 2026-10-14 23:05 (in Rin's steel box); Lucy's removed Oct 8; Gallo holds three stones at home; cell stock moves via Mercer/Southport at low water
    active_world_pressures.glass_spread.trajectory :: untreated wearers worsen and active cash/stock handoffs expose more people; Gallo, Warren and the cell make their own moves, while residue draws lesser demons at real locations. Public crisis requires actual witnesses and information channels.
    active_world_pressures.seal_erosion.actors :: ["the_surveyor", "orin_sable", "jonas_rusk", "court_runner"]
    active_world_pressures.seal_erosion.clock.filled :: 1
    active_world_pressures.seal_erosion.clock.name :: seal erosion
    active_world_pressures.seal_erosion.clock.on_fill :: if eight legitimately earned fills accumulate without successful structural intervention, the patched main seal gives way sufficiently to open a larger route. The Court must still physically move through passable galleries and overcome real defenses. Once a breach or full restoration changes the process, retire this erosion pressure and use its actual ongoing consequence as a successor only when warranted.
    active_world_pressures.seal_erosion.clock.pace :: every 2 weeks while actual extraction or deliberate below-seam damage continues; otherwise every 1 month from load cycling only if the pre-existing crack remains unrepaired and mechanically stressed. Never apply both modes in one interval; proven stabilization halts it.
    active_world_pressures.seal_erosion.clock.segments :: 8
    active_world_pressures.seal_erosion.discovered_information :: {}
    active_world_pressures.seal_erosion.name :: Red Spur seal erosion
    active_world_pressures.seal_erosion.origin :: Orin's months of residue removal through door 7-B weakened the 2004 patch and opened a hairline, still-active load-bearing fracture at a small bleed-drain. Continuing shipments accelerate wear; even without shipments, periodic load cycles stress the unreinforced crack slowly.
    active_world_pressures.seal_erosion.state.current :: the main seal still blocks large Court entities. A narrow, damaged side-drain slit admits lesser-sized bodies at low water, but the outer gallery and freight corridors are not a stable invasion route. Fracture growth can be measured near the far seam; suitable repair or isolation can stop it.
    active_world_pressures.seal_erosion.trajectory :: extraction and active sabotage strain the patch faster; if all such action stops, slow cyclical stress remains until the crack is physically stabilized. Repair, replacement, or changes to water and support loads can slow, reverse or arrest it.
    continuity_status.player_corrected.28 :: R33: GM omitted that Rin photographed Warren's M (Choir) thread at R28 (ordinary PI competence) → Rin's phone holds 3 photos of the thread; R33 replayed with screenshots sent
    continuity_status.player_corrected.36 :: R36: GM omitted that Rin photographed both fight scenes (hut 3 slag and claw marks Oct 6; Suds & Spin basement pipes, bones, slag Oct 7) → photos on Rin's phone; no later outcome changed
    continuity_status.player_corrected.40 :: R40: R33 entries replaced Jo's whole credit and grievance lists toward Rin, dropping the Round-0 entries → both lists restored with old and new entries
    continuity_status.player_corrected.45 :: R45: GM narrowed "collect the stones" to the hut 3 pair → Rin also collected Warren's charm from Hartley the same morning; no later outcome changed
    continuity_status.player_corrected.66 :: R66: GM misread "check the up and down" as Gallo's supply chain and ran an extra evening watch, police stop and property search → R66 replayed: Rin watched one smoke break to read why Gallo scans the street and left at 17:30; no police contact, no property search
    continuity_status.player_corrected.72 :: R72: GM omitted that Rin clipped his camera on before entering the Dalens' flat (ordinary PI documentation) → camera recorded from 22:55 Oct 14: the stone's faint red glow, the cut, Imran's shaking and the mumbling with audio; no outcome changed
    continuity_status.player_corrected.77 :: R77: the night taxi Rin took from the hospital to Rook Street 03:00 Oct 15 was not charged → $25 deducted now
    continuity_status.player_corrected.80 :: R80: R78 entry replaced Mrs Okafor's credit list toward Rin, dropping the Round-0 entry → list restored with both
    continuity_status.player_corrected.82 :: R82: glass_spread clock fill due 2026-10-14 was not applied → applied now with the Oct 18 fill; clock 4/6
    continuity_status.player_corrected.90 :: R90: routine entries at R86/R88/R89 were written as top-level "routines.*" ids → filed at their owners (player.routines, npcs.eli_voss.state.routines)
    continuity_status.round0_revisions.l_warren_gender :: R59: {field: npcs.l_warren.gender, was: unspecified, now: woman (about 23), reason: Rin has met her in person; background left it unset, round: 59}
    continuity_status.round0_revisions.names_completed :: R59: {field: npcs.l_warren.name / npcs.dale.name / npcs.vic.name, was: "L. Warren" / "Dale" / "Vic", now: Lucy Warren / Dale Brennan / Vic Moreno, reason: background left names incomplete; player asked to correct, round: 59}
    continuity_status.round0_revisions.nightglass_origin :: R17: {field: Nightglass Blade origin, was: unstated, now: Ada gave it to Rin at sixteen from the sealer parent's things; maker unknown to Rin and Ada, reason: player asked to commit it from the world, round: 17}
    factions.ash_choir.capability.reach :: scattered safehouses and intermediaries
    factions.ash_choir.discovered_information :: {}
    factions.ash_choir.drives.fears :: ["exposure", "betrayal by patrons"]
    factions.ash_choir.drives.wants :: ["power", "protection", "knowledge", "favour"]
    factions.ash_choir.knowledge.channels :: ["cell leaders", "ritual contacts", "criminal intermediaries"]
    factions.ash_choir.knowledge.facts :: {}
    factions.ash_choir.name :: The Ash Choir
    factions.ash_choir.relationships :: {}
    factions.ash_choir.role :: loose human occult network trading with demonic powers
    factions.ash_choir.state.structure :: cellular; members know different amounts
    factions.ashfall_transit_authority.capability.institutional_reach :: controls access to its depots, tunnels and records
    factions.ashfall_transit_authority.discovered_information :: {}
    factions.ashfall_transit_authority.drives.fears :: ["public incidents", "contractor scandal"]
    factions.ashfall_transit_authority.drives.wants :: ["trains running", "low liability"]
    factions.ashfall_transit_authority.knowledge.channels :: ["work orders", "safety liaison", "security cameras"]
    factions.ashfall_transit_authority.knowledge.facts :: {}
    factions.ashfall_transit_authority.name :: Ashfall Transit Authority
    factions.ashfall_transit_authority.relationships :: {}
    factions.ashfall_transit_authority.role :: city transit operator; runs the subway, service tunnels, pump stations and maintenance network
    factions.ashfall_transit_authority.state.public_status :: ordinary municipal agency
    factions.ashfall_transit_authority.state.records :: keeps original gate video (30-day retention), shift sign-outs and work orders outside Merrow's edit access
    factions.brannock_freight :: R65: {name: Brannock Freight Services Ltd, role: small courier, light freight and storage company at Unit 9, Exchange Yard, Old Exchange; inc. 2019; director Aidan Brannock; accounts tiny and late; moves Choir stock (OX-9 stencils), state: {public_status: ordinary small firm}, capability: {reach: a few vans and cars, one unit}}
    factions.brannock_freight.state.summons :: R82: Trading Standards summoned Brannock Freight after the Unit 9 seizure, 2026-10-19
    factions.brannock_freight.state.vehicles :: R85: grey Nissan KT 72 VRN and white Ford Transit van AF 19 KXT; only premises Unit 9; director Aidan Brannock, home address in Saltgate; no other leases
    factions.cinder_court.capability.reach :: strong in the lower routes; none on the surface without a breach or agent
    factions.cinder_court.discovered_information :: {}
    factions.cinder_court.drives.fears :: ["rival control", "a large human response"]
    factions.cinder_court.drives.wants :: ["stable routes", "territory", "bargains"]
    factions.cinder_court.knowledge.channels :: ["emissaries", "bound sites", "human intermediaries"]
    factions.cinder_court.knowledge.facts :: {}
    factions.cinder_court.name :: The Cinder Court
    factions.cinder_court.relationships :: {}
    factions.cinder_court.role :: loose demonic compact holding deep routes beneath Ashfall
    factions.cinder_court.state.surface_presence :: minimal
    factions.cinder_court.state.unity :: transactional; rivals within
    factions.lantern_office.capability.institutional_reach :: limited databases and a small field response
    factions.lantern_office.discovered_information :: {}
    factions.lantern_office.drives.fears :: ["public panic", "political closure", "acting on bad evidence"]
    factions.lantern_office.drives.wants :: ["verify and contain real hazards"]
    factions.lantern_office.knowledge.channels :: ["restricted incident reports", "archived cases", "covert field contacts", "municipal risk report requests"]
    factions.lantern_office.knowledge.facts.demons :: real and poorly catalogued
    factions.lantern_office.name :: The Lantern Office
    factions.lantern_office.relationships :: {}
    factions.lantern_office.role :: small secret municipal occult-containment cell
    factions.lantern_office.state.public_status :: unacknowledged
    factions.lantern_office.state.site_attention :: Ferris Yard and other old-route outages are under routine risk review, not confirmed demonic incidents
    factions.lantern_office.state.staffing :: small and underfunded; Mara and one part-time field assistant can perform a limited field inspection, not a raid
    factions.merrow_utility_solutions.capability.institutional_reach :: citywide contractor access where contracts permit
    factions.merrow_utility_solutions.discovered_information :: {}
    factions.merrow_utility_solutions.drives.fears :: ["scandal", "criminal investigation", "losing city contracts"]
    factions.merrow_utility_solutions.drives.wants :: ["contracts", "low liability"]
    factions.merrow_utility_solutions.knowledge.channels :: ["work orders", "supervisors", "city contracts", "compliance reporting"]
    factions.merrow_utility_solutions.knowledge.facts :: {}
    factions.merrow_utility_solutions.name :: Merrow Utility Solutions
    factions.merrow_utility_solutions.relationships :: {}
    factions.merrow_utility_solutions.role :: major infrastructure contractor; one night supervisor's crew is compromised
    factions.merrow_utility_solutions.state.audit :: corporate compliance could investigate Rusk if an external discrepancy reaches it; it is not part of his scheme and cannot be assumed hostile to Rin.
    factions.merrow_utility_solutions.state.compromise :: Rusk and two crew men only; the rest of the company knows nothing
    factions.merrow_utility_solutions.state.public_status :: legitimate contractor
    locations.ashfall_general :: R72: {name: Ashfall General Hospital, emergency department, conditions: {surface: city hospital ER, ambulance bay, triage desk}, challenge_band: {min: 1, max: 2, basis: hospital}}
    locations.ashfall_general.conditions.er_record :: R73: ER notes 2026-10-15: prolonged exposure to an unknown warm pendant, removed 23:05, rigors 23:15; anonymised GP comparison report photographed from Rin's phone; doctor recorded Rin's name and PI licence as the man who brought him in and holds the object for the city
    locations.bellamy_clinic :: R11: {name: walk-in clinic, Bellamy Street, Morrow Ward, conditions: {surface: cash accepted, first name only, older doctor who does not ask how injuries happened; Rin has used it before}, challenge_band: {min: 1, max: 2, basis: ordinary clinic}}
    locations.canal_embankment.challenge_band.basis :: derelict infrastructure; whatever the shard draws
    locations.canal_embankment.challenge_band.max :: 4
    locations.canal_embankment.challenge_band.min :: 1
    locations.canal_embankment.conditions.character :: six padlocked brick relay huts on a disused rail embankment, weeds, a service road
    locations.canal_embankment.conditions.hut_3_door :: R2: hasp rusted through; Eli pulled the door shut and wedged it from inside on Oct 5; fresh claw scratches outside from the cinderling
    locations.canal_embankment.conditions.hut_3_lock :: R45: hut 3 door still chained with Rin's padlock; empty inside
    locations.canal_embankment.name :: Canal Street embankment relay huts
    locations.city_risk_office.challenge_band.basis :: ordinary bureaucracy, records controls and small covert containment resources
    locations.city_risk_office.challenge_band.max :: 4
    locations.city_risk_office.challenge_band.min :: 1
    locations.city_risk_office.conditions.counter_3 :: R30: public hazard counter, Form RM-12 (name and contact optional); clerk logs reports to an analyst, flags urgent ones the same day; Q3 service interruption summary on the notice board lists three "cause undetermined" lines incl. Ferris Yard Sept 15 overnight
    locations.city_risk_office.conditions.counter_3_clerk :: R31: young clerk at Counter 3; did not recognise the word "cinderling"; routes plain pest reports to Environmental Health (1st floor, Room 4) and logs pest-caused hazards (fire, structural, wiring, gas, flooding) on RM-12 for an analyst
    locations.city_risk_office.conditions.evidence :: Mara has three independent outage summaries but no known secret culprit, authority to seize charm stock or field team capable of fighting demons. Her office can fund a verified external hunter.
    locations.city_risk_office.conditions.rm12_0417 :: R32: hazard report RM-12 ref 26-1008-0417 filed by Rin 12:20 Oct 8: pest-caused fire hazard, multiple locations, example Kettering commercial basement, "cinderlings" drawn to dark-glass "lucky charms" being sold, carriers ill; Rin's card attached; flagged fire priority for an analyst today
    locations.city_risk_office.conditions.surface :: public desk, hazard reports, notice board, permit index, staff offices and restricted Lantern archive
    locations.city_risk_office.name :: Municipal Risk Management Office, central Ashfall
    locations.exchange_yard :: R80: {name: Exchange Yard, Old Exchange, conditions: {surface: iron-gated cobbled courtyard of numbered roller-shutter trade units in the old merchants' quarter}, challenge_band: {min: 2, max: 5, basis: private trade yard}}
    locations.exchange_yard_unit9 :: R65: {name: Unit 9, Exchange Yard, Old Exchange, conditions: {surface: registered address of Brannock Freight Services; the OX-9 freight code}, challenge_band: {min: 2, max: 5, basis: private freight unit tied to the charm trade}}
    locations.exchange_yard_unit9.conditions.inside :: R80: steel shelving and stacked cardboard cartons stencilled OX-9, seen through the half-raised shutter 23:50 Oct 16
    locations.exchange_yard_unit9.conditions.seized :: R82: Trading Standards seized 3 cartons (72 charms) and a raw-glass crate with Merrow tape from Unit 9, 10:00 Oct 19; unit under notice
    locations.ferris_yard.challenge_band.basis :: industrial site, night security, a small criminal crew and possible municipal responders
    locations.ferris_yard.challenge_band.max :: 5
    locations.ferris_yard.challenge_band.min :: 2
    locations.ferris_yard.conditions.evidence :: Halden gate camera and visitor sheets are Transit-controlled, not Rusk-controlled; 30-day footage retention
    locations.ferris_yard.conditions.night_guard :: R20: Bernie, depot night security, gatehouse at the main entrance; fence walk about hourly; coffee at the kiosk ~midnight (per the kiosk owner)
    locations.ferris_yard.conditions.surface :: transit depot, night kiosk, Halden Lane service building behind chain-link with a camera on the gate
    locations.ferris_yard.conditions.use :: Merrow vans use Halden Lane for irregular nighttime loads. Rusk can control his local paperwork and crew, not independent Transit archives or the Mercer pump.
    locations.ferris_yard.name :: Ferris Yard and Halden Lane
    locations.fishmarket_arcade :: R24: {name: Fishmarket Arcade, wharf district, conditions: {surface: covered market arcade; Haller's knife-grinding stall}, challenge_band: {min: 1, max: 3, basis: public market}}
    locations.gallo_pawn.challenge_band.basis :: public shop, cautious owner and possible criminal intermediaries
    locations.gallo_pawn.challenge_band.max :: 4
    locations.gallo_pawn.challenge_band.min :: 1
    locations.gallo_pawn.conditions.channels :: stock arrives through an Old Exchange courier; the under-counter stones are not publicly advertised
    locations.gallo_pawn.conditions.gallo_home_emptied :: R79: Gallo's stones and batch notes taken from 14 Tanner Lane 23:20 Oct 16 by the courier and a shaven-headed man
    locations.gallo_pawn.conditions.surface :: legitimate pawnbroker, back-counter charm sales, ordinary till receipts and customer records
    locations.gallo_pawn.name :: Gallo Pawn & Loan, Tanner Street, Lowfield
    locations.hale_workshop.challenge_band.basis :: ordinary urban workplace
    locations.hale_workshop.challenge_band.max :: 4
    locations.hale_workshop.challenge_band.min :: 1
    locations.hale_workshop.conditions.access :: Rin rents the street-level workshop and back room; a hand-painted sign says RECOVERY & ODD JOBS
    locations.hale_workshop.conditions.public_surface :: ordinary mixed commercial block; landlady upstairs
    locations.hale_workshop.name :: Hale Workshop, Morrow Ward
    locations.hartley_allotments :: R29: {name: Hartley allotments, Kettering edge, conditions: {surface: council-closed allotments behind a broken gate, overgrown, collapsing tool sheds; nobody through in months, shed_box: Warren's worn charm in Rin's second locked steel cash box (key with Rin) under rotted seed trays in the last shed, 2026-10-08 10:45; unexposed}, challenge_band: {min: 1, max: 2, basis: abandoned allotments}}
    locations.hartley_allotments.conditions.shed_box :: R45: no longer holds — cash box with Warren's charm taken out by Rin 08:50 Oct 9
    locations.ironside_lane :: R86: {name: Ironside Lane, Lower Docks, conditions: {surface: old dockside street; Teodor Varga's ironworks}, challenge_band: {min: 1, max: 2, basis: quiet trade street}}
    locations.kettering_laundromat.challenge_band.basis :: one lesser demon in a cramped basement
    locations.kettering_laundromat.challenge_band.max :: 4
    locations.kettering_laundromat.challenge_band.min :: 2
    locations.kettering_laundromat.conditions.back_alley :: R38: narrow alley behind the block: back door under one caged bulb, wheelie bins, garages opposite; exits to the side street and to the delivery yard of a closed carpet warehouse
    locations.kettering_laundromat.conditions.problem :: a cinderling nests beside a small cache of stock held by tenant L. Warren for a later Ash Choir collection; the cache gives off heat and scorch marks. Warren is not guaranteed to stay or hand it over.
    locations.kettering_laundromat.name :: Suds & Spin laundromat, Kettering
    locations.lower_works.challenge_band.basis :: demonic territory
    locations.lower_works.challenge_band.max :: 14
    locations.lower_works.challenge_band.min :: 7
    locations.lower_works.conditions.access :: not on public maps; only past the old seal
    locations.lower_works.conditions.status :: older chambers below municipal construction
    locations.lower_works.name :: The Lower Works
    locations.lowfield.challenge_band.basis :: working-class district; street crime; lesser demons follow the charms
    locations.lowfield.challenge_band.max :: 5
    locations.lowfield.challenge_band.min :: 1
    locations.lowfield.conditions.character :: older brick walk-ups, corner stores, transit workers' neighbourhood; Eli's flat, Tomas's flat, Gallo Pawn & Loan
    locations.lowfield.conditions.dalen_flat :: R70: 31B Rook Street, above the bakery; Lina gave Rin a spare key
    locations.lowfield.name :: Lowfield
    locations.lowfield_cab_rank.challenge_band.basis :: ordinary public streets with a developing, not yet recognized occult hazard
    locations.lowfield_cab_rank.challenge_band.max :: 5
    locations.lowfield_cab_rank.challenge_band.min :: 1
    locations.lowfield_cab_rank.conditions.problem :: Imran is the longer-exposed of two identified current charm wearers; his symptoms need not point automatically to Gallo. Public disturbance is possible, not guaranteed.
    locations.lowfield_cab_rank.conditions.surface :: shared dispatch, driver shift sheets, vehicle dashcams and a small queue outside the night diner
    locations.lowfield_cab_rank.name :: Lowfield taxi rank and dispatch office
    locations.marisols_grill :: R82: {name: Marisol's, Lowfield high street, conditions: {surface: busy little grill where Nadia is shift manager}, challenge_band: {min: 1, max: 2, basis: restaurant}}
    locations.mercer_pump.challenge_band.basis :: maintenance access, unstable water, lesser demons only where the residue supports them
    locations.mercer_pump.challenge_band.max :: 6
    locations.mercer_pump.challenge_band.min :: 2
    locations.mercer_pump.conditions.access :: street-level locked pump room and service stairs down to an outer Red Spur gallery, independent of 7-B; access requires lawful permission, a workable maintenance route or real bypass
    locations.mercer_pump.conditions.discovery :: night worker has noted scorch-coloured grit and a damaged screen; runoff patterns and a faded maintenance stencil point toward Southport outfall
    locations.mercer_pump.conditions.hazards :: automatic impellers, fluctuating water, unsecured grilles and heat/cinder residue washed from the bleed-drain; a cinderling has scavenged near the lower baffle
    locations.mercer_pump.conditions.oct10_traces :: R53: fresh black-red grit at the sump screen and disturbed baffle after the 04:00 Oct 10 low water
    locations.mercer_pump.conditions.surface :: working municipal flood-control building and rusting pump gallery south of the Red Line; staffing is sparse at night
    locations.mercer_pump.name :: Mercer municipal flood pump and old overflow sump
    locations.sealed_red_spur.challenge_band.basis :: smuggling route, lesser demons drawn to the residue, the spur warden
    locations.sealed_red_spur.challenge_band.max :: 8
    locations.sealed_red_spur.challenge_band.min :: 3
    locations.sealed_red_spur.conditions.access :: two physically distinct outer approaches: door 7-B from Halden freight access, and a maintenance sump via Mercer flood pump and Southport culvert. Neither crosses the active main seal; the narrow damaged bleed-drain through its side patch passes only lesser-sized bodies under suitable water conditions
    locations.sealed_red_spur.conditions.discovery :: Halden crew traffic, Eli and cargo traces identify 7-B; Southport runoff, Mercer pump-worker sightings and an old maintenance marker can independently identify the culvert. Blocking one access does not erase the other.
    locations.sealed_red_spur.conditions.infrastructure :: three dead stations, pump corridors, patched masonry; cinder glass crusts the far tunnel walls; the seal sigil is in the masonry at the far platform
    locations.sealed_red_spur.conditions.resonance :: within 20 metres of the main seal, the sealer-line mark registers; a surge elsewhere only registers if near unneutralized connected residue or old route masonry. The Surveyor does not thereby know Rin's identity.
    locations.sealed_red_spur.name :: Sealed Red Spur
    locations.signal_box_pub :: R61: {name: The Signal Box, Ferris Road, conditions: {surface: railworkers' pub two streets from Ferris Yard; brown wood, timetables, darts, football on the telly}, challenge_band: {min: 1, max: 2, basis: neighbourhood pub}}
    locations.southport_outfall.challenge_band.basis :: water, cramped access and creatures emerging by a real route
    locations.southport_outfall.challenge_band.max :: 5
    locations.southport_outfall.challenge_band.min :: 2
    locations.southport_outfall.conditions.oct10_traces :: R53: wet three-toed prints on the outfall apron and a loosened grate fastener, morning of Oct 10
    locations.southport_outfall.conditions.rin_camera :: R86: Rin's clip camera on a cable bracket under the downstream handrail of the footbridge 30 m from the outfall since 06:20 Oct 20; covers the grate and apron; night mode; battery ~2 days
    locations.southport_outfall.conditions.route :: old culvert leads upstream into Mercer pump sump and from there the outer Red Spur gallery; the culvert is not always safely passable
    locations.southport_outfall.conditions.surface :: open tidal embankment, grated runoff mouth and municipal inspection marker, accessible without Halden security
    locations.southport_outfall.conditions.trace :: isolated black-red sediment, displaced grate fasteners and occasional animal reports; a runner needs low water and unobstructed baffles
    locations.southport_outfall.name :: Southport canal outfall and storm culvert
    locations.the_last_stop.challenge_band.basis :: neighbourhood bar
    locations.the_last_stop.challenge_band.max :: 3
    locations.the_last_stop.challenge_band.min :: 1
    locations.the_last_stop.conditions.character :: narrow bar, trains overhead every six minutes, a corkboard of odd jobs behind the counter
    locations.the_last_stop.name :: The Last Stop, under the elevated line, Morrow Ward
    locations.wharf_room :: R78: {name: back room above the old chandlery, wharf, conditions: {surface: Mrs Wolak's cash room; Rin's bolt-hole, key on a fisherman's float; go-bag in the wardrobe with $400 sewn in the lining, spare clothes, delivery jacket, vest and clipboard, first-aid kit, torch, charger, food}, challenge_band: {min: 1, max: 2, basis: quiet lodging}}
    locations.wren_bridge_toll_hut :: R17: {name: old tollkeeper's hut, Wren Bridge approach ramp, Morrow Ward edge, conditions: {surface: brick hut with steel shutter, empty for decades, usually deserted; Rin knows it from courier work, now: city 14 bus broken down at the ramp foot 11:50 Oct 7, ~20 passengers waiting under the bridge, some sheltering at the hut}, challenge_band: {min: 1, max: 2, basis: abandoned roadside structure}}
    locations.wren_bridge_toll_hut.conditions.now :: R18: bus replaced 12:20; ramp empty again apart from the broken bus and its driver
    locations.wren_bridge_toll_hut.conditions.shard_box :: R18: Eli's shard in Rin's locked steel cash box (key with Rin), back corner behind a broken chair, shutter bolted as found, 2026-10-07 12:25; unexposed
    locked_case_truths.civic_collision.cause :: Mara flagged three unexplained outages and requested ordinary records from Merrow on Oct 5. The compromised crew can quietly conceal its own log but does not control Transit video. Mara lacks field strength, automatic access and any grounds to identify the occult cause. On-site pump damage and witnesses may independently intersect her inquiry or Rin's path.
    locked_case_truths.civic_collision.discovered_information :: {}
    locked_case_truths.civic_collision.discovered_information.crew_moved :: R82: via Eli/Tomas 2026-10-17: Merrow's night crew moved to Kettering depot; Rusk still off sick and unseen
    locked_case_truths.civic_collision.discovered_information.halden_suspended :: R74: Mara told Rin 2026-10-15: Transit Safety suspended Merrow's after-hours Halden access 16:00 Oct 14; Rusk phoned in sick to his compliance meeting
    locked_case_truths.civic_collision.discovered_information.kiosk_account :: R20: kiosk owner told Rin 2026-10-07: back half of the yard goes dark 2–3 nights a week, Merrow vans in Halden 01:00–02:00, Transit staff locked out for "Merrow works"
    locked_case_truths.civic_collision.discovered_information.mara_contact :: R36: Mara Quill (City Risk Management) took Rin's report; reacted to Ferris Yard / Halden Lane; asked for evidence and a meeting
    locked_case_truths.civic_collision.discovered_information.mara_offer :: R47: Mara told Rin 2026-10-09 that Merrow blames aging equipment for Ferris, that she requested Transit's original sign-out sheets for Sept–Oct, and offered $750 for the report and custody of the charms, $1,500 for a documented Halden window from outside
    locked_case_truths.civic_collision.discovered_information.mara_tipoff :: R60: Mara reads the on-time window after Rin's call with Orin as a tip-off, 2026-10-11
    locked_case_truths.civic_collision.discovered_information.public_summary :: R30: Rin read the posted Q3 summary 2026-10-08: three "cause undetermined" interruptions incl. Ferris Yard Sept 15
    locked_case_truths.civic_collision.discovered_information.sheets_verdict :: R67: Mara confirmed 2026-10-14: Transit's original sheets show 1-hour windows; Merrow's copies show 2–3 hours with a non-existent Transit code; she is asking Transit Safety to suspend Merrow's after-hours Halden access and writing to Merrow compliance
    locked_case_truths.civic_collision.discovered_information.yard_gossip :: R76: via Eli and Tomas 2026-10-15: Halden locked after hours, Merrow night crew removed, audit talk, Rusk off sick
    locked_case_truths.civic_collision.evidence.camera :: Halden footage recorded Eli being chased on Oct 4; retention is thirty days
    locked_case_truths.civic_collision.evidence.inspector_notices :: the October 5 document request can be followed through city and Merrow records
    locked_case_truths.civic_collision.evidence.mercers :: independent stormwater notices report overheated sediment and a loose sump screen; Mara has not connected these to demon activity
    locked_case_truths.civic_collision.evidence.public_outages :: dates and sites in city risk summaries overlap Ferris and the Red Line service route
    locked_case_truths.civic_collision.evidence.transit_duplicates :: Transit log copies disagree with Rusk's locally modified end times
    locked_case_truths.civic_collision.evidence.vic_testimony :: Vic knows a specific van, run and unauthorized doorway; risk of testimony depends on his fear
    locked_case_truths.civic_collision.routes :: public incident witnesses, Ferris field observation, Merrow crew decisions or Mercer pump conditions can generate independent action; ordinary logs corroborate but do not safely access the Spur. Mara can ask for help, refer a hazard or pay a credible hunter but does not automatically close the site.
    locked_case_truths.civic_collision.state.archive :: Transit retains originals, but records support evidence rather than replace physical action at the compromised sites
    locked_case_truths.civic_collision.state.mara :: a tentative public-safety file and one request pending; no two-person containment team or proven culprit
    locked_case_truths.civic_collision.state.rusk :: knows city staff may inspect; knows nothing of Rin or the Voss inquiry
    locked_case_truths.glass_trade.cause :: Orin buys the glass from Rusk's crew, sells part as luck stones through Gallo and the rest to Ash Choir cells. The stones work a little at first; they draw cinderlings, and a wearer of weeks starts to hollow until a lesser demon can ride them.
    locked_case_truths.glass_trade.discovered_information :: {}
    locked_case_truths.glass_trade.discovered_information.brannock_records :: R85: Rin's records search 2026-10-19: Brannock has the Nissan and a white Transit van AF 19 KXT; Unit 9 is its only premises; director Aidan Brannock lives in Saltgate
    locked_case_truths.glass_trade.discovered_information.charms_shown_eli :: R16: Eli saw the two laundromat charms and recognised the same glass as his shard, 2026-10-07
    locked_case_truths.glass_trade.discovered_information.courier_photos :: R40: Jo photographed the courier (forties, flattened nose, eyebrow scar) and his dark grey Nissan, plate KT 72 VRN, 2026-10-08 22:05
    locked_case_truths.glass_trade.discovered_information.gallo_lead :: R33: Jo told Rin 2026-10-08 that Gallo's pawnshop in Lowfield sells stones like that under the counter
    locked_case_truths.glass_trade.discovered_information.gallo_scanning :: R66: Rin read Gallo's street-checking 17:20 Oct 13: he scans parked cars, upper windows and the bus-stop corner, smokes back to the wall — afraid of being watched or approached, not waiting for a delivery
    locked_case_truths.glass_trade.discovered_information.gallo_watch :: R65: Rin watched Gallo's 14:00–17:00 Oct 13: ordinary trade; Gallo nervous, checks the street; at 15:40 took a small bag to 14 Tanner Lane and returned without it
    locked_case_truths.glass_trade.discovered_information.imran_footage :: R72: Rin's camera footage 2026-10-14 22:55 onward: Imran's stone glowing faintly red in the dark, the cord cut, the stone boxed, Imran's shaking and his mumbling in an unknown language (audio)
    locked_case_truths.glass_trade.discovered_information.imran_recording :: R82: Lina sent Rin a 4-minute recording of Imran's sleep-talk 2026-10-17 03:00: three or four hard, clipped words repeated with small changes, like reciting directions; unknown language; Rin forwarded it to Mara
    locked_case_truths.glass_trade.discovered_information.imran_reflex :: R69: Lina says Imran grabbed her wrist hard in his sleep last week when she touched the stone and didn't remember it
    locked_case_truths.glass_trade.discovered_information.imran_sale :: R68: Lina told Rin 2026-10-14: Imran Dalen bought a stone under the counter at Gallo's ~6 weeks ago for $60; wears it daily; cold, weight loss, lost hours, missed shifts; clinic Monday said stress/anaemia; won't take it off; drivers say his eyes have changed
    locked_case_truths.glass_trade.discovered_information.imran_stone :: R70: Rin cut Imran's stone off 23:05 Oct 14; it glowed faintly red in the dark and was very hot; now in Rin's third steel box; Imran went into severe chills and mumbled in an unknown language within ten minutes
    locked_case_truths.glass_trade.discovered_information.jo_client_claim :: R21: Jo told Rin 2026-10-07 22:35 that an unnamed client claims the Kettering charms as stored property and hired her to get them back
    locked_case_truths.glass_trade.discovered_information.laundromat_box :: R14: Rin opened the cache 2026-10-07: two charms matching Eli's shard, freight stencil OX-9 → KETT, courier tie, space for a third
    locked_case_truths.glass_trade.discovered_information.lucy_report :: R66: signed medical report on Lucy Warren 2026-10-14: anaemia, low white cells, raised liver enzyme, low core temperature, weight loss; metabolic strain improving since the warm object was removed
    locked_case_truths.glass_trade.discovered_information.m_cutoff :: R57: Warren forwarded M's 2026-10-11 07:02 message cutting Warren loose: no more boxes, don't contact, don't talk, keep the $200, "good luck"
    locked_case_truths.glass_trade.discovered_information.m_thread :: R28: Rin saw Warren's M (Choir) thread 2026-10-08: box arrived Sept 25, pickup Oct 8 22:00 back door for $200, "keep one for yourself, good luck charm", Warren's Oct 7 message naming Rin, M's reply "stay put, be there at 10"; carton from "the Exchange"; courier wears a big coat with the hood up
    locked_case_truths.glass_trade.discovered_information.orin_call :: R51: a man calling himself Orin, "a dealer in old things", phoned Rin 2026-10-09 18:00: claims the two Kettering pieces as his, offers $2,000 cash for them and work with "very little paperwork"
    locked_case_truths.glass_trade.discovered_information.plate_trace :: R65: KT 72 VRN is registered to Brannock Freight Services Ltd, Unit 9 Exchange Yard (OX-9), director Aidan Brannock; M's number is an unregistered prepaid SIM, 2026-10-13
    locked_case_truths.glass_trade.discovered_information.shard_seen :: R5: Rin saw Eli's shard (dark glass, red core, warm)
    locked_case_truths.glass_trade.discovered_information.tanner_collection :: R79: Rin filmed 23:20 Oct 16 at 14 Tanner Lane: the grey Nissan KT 72 VRN, the courier and a shaven-headed man taking Gallo's zipped bag and a ledger-sized notebook and papers; the shaven-headed man jabbed Gallo and threatened him; the car left toward the ring road
    locked_case_truths.glass_trade.discovered_information.trading_standards_route :: R67: Mara says Trading Standards can seize dangerous consumer goods at a shop given a doctor's report, a sample and the shop; she needs the holder's written consent and evidence tying the stones to Gallo's
    locked_case_truths.glass_trade.discovered_information.unit9_delivery :: R80: Rin tailed the grey Nissan from 14 Tanner Lane to Exchange Yard, Old Exchange, 2026-10-16; filmed Unit 9's shutter opening on shelving and OX-9 cartons, an older man in a cardigan taking Gallo's bag and notebook from the shaven-headed man; courier and shaven-headed man stayed inside
    locked_case_truths.glass_trade.discovered_information.unit9_seizure :: R82: Mara told Rin 2026-10-19: Trading Standards seized 72 charms and a warm crate of raw black glass with Merrow tape from Unit 9; all sealed in a windowless room; keeper silent; Brannock summoned
    locked_case_truths.glass_trade.discovered_information.warren_admission :: R27: Warren admitted being paid to hold the box for a collection 2026-10-08 22:00 at the alley back door, and telling the collectors Rin took it
    locked_case_truths.glass_trade.discovered_information.warren_charm :: R15: Rin saw Warren wearing a matching black cord under the hoodie, grey-sheened skin; Warren denied the box, 2026-10-07
    locked_case_truths.glass_trade.discovered_information.warren_exam :: R59: Lucy Warren's exam 2026-10-11: low core temperature, low BP, weight loss, a healing thermal mark where the charm hung; bloods pending Wednesday
    locked_case_truths.glass_trade.discovered_information.worn_charm_stored :: R29: Rin holds Warren's worn charm, locked at the Hartley allotments shed since 2026-10-08
    locked_case_truths.glass_trade.evidence.courier :: Orin's usual Old Exchange courier collects stock money through Gallo; separate small-cell stock moves through Warren and Mercer when the machinery permits.
    locked_case_truths.glass_trade.evidence.eli_shard :: Eli's shard matches the stones
    locked_case_truths.glass_trade.evidence.gallo :: Gallo makes selective under-counter sales and has only partial batch and courier notes, not a complete indexed list of buyers or an automatic confession
    locked_case_truths.glass_trade.evidence.hollowing_cabbie :: Imran Dalen has worn his charm for five weeks; Lina noticed the changes and his dispatch colleagues know routes. He can recall the shop but there is no convenient receipt in his car.
    locked_case_truths.glass_trade.evidence.jo :: Jo is already testing a charm, so she can independently trace or intercept Gallo stock; she does not yet know Orin's purpose. If Orin recruits her later, she can learn a different partial story.
    locked_case_truths.glass_trade.evidence.kestrel :: Kestrel is already sniffing at Gallo's
    locked_case_truths.glass_trade.evidence.laundromat_box :: Warren hides a small cell cache near the boiler beside a cinderling nest; the carton's freight stencil and a scorch-marked delivery tie mark identify a route, not a universal buyer roster
    locked_case_truths.glass_trade.evidence.supply :: physical glass lots and crate marks, courier movement, demon attraction and pump sediment link Old Exchange traffic with Halden and the Mercer/Southport outer route, without needing exhaustive records.
    locked_case_truths.glass_trade.evidence.warren :: L. Warren at Suds & Spin wore a charm for nine days and hides cell stock; a scheduled collector may move it. Warren can flee, bargain or be endangered before Rin arrives.
    locked_case_truths.glass_trade.routes :: Gallo or Jo/courier to Orin; Warren's damaged basement cache to Old Exchange or Mercer; Imran, Lina and an actual public incident to contaminated stock; Eli's shard to a matching physical lot. Each involves actors or contested terrain and may end peacefully, violently or inconclusively; no route requires a sequence of buyer interviews.
    locked_case_truths.hale_bloodline.cause :: Rin's absent parent is the demon who set the Red Spur seal. Ada hid this to keep the Court and occult brokers away from the line.
    locked_case_truths.hale_bloodline.discovered_information :: {}
    locked_case_truths.hale_bloodline.discovered_information.ada_2004 :: R55: Ada told Rin 2026-10-10: his parent, a being from below who broke from a "court", sealed something under the Red Line in autumn 2004 after Rin's birth that spring; gave Rin to Ada and vanished; the blade was the parent's; letters in a deposit box at Harland's Bank, Wexley
    locked_case_truths.hale_bloodline.discovered_information.blade_no_ward :: R71: Rin learned 2026-10-14 the Nightglass has no warding or healing effect when laid on a person; it only bites what it strikes
    locked_case_truths.hale_bloodline.discovered_information.haller_exam :: R42: Haller judged the Nightglass not forged, uniform, glass-dark, ~20 years old by the grip wear, and would not treat it, 2026-10-08
    locked_case_truths.hale_bloodline.discovered_information.haller_lead :: R24: Jo named Dutch Haller (blade treater, not a forger) and says no one she knows could make Rin's blade, 2026-10-07
    locked_case_truths.hale_bloodline.discovered_information.parent_letter :: R62: Rin read his parent's letter 2026-10-12 (signed only with a sigil like a closed eye crossed by a line): the parent was of the court below and left it; after Rin's birth they sealed the old way under the Red Line with their own mark; the mark holds while nobody takes from it, weakens if dug at; it knows the parent's blood and Rin's; if Rin calls up his power near the old stones or near the black glass that grows from them, those below feel the blood is alive and close, though not his name or face; walking right up to the seal wakes it regardless; the blade is made from what the parent was and won't break against them; the parent doesn't know if Rin could mend the mark
    locked_case_truths.hale_bloodline.evidence.independent_proof :: Ada's deposit box letters, Lantern LO-04 and the seal mark can establish the parentage even when the Surveyor never speaks to Rin
    locked_case_truths.hale_bloodline.evidence.letters :: Ada's deposit box
    locked_case_truths.hale_bloodline.evidence.recognition :: only sealer-line surge near exposed connected cinder glass within 50 metres or inside the old route, or an actual approach within 20 metres of the main seal, registers the line. No name, precise location or mandatory encounter follows.
    locked_case_truths.hale_bloodline.evidence.seal_reaction :: the seal answers Rin's blood
    locked_case_truths.hale_bloodline.state.absent_parent_status :: unknown
    locked_case_truths.hale_bloodline.state.future_power :: not predetermined
    locked_case_truths.hale_bloodline.trajectory :: dormant unless play opens a real channel; never revealed because of a level threshold
    locked_case_truths.old_seal.cause :: In 2004 a demon who had broken from the Cinder Court sealed the breach under the Red Spur and vanished. The seal carries its mark. The Surveyor wants the seal open and the sealer's line found.
    locked_case_truths.old_seal.discovered_information :: {}
    locked_case_truths.old_seal.discovered_information.ada_2004 :: R55: Ada witnessed the end of the 2004 sealing under the Red Line; describes the thing below as old and nearly out
    locked_case_truths.old_seal.discovered_information.haller_lore :: R41: Haller told Rin 2026-10-08: "ember glass" softens nearby steel edges, draws vermin and bigger things; old-trade talk says it sweats out of the walls at old bricked-up breaches where heat comes up from below
    locked_case_truths.old_seal.discovered_information.haller_saying :: R85: Haller 2026-10-19: raw fist-sized ember glass is straight out of a wall; old-trade saying "what you take from below, below comes looking for"; keep it cold, closed, away from people, never sold back
    locked_case_truths.old_seal.discovered_information.mara_2004_file :: R90: Mara told Rin 2026-10-22 she has an old 2004 file with a sealed part never opened for lack of physical proof; she is requesting it now
    locked_case_truths.old_seal.discovered_information.parent_letter :: R62: the seal holds while nobody takes from it; it weakens if dug at; its mark is the sigil on the letter
    locked_case_truths.old_seal.discovered_information.runner_seen :: R89: Rin saw on camera a small slag creature passing through the Southport grate at low water to meet the Choir courier, 2026-10-21
    locked_case_truths.old_seal.discovered_information.varga_lead :: R86: Mara named Teodor Varga, ironworker in Ironside Lane, who did city contract work in 2004 making iron fittings for a job under the Red Line; she'll ask him to see Rin
    locked_case_truths.old_seal.evidence.ada :: Ada was there in 2004 and keeps the parent's letters in a deposit box
    locked_case_truths.old_seal.evidence.containment_options :: work on the main seam requires access, documented alignment, glass/iron support and skills or qualified help; relieve pump loads or insert supports to arrest cyclic stress, reclose the bleed slit, shut down extraction, bargain for time or block physical approaches. Each option has practical cost and limits; successful repairs actually stop that cause rather than scheduling a new unavoidable breach.
    locked_case_truths.old_seal.evidence.lantern_case :: Lantern case LO-04 records a human-passing demon at the 2004 Red Spur incident; Mara can request it once she has physical proof
    locked_case_truths.old_seal.evidence.mercer_path :: Mercer pump and Southport outfall are an independent outer-gallery route. Grille marks, storm residue, actual pump workers and old municipal maintenance numbering provide evidence. The small bleed slit is a physical messenger path from the Court side, not permission to move larger forces.
    locked_case_truths.old_seal.evidence.seal_mark :: sigil responds to a sealer-line surge near unneutralized connected glass within 50 metres or inside the old connected route; approach within 20 metres of main seal itself also registers. This is not a citywide bloodline beacon.
    locked_case_truths.old_seal.evidence.site_physics :: the main 2004 patch divides outer spur galleries from the Lower Works. Old bleed-drain material has fractured after residue removal; its slit passes only lesser-size entities under suitable low-water flow. Door 7-B and Mercer/Southport enter outer galleries separately; repairing the main seam and drain can stop both the slow crack and the courier leak.
    locked_case_truths.old_seal.evidence.spur_warden :: the warden guards the seam and will not cross the seal line
    locked_case_truths.old_seal.evidence.surveyor :: the Surveyor's voice in the spur bargains and may reveal its intent or knowledge if a real channel opens
    locked_case_truths.old_seal.routes :: Find 2004 through Ada's letters, Lantern LO-04, site marks, surviving witness statements or Court bargaining; approach the compromised patch through Halden or the independent Mercer route. Closing either door alone never guarantees isolation; repair may be successful, fail or be refused.
    locked_case_truths.old_seal.state.bleed_slit :: passable only for small scouts at low-water windows; physically blockable and repairable
    locked_case_truths.old_seal.state.failure_modes :: material collapse from cumulative extraction and slower cyclic loading, or purposeful sabotage with actual means
    locked_case_truths.old_seal.state.main_arc_resolution_scope :: The Red Spur main arc may close when its final real undertaking decisively resolves access and the seal: stable restoration or isolation, a negotiated arrangement, actual breach and new control, informed withdrawal or a genuinely impossible objective. Neither defeating Surveyor nor a revelation is a mandatory win condition. These are closure possibilities, not automatic scenario termination.
    locked_case_truths.old_seal.state.main_seal :: holds against large Court entry while thinned and leaking lesser-sized bodies at the bleed drain
    locked_case_truths.red_line_case.cause :: Jonas Rusk extends blackout windows for Orin's cash so crews can carry cinder glass out of the sealed spur through door 7-B. Eli noticed, followed a van on Oct 4, took a shard, saw a demon on the far platform, was spotted, fell, and escaped injured. He hides in relay hut 3.
    locked_case_truths.red_line_case.discovered_information :: {}
    locked_case_truths.red_line_case.discovered_information.clean_window :: R56: Rin watched the booked window 00:30–01:30 Oct 11 run exactly to time with no vans or crates; every earlier window in Eli's notes ran 1–2 hours over
    locked_case_truths.red_line_case.discovered_information.eli_account :: R5: Eli told Rin 2026-10-06: extended windows, Merrow van into Halden Lane, door 7-B into the sealed spur, crates carried out, Jonas Rusk present, took a shard, chased, fell on service stairs, phone off; blurry photo of something on the far platform
    locked_case_truths.red_line_case.discovered_information.embankment_signs :: R2: Rin found cinderling tracks, burned rat, and hut 3 wedged from inside, with someone silent inside, 2026-10-06 20:45
    locked_case_truths.red_line_case.discovered_information.mercer_low_forecast :: R88: Eli's telemetry reading 2026-10-20: Mercer sump expected low ~03:00–05:00 Wed 21 Oct
    locked_case_truths.red_line_case.discovered_information.mercer_route_eli :: R85: Eli told Rin 2026-10-19 that the Red Spur's old drainage runs to the Mercer flood pump, with service stairs into old galleries once linked to the spur's outer galleries, and overflow to the Southport outfall
    locked_case_truths.red_line_case.discovered_information.next_window :: R50: Rin knows the next Ferris back-half isolation is booked night of Oct 10–11, 00:30–01:30, per Eli's roster app
    locked_case_truths.red_line_case.discovered_information.phone_location :: R1: Rin saw the locator via Nadia 2026-10-06 20:00; area only, not hut
    locked_case_truths.red_line_case.discovered_information.runner_footage :: R89: Rin's Southport camera 04:06–04:13 Wed 21 Oct: the courier waited at the outfall; a cat-sized slag creature with glowing cracks came out through the grate at low water, gave him a tiny red glinting chip, took a folded paper message wrapped round something, and went back through the grate
    locked_case_truths.red_line_case.discovered_information.rusk_footage :: R62: Rin's camera filmed Rusk at the Halden gate 16:20 Oct 11 in a white Merrow pickup, checking the service door padlock; face clear in two frames, plate readable; the 00:30–01:30 window empty; clips saved in three places
    locked_case_truths.red_line_case.discovered_information.spur_map :: R1: Rin has Eli's map with RED SPUR (CLOSED) circled
    locked_case_truths.red_line_case.discovered_information.vermin_mesh :: R90: Mara is asking Transit Safety to fit fine vermin mesh on the Southport outfall grate and the Mercer sump screen, 2026-10-22
    locked_case_truths.red_line_case.evidence.apartment_papers :: work orders with Eli's real end times and "WHO EXTENDS? NOT US." in his flat
    locked_case_truths.red_line_case.evidence.cinderling :: a lesser demon prowling the embankment at night is drawn by the shard; anyone who knows the signs can follow it to hut 3
    locked_case_truths.red_line_case.evidence.crew_watch :: Dale and Vic sit in a Merrow van outside Eli's flat some evenings; following them or leaning on Vic leads to Rusk and Halden Lane
    locked_case_truths.red_line_case.evidence.ferris_window :: scheduled night traffic and missing authorizations identify 7-B as a physical destination, regardless of whether Eli can be rescued
    locked_case_truths.red_line_case.evidence.mercer_worker :: pump operator's shift notices note unusual hot grit and a changed low-water flow; the operator has ordinary local knowledge, not secret knowledge of Orin or the Court
    locked_case_truths.red_line_case.evidence.phone_location :: family-plan location history shows Eli's phone last on the Canal Street embankment at 06:40 Oct 5 (Nadia's account)
    locked_case_truths.red_line_case.evidence.shared_records :: Transit retains original gate video and shift sign-outs outside Rusk's edit access; publicly indexed outage dates allow licensed PI comparison without Mara or Nadia's cooperation
    locked_case_truths.red_line_case.evidence.southport_scour :: at Southport outfall, cinder-coloured grit and a loosened old grille are observable; a maintenance stencil connects that culvert to Mercer without obtaining a private camera record
    locked_case_truths.red_line_case.evidence.stairs :: blood and a torn sleeve on the Halden Lane service stairs; the gate camera recorded the chase (Transit footage, 30-day retention)
    locked_case_truths.red_line_case.evidence.tomas :: knows about the windows and that Eli goes to the embankment relay huts to think
    locked_case_truths.red_line_case.evidence.van :: the plate in Eli's photos is a Merrow van signed out to Rusk's crew
    locked_case_truths.red_line_case.routes :: Eli and his phone/Tomas/field marks lead to 7-B. Gallo stock, a cell courier or Suds & Spin cache identifies the Old Exchange supply. Southport runoff, Mercer worker reports and the damaged grille reveal a second physical way into the outer spur without Halden permission. The people, places and sites remain independent; any one can be lost.
    locked_case_truths.red_line_case.state.windows :: 2–3 nights a week
    npcs.ada_hale.belongs :: []
    npcs.ada_hale.capability.overall_level :: 3
    npcs.ada_hale.character :: warm, sharp, nags as a love language; changes the subject when Rin asks about the parent
    npcs.ada_hale.discovered_information :: {}
    npcs.ada_hale.drives.fears :: ["the Court finding Rin"]
    npcs.ada_hale.drives.values :: ["family", "promises kept"]
    npcs.ada_hale.drives.wants :: ["Rin safe", "Rin happy"]
    npcs.ada_hale.gender :: woman
    npcs.ada_hale.job :: retired, Wexley; Rin's guardian
    npcs.ada_hale.knowledge.channels :: ["old Lantern contacts", "Rin"]
    npcs.ada_hale.knowledge.facts.nightglass_origin :: R17: the Nightglass Blade was left with infant Rin by the sealer parent in 2004; Ada kept it and gave it to Rin at sixteen saying only that it came from someone who'd want Rin to have it; she does not know who forged it
    npcs.ada_hale.knowledge.facts.rin_case :: R55: Rin told her 2026-10-10 everything: Eli, the cinderlings, the charms and the Choir, Haller's ember glass, the city contract, door 7-B and the sealed Red Spur, a figure on the far platform, the man calling himself Orin, and his plan to watch Halden tonight
    npcs.ada_hale.knowledge.facts.rin_glass_call :: R19: Rin described warm black glass with a red core that draws small demons, 2026-10-07 afternoon; would not say where it came from
    npcs.ada_hale.knowledge.facts.rin_promise :: R63: Rin promised 2026-10-12 not to call up his power near the stones
    npcs.ada_hale.knowledge.facts.the_2004 :: she was there when Rin's parent sealed the Red Spur and promised to raise Rin away from it; a bank deposit box holds the parent's letters
    npcs.ada_hale.name :: Ada Hale
    npcs.ada_hale.relationships.rin_hale.attitude :: R55: loves Rin; frightened; relieved to have told him
    npcs.ada_hale.relationships.rin_hale.believes_identity :: null
    npcs.ada_hale.relationships.rin_hale.credit :: []
    npcs.ada_hale.relationships.rin_hale.grievance :: []
    npcs.ada_hale.relationships.rin_hale.tie :: guardian since infancy
    npcs.ada_hale.state.due :: R89: 2026-10-25 18:00 Sunday call
    npcs.ada_hale.state.plan :: R63: calls with Rin Wednesday and Sunday; ready to come back if he needs her
    npcs.ada_hale.state.position :: R63: her flat in Wexley, from 15:00 Oct 12
    npcs.ada_hale.state.status :: R89: Wednesday call 18:00 Oct 21 on time; went quiet at "2004"; told Rin to be polite to Varga — men like that don't talk twice
    npcs.agnieszka_wolak :: R78: {name: Agnieszka Wolak, job: lets four rooms above a closed chandlery on the wharf, cash by the week, no ID, belongs: [], gender: woman, character: sixty-five, thin, smokes at the window; temper roll 13 (ordinary), state: {position: wharf rooms above the old chandlery, status: holding her back room for Rin for a month, paid $150 cash 2026-10-16, plan: keep the room; no questions, due: 2026-11-16 room hold ends}, relationships: {rin_hale: {tie: landlady from his courier days, attitude: neutral, mildly fond, credit: [never dripped on her stairs], grievance: [], believes_identity: the polite courier boy}}, capability: {overall_level: 1}}
    npcs.ashfall_general_er :: R73: {name: Ashfall General ER staff, job: emergency department, belongs: [], gender: mixed, character: busy, professional, state: {position: ashfall_general, status: treating Imran; asked about the object, noted Rin's details, plan: treat; may ask the city about the object, due: ordinary}, capability: {overall_level: 2}}
    npcs.bellamy_doctor :: R59: {name: the Bellamy Street doctor (unnamed), job: GP at the Bellamy Street walk-in clinic, open Sundays till 14:00, belongs: [], gender: man, character: older, tired, cardigan; thorough; asks no questions he doesn't need; temper roll 14 (ordinary), state: {position: bellamy_clinic, status: examined Lucy Warren 10:40 Oct 11, plan: written report with blood results for Rin and Lucy, due: 2026-10-14 bloods back; Lucy's follow-up}, relationships: {rin_hale: {tie: doctor Rin uses, attitude: neutral, trusting, credit: [], grievance: [], believes_identity: PI who brings in odd cases}}, knowledge: {facts: {warren_exam: low core temperature, low BP, fast pulse, mild dehydration, recent weight loss, a healing walnut-sized thermal injury below the throat consistent with long contact with something warm}}, capability: {overall_level: 3}}
    npcs.bellamy_doctor.relationships.rin_hale.attitude :: R72: neutral turning wary; suspicious
    npcs.bellamy_doctor.state.due :: R66: 2026-10-28 Lucy's follow-up
    npcs.bellamy_doctor.state.status :: R72: refused to open at midnight 23:35 Oct 14 (NO, AND); told Rin to take Imran to Ashfall General; now suspicious of what Rin is mixed up in
    npcs.brannock_heavy :: R79: {name: shaven-headed man (unnamed), job: Brannock/Choir muscle; collected Gallo's stones and notes, belongs: [ash_choir], gender: man, character: short, wide, shaven head, leather jacket, swaggering; kicks gates, jabs people; temper roll 15 (difficult — a bully), state: {position: in the grey Nissan toward the ring road, 23:25 Oct 16, status: took Gallo's stones and batch notes, plan: deliver them to Unit 9 or M, due: 2026-10-17 00:00}, capability: {overall_level: 4}}
    npcs.brannock_heavy.state.position :: R80: inside Unit 9, Exchange Yard, from 23:50 Oct 16
    npcs.brannock_heavy.state.status :: R80: handed the bag and notebook to the older man at Unit 9; laughed; stayed inside
    npcs.choir_contact_m :: R28: {name: M (Choir), job: Ash Choir cell stock contact; arranges holds and pickups by text, belongs: [ash_choir], gender: unknown, character: terse, unknown in person, state: {position: unknown, status: told Warren 2026-10-07 11:51 to stay put and be at the back door at 22:00, plan: send the courier to Suds & Spin 2026-10-08 22:00 to talk to Warren about the lost stock; reports to the cell and Orin's people, due: 2026-10-08 22:00}, knowledge: {facts: {loss: Warren says Pike's hunter Rin Hale of Hale Workshop took the box}}, capability: {overall_level: unknown}}
    npcs.choir_contact_m.state.due :: R57: next stock movement through the Mercer/Southport route at low water
    npcs.choir_contact_m.state.plan :: R57: drop Suds & Spin as a holding point; use other holders; report to Orin's people
    npcs.choir_contact_m.state.status :: R57: cut Warren loose 07:02 Oct 11 (YES): no more boxes, don't contact, don't talk, keep the $200, "good luck"
    npcs.choir_courier :: R28: {name: hooded courier, job: picks up and drops off for M, belongs: [ash_choir], gender: man, character: big coat, hood always up; unknown, state: {position: unknown, plan: come to the Suds & Spin alley back door 2026-10-08 22:00 for M, due: 2026-10-08 22:00}, capability: {overall_level: unknown}}
    npcs.choir_courier.capability.description :: R40: forties, broad face, flattened nose, scar through one eyebrow
    npcs.choir_courier.capability.overall_level :: R39: 3
    npcs.choir_courier.character :: R39: big, slow, heavy-shouldered, long dark hooded parka with fur trim, stubble; flat local voice; temper roll 6 (ordinary)
    npcs.choir_courier.state.due :: R79: 2026-10-17 00:00 delivers to Unit 9 or M
    npcs.choir_courier.state.plan :: R40: report to M tonight: Rin Hale present at the pickup, refuses, invites an offer; Warren with Rin
    npcs.choir_courier.state.position :: R80: inside Unit 9, Exchange Yard, Old Exchange, from 23:50 Oct 16
    npcs.choir_courier.state.status :: R89: met the Surveyor's runner at the Southport outfall 04:06–04:13 Wed 21 Oct as Orin's watcher; received a red glass chip; passed back Orin's folded message; filmed by Rin's camera
    npcs.choir_courier.state.vehicle :: R65: dark grey Nissan KT 72 VRN, registered keeper Brannock Freight Services Ltd, Unit 9, Exchange Yard, Old Exchange
    npcs.court_runner.belongs :: ["cinder_court"]
    npcs.court_runner.capability.overall_level :: 3
    npcs.court_runner.capability.skills.mobility :: T2
    npcs.court_runner.capability.skills.stealth :: T1
    npcs.court_runner.character :: quick, cautious, curious about heated glass, will retreat from superior force
    npcs.court_runner.discovered_information :: {}
    npcs.court_runner.drives.fears :: ["pump turbines", "daylight witnesses", "hunters"]
    npcs.court_runner.drives.values :: ["binding orders", "survival"]
    npcs.court_runner.drives.wants :: ["complete Surveyor's delivery", "return with reconnaissance"]
    npcs.court_runner.gender :: none
    npcs.court_runner.job :: small bound Cinder Court messenger serving the Surveyor
    npcs.court_runner.knowledge.channels :: ["Surveyor", "physical marks and sound through the drain", "Orin's marked contact points"]
    npcs.court_runner.knowledge.facts.employer :: Surveyor's status token is for Orin or his designated contacts, not for Rin
    npcs.court_runner.knowledge.facts.exit :: small slit at the main seal's side drain, through Mercer outer sump to Southport outfall; cannot use 7-B or teleport
    npcs.court_runner.name :: Slag Runner
    npcs.court_runner.relationships :: {}
    npcs.court_runner.state.carries :: one marked glass chip used to verify a delivery; no general power to pass closed wards
    npcs.court_runner.state.due :: R89: next low water after it reports
    npcs.court_runner.state.plan :: R89: carry Orin's message back to the Surveyor; return at the next low water
    npcs.court_runner.state.position :: lower_works, near the damaged bleed-drain
    npcs.court_runner.state.status :: R89: 04:11 Wed 21 Oct passed the bleed-drain slit at low water to the Southport outfall; handed Orin's watcher (the courier) a marked red glass chip; took back a folded paper message wrapped round something; returned through the grate 04:13
    npcs.dale.belongs :: ["merrow_utility_solutions"]
    npcs.dale.capability.overall_level :: 2
    npcs.dale.character :: loud, sure of himself, likes the cash and the swagger
    npcs.dale.discovered_information :: {}
    npcs.dale.drives.fears :: ["police"]
    npcs.dale.drives.values :: ["money"]
    npcs.dale.drives.wants :: ["cash"]
    npcs.dale.gender :: man
    npcs.dale.job :: Merrow night labourer on Rusk's side payroll
    npcs.dale.knowledge.channels :: ["Rusk"]
    npcs.dale.knowledge.facts.crates :: they carry sealed crates out of 7-B to a van; he can identify 7-B
    npcs.dale.name :: R59: Dale Brennan
    npcs.dale.relationships.jonas_rusk.attitude :: loyal while paid
    npcs.dale.relationships.jonas_rusk.believes_identity :: null
    npcs.dale.relationships.jonas_rusk.credit :: []
    npcs.dale.relationships.jonas_rusk.grievance :: []
    npcs.dale.relationships.jonas_rusk.tie :: boss on the side payroll
    npcs.dale.relationships.vic.attitude :: thinks he's soft
    npcs.dale.relationships.vic.believes_identity :: null
    npcs.dale.relationships.vic.credit :: []
    npcs.dale.relationships.vic.grievance :: []
    npcs.dale.relationships.vic.tie :: crewmate
    npcs.dale.state.due :: R53: when Rusk calls him back to work
    npcs.dale.state.plan :: do what Rusk pays for and keep the side job concealed; during an inspection follow Rusk's public story unless contradictory evidence or personal risk breaks it
    npcs.dale.state.position :: Ferris Yard on window nights; Lowfield some evenings
    npcs.dale.state.status :: R53: told by Rusk 21:00 Oct 9: no runs for two weeks
    npcs.dutch_haller :: R24: {name: Dutch Haller, job: knife-grinder at a stall in the Fishmarket Arcade by the wharf; at night treats steel for a few hunters and sells occult odds and ends, belongs: [], gender: man, character: unknown (not yet met), state: {position: Fishmarket Arcade stall, status: working his trade, plan: ordinary trade; night work only for vouched clients, due: ordinary routine}, knowledge: {facts: {}}, capability: {overall_level: unknown until met}}
    npcs.dutch_haller.capability.overall_level :: R34: 3
    npcs.dutch_haller.character :: R34: big, slow, unhurried, burn-scarred hands; cautious; temper roll 5 (ordinary)
    npcs.dutch_haller.knowledge.facts.ember_glass :: R41: calls it "ember glass"; ~2011 a hunter brought him a thumbnail chip to set in a pommel; in three days nearby steel edges went soft as if over-tempered, rats got past his salt, something bigger tried his back door on the third night; he threw it off the pier; old trade talk says it grows where heat comes up from below at old breaches, places bricked shut long ago, sweating out of the walls; he doesn't know if that's true
    npcs.dutch_haller.knowledge.facts.nightglass_seen :: R42: Rin showed him the Nightglass Blade 2026-10-08; he could not identify its make; wants to meet whoever made it
    npcs.dutch_haller.knowledge.facts.raw_glass :: R85: Rin described the seized raw crate to him 2026-10-19
    npcs.dutch_haller.relationships.rin_hale :: R34: {tie: hunter asking trade talk, attitude: neutral, wary, credit: [], grievance: [], believes_identity: hunter Kestrel knows}
    npcs.dutch_haller.relationships.rin_hale.attitude :: R43: neutral; a paying customer
    npcs.dutch_haller.state.due :: R62: any night after 21:00 at the back loading door
    npcs.dutch_haller.state.plan :: R44: cure and edge two treated 4-inch blades for Rin; ordinary trade by day
    npcs.dutch_haller.state.status :: R43: honed the nick out of the Nightglass Blade 23:30 Oct 8 for $20; quoted Rin: treated 4-inch fixed blade $300 (half up front, three-day cure, ready Sunday 2026-10-11); untreated legal lock-knife $45 tonight; second treated blade another $300 and three days
    npcs.eli_voss.belongs :: ["ashfall_transit_authority"]
    npcs.eli_voss.capability.overall_level :: 2
    npcs.eli_voss.capability.skills.observation :: T1
    npcs.eli_voss.capability.skills.transit_maintenance :: T2
    npcs.eli_voss.character :: earnest train nerd, brave in a badly planned way, talks fast when scared, can't lie to his sister
    npcs.eli_voss.discovered_information :: {}
    npcs.eli_voss.drives.fears :: ["the crew", "Nadia searching alone", "the thing on the platform"]
    npcs.eli_voss.drives.values :: ["family", "doing the job right"]
    npcs.eli_voss.drives.wants :: ["stay alive", "get the proof to someone who acts", "keep Nadia out of it"]
    npcs.eli_voss.gender :: man
    npcs.eli_voss.job :: transit maintenance technician
    npcs.eli_voss.knowledge.channels :: ["work logs", "direct observation", "Tomas"]
    npcs.eli_voss.knowledge.facts.crew :: Oct 4 he followed a Merrow van into Halden Lane, saw Jonas Rusk and two men carry crates out of 7-B, took a shard from an open crate, was spotted, ran, fell on the service stairs.
    npcs.eli_voss.knowledge.facts.door_7b :: Service door 7-B into the sealed spur is in use and on no work order.
    npcs.eli_voss.knowledge.facts.false_windows :: Seven blackout windows around the Red Spur ran 1–2 hours past sign-out; nobody on Transit orders extended them.
    npcs.eli_voss.knowledge.facts.figure :: Through 7-B he saw something not human crossing the far platform.
    npcs.eli_voss.knowledge.facts.mercer_route :: R85: told Rin 2026-10-19: the old spur drained south to the Mercer flood pump (still working); service stairs from the pump room down into old drainage galleries that once connected to the spur's outer galleries; overflow runs by culvert to the Southport outfall on the canal; often flooded, dangerous pumps; never been down
    npcs.eli_voss.knowledge.facts.next_window :: R50: Transit roster shows the Ferris back-half isolation booked Sat 10 Oct 00:30–01:30 (night of Oct 10–11); Eli expects the lights off at 00:30 and the vans after
    npcs.eli_voss.knowledge.facts.photos :: His phone holds photos of the crates, the van plate, and a blurred shape in the spur.
    npcs.eli_voss.knowledge.facts.rin_warning :: R87: Rin told him 2026-10-20 someone may be using the Mercer–Southport route and a camera is on it; keep away
    npcs.eli_voss.knowledge.facts.shard_draws :: R5: Rin told him the shard is what draws the creatures
    npcs.eli_voss.knowledge.facts.telemetry :: R87: the yard office has a live Transit telemetry screen showing every pump station's sump level, including Mercer; he looks at it every morning
    npcs.eli_voss.knowledge.facts.yard_gossip :: R76: via Tomas 2026-10-15: Halden locked down after hours; Merrow's night crew removed from the Halden building by Transit Safety Oct 14; talk of an audit; Rusk off "sick"; Merrow staff tense
    npcs.eli_voss.name :: Eli Voss
    npcs.eli_voss.relationships.nadia_voss.attitude :: adores her, dreads her lecture
    npcs.eli_voss.relationships.nadia_voss.believes_identity :: null
    npcs.eli_voss.relationships.nadia_voss.credit :: []
    npcs.eli_voss.relationships.nadia_voss.grievance :: []
    npcs.eli_voss.relationships.nadia_voss.tie :: younger brother
    npcs.eli_voss.relationships.rin_hale :: R5: {tie: PI hired by Nadia, attitude: relieved, still wary, credit: [killed the creature at his door], grievance: [], believes_identity: PI sent by Nadia}
    npcs.eli_voss.relationships.rin_hale.attitude :: R77: grateful, loyal; would help again
    npcs.eli_voss.relationships.rin_hale.credit :: R8: [found him and brought him safe, 2026-10-06]
    npcs.eli_voss.relationships.tomas_reyes.attitude :: trusting
    npcs.eli_voss.relationships.tomas_reyes.believes_identity :: null
    npcs.eli_voss.relationships.tomas_reyes.credit :: []
    npcs.eli_voss.relationships.tomas_reyes.grievance :: []
    npcs.eli_voss.relationships.tomas_reyes.tie :: coworker and best friend
    npcs.eli_voss.state.carries :: R7: phone (off); no longer the shard
    npcs.eli_voss.state.due :: R88: 2026-10-20 12:30 next sump check; daily
    npcs.eli_voss.state.hp :: R10: 12 — full night's rest
    npcs.eli_voss.state.plan :: R88: check the Transit telemetry board each morning and at lunch; text Rin when Mercer's sump runs low; stay at his desk
    npcs.eli_voss.state.position :: R19: Nadia's flat, Lowfield, from ~20:00 Oct 7
    npcs.eli_voss.state.routines.telemetry :: R88: Eli texts Rin the Mercer sump level each morning and at lunch, from his desk
    npcs.eli_voss.state.status :: R87: Rin told him 07:05 Oct 20 someone may be using the Mercer–Southport drainage, that a camera is watching it, and not to go near it or be curious; Eli promised
    npcs.eli_voss.state.supplies :: water and vending snacks for about 4 more days
    npcs.embankment_cinderling :: R2: {name: cinderling (Canal embankment), job: lesser demon scavenger, belongs: [], gender: none, character: hungry, cautious, fixated on the shard's heat, state: {position: weeds ~20 m from hut 3, status: watching Rin, hp: 6, plan: keep distance while Rin is there; return to scratching at hut 3 once Rin leaves; withdraw if hurt, due: when Rin leaves the embankment or closes within a few metres}, drives: {wants: [the shard, warmth, food], fears: [strong light, superior force]}, capability: {overall_level: 2, size: small}}
    npcs.embankment_cinderling.state.plan :: R3: no longer holds — dead
    npcs.embankment_cinderling.state.status :: R3: killed by Rin 2026-10-06 20:47; body cooled to inert slag on the embankment
    npcs.gallo_pawnbroker.belongs :: ["ash_choir"]
    npcs.gallo_pawnbroker.capability.overall_level :: 2
    npcs.gallo_pawnbroker.character :: chatty, smells money, scared of Orin, kinder to regulars than he admits
    npcs.gallo_pawnbroker.discovered_information :: {}
    npcs.gallo_pawnbroker.drives.fears :: ["Orin", "the police"]
    npcs.gallo_pawnbroker.drives.values :: ["his shop"]
    npcs.gallo_pawnbroker.drives.wants :: ["the margin"]
    npcs.gallo_pawnbroker.gender :: man
    npcs.gallo_pawnbroker.job :: owner, Gallo Pawn & Loan, Tanner St, Lowfield
    npcs.gallo_pawnbroker.knowledge.channels :: ["customers", "Orin's courier"]
    npcs.gallo_pawnbroker.knowledge.facts.inventory :: A partial batch tally and courier waybill show supply via Old Exchange but not every sale; three stones are in his present under-counter stock. He remembers selling one to Imran, a regular cabbie, about five weeks ago.
    npcs.gallo_pawnbroker.knowledge.facts.jo_questions :: a competing hunter named Jo has asked about rare charms, not their source or actual purpose.
    npcs.gallo_pawnbroker.knowledge.facts.stones :: he does not know what the stones are; he knows customers come back for more
    npcs.gallo_pawnbroker.name :: Sal Gallo
    npcs.gallo_pawnbroker.relationships.orin_sable.attitude :: afraid
    npcs.gallo_pawnbroker.relationships.orin_sable.believes_identity :: null
    npcs.gallo_pawnbroker.relationships.orin_sable.credit :: []
    npcs.gallo_pawnbroker.relationships.orin_sable.grievance :: []
    npcs.gallo_pawnbroker.relationships.orin_sable.tie :: supplier
    npcs.gallo_pawnbroker.state.due :: R79: 2026-10-19 if a warrant comes; immediately if contacted
    npcs.gallo_pawnbroker.state.plan :: R79: keep his head down; deny everything; terrified of both the Choir and Trading Standards
    npcs.gallo_pawnbroker.state.position :: gallo_pawn
    npcs.gallo_pawnbroker.state.status :: R79: Trading Standards inspected his shop 10:00 Oct 16, found nothing, took ledger copies, served a notice; called the courier in a panic; at 23:20 the courier and a shaven-headed man came to his house, took the bag of stones and his batch notes and papers; the shaven-headed man jabbed him in the chest and threatened him; Gallo went dark
    npcs.imran_dalen.belongs :: []
    npcs.imran_dalen.capability.overall_level :: 1
    npcs.imran_dalen.character :: sociable, stubbornly optimistic, works late to meet his car payments
    npcs.imran_dalen.discovered_information :: {}
    npcs.imran_dalen.drives.fears :: ["losing his licence", "frightening his family"]
    npcs.imran_dalen.drives.values :: ["responsibility"]
    npcs.imran_dalen.drives.wants :: ["keep his income", "feel normal again"]
    npcs.imran_dalen.gender :: man
    npcs.imran_dalen.job :: Lowfield taxi driver
    npcs.imran_dalen.knowledge.channels :: ["taxi dispatch", "passengers", "family"]
    npcs.imran_dalen.knowledge.facts.stone :: his charm came from Gallo and seemed lucky at first; he does not know its source or mechanism
    npcs.imran_dalen.name :: Imran Dalen
    npcs.imran_dalen.state.carries :: R70: no stone
    npcs.imran_dalen.state.due :: R85: discharge review later this week
    npcs.imran_dalen.state.plan :: R70: none — incapacitated by withdrawal
    npcs.imran_dalen.state.position :: R85: Ashfall General, general ward
    npcs.imran_dalen.state.status :: R85: moved out of high-dependency to a normal ward 2026-10-19 morning (YES); knew the date, asked for tea and his cab; still talks in his sleep
    npcs.jo_kestrel.belongs :: []
    npcs.jo_kestrel.capability.overall_level :: 4
    npcs.jo_kestrel.capability.skills.close_combat :: T2
    npcs.jo_kestrel.capability.skills.firearms :: T2
    npcs.jo_kestrel.capability.skills.occult_lore :: T2
    npcs.jo_kestrel.character :: precise, sardonic, prepared for everything; carries too many tools and is right to; competitive about money, not about people
    npcs.jo_kestrel.discovered_information :: {}
    npcs.jo_kestrel.drives.fears :: ["debt", "a job she can't finish"]
    npcs.jo_kestrel.drives.values :: ["professionalism", "preparation"]
    npcs.jo_kestrel.drives.wants :: ["steady paying work", "to be the hunter people call first"]
    npcs.jo_kestrel.gender :: woman
    npcs.jo_kestrel.job :: independent hunter, human
    npcs.jo_kestrel.knowledge.channels :: ["Pike", "other hunters", "police scanner"]
    npcs.jo_kestrel.knowledge.facts.charms :: a pawnshop in Lowfield sells luck charms that make her detector click
    npcs.jo_kestrel.knowledge.facts.choir_thread :: R33: Rin sent her 2026-10-08 photos of the M (Choir) thread: paid holding, "keep one for yourself, good luck charm", pickup Oct 8 22:00 back door, Warren naming Rin; holder sick after wearing one
    npcs.jo_kestrel.knowledge.facts.rin_blade :: R24: has seen Rin's blade in use; knows no maker who could make it; wants to know if Rin finds out
    npcs.jo_kestrel.knowledge.facts.rin_claims :: R33: Rin admitted the receipt was a lie 2026-10-08; the nest claim stands
    npcs.jo_kestrel.knowledge.facts.rivalry :: Rin once completed the job she had been working; she also owes Rin for an older rescue.
    npcs.jo_kestrel.knowledge.facts.uninformed :: She does not know Orin's aim, the seal, Rin's parentage or that a future cleanup job would protect a dangerous scheme.
    npcs.jo_kestrel.name :: Jo Kestrel
    npcs.jo_kestrel.relationships.orin_sable :: R19: {tie: client through a hunting-work contact (did not meet him), attitude: businesslike, credit: [paid half up front], grievance: [], believes_identity: a dealer recovering his client's antiques}
    npcs.jo_kestrel.relationships.orin_sable.attitude :: R33: done with him; feels used
    npcs.jo_kestrel.relationships.orin_sable.grievance :: R23: [story about "stored antiques" looks false to her, 2026-10-07]
    npcs.jo_kestrel.relationships.rin_hale.attitude :: R61: wary respect warming toward friendly; paid and treated straight
    npcs.jo_kestrel.relationships.rin_hale.believes_identity :: unusually tough human hunter; suspects more
    npcs.jo_kestrel.relationships.rin_hale.credit :: R40: [Rin pulled her out of a flooded culvert two years ago; warned her off a dirty client with real evidence, 2026-10-08]
    npcs.jo_kestrel.relationships.rin_hale.grievance :: R40: [Rin took and finished a job she had spent a week on last spring, and got paid for it; lied to her face about a receipt, admitted it 2026-10-08]
    npcs.jo_kestrel.relationships.rin_hale.tie :: competitor
    npcs.jo_kestrel.state.due :: R75: none pending; on Rin's contact
    npcs.jo_kestrel.state.plan :: R46: keep finding out who used her; $200 still owed by Rin
    npcs.jo_kestrel.state.position :: R61: behind the shut tyre shop off Ferris Road, 21:06 Oct 11, holding Rin's camera
    npcs.jo_kestrel.state.status :: R75: sent Mara a three-page written statement 10:40 Oct 15: Oct 9 Gallo visit, detector model and readings behind the counter, what Gallo said, plus the four alley photos and a detector graph; no interviews
    npcs.jonas_rusk.belongs :: ["merrow_utility_solutions"]
    npcs.jonas_rusk.capability.overall_level :: 3
    npcs.jonas_rusk.capability.skills.administration :: T2
    npcs.jonas_rusk.capability.skills.deception :: T1
    npcs.jonas_rusk.character :: neat, tired, polite on the phone and sweating off it; tells himself it's only paperwork
    npcs.jonas_rusk.discovered_information :: {}
    npcs.jonas_rusk.drives.fears :: ["Merrow audit", "police", "Orin", "what is below"]
    npcs.jonas_rusk.drives.values :: ["self-preservation"]
    npcs.jonas_rusk.drives.wants :: ["the money", "to get out clean"]
    npcs.jonas_rusk.gender :: man
    npcs.jonas_rusk.job :: Merrow night operations supervisor, Red Line contract
    npcs.jonas_rusk.knowledge.channels :: ["work orders", "his crew", "Orin's phone"]
    npcs.jonas_rusk.knowledge.facts.eli_seen :: Eli saw the crates on Oct 4 and got away; Rusk does not know where he is.
    npcs.jonas_rusk.knowledge.facts.risk_request :: city risk management has asked for Ferris outage explanations; Rusk does not know the Lantern Office exists or who is reviewing it.
    npcs.jonas_rusk.knowledge.facts.windows :: He extends blackout windows so Orin's people can carry crates out through 7-B.
    npcs.jonas_rusk.name :: Jonas Rusk
    npcs.jonas_rusk.relationships.mara_quill.attitude :: guarded, publicly cooperative
    npcs.jonas_rusk.relationships.mara_quill.believes_identity :: ordinary municipal analyst, not aware of Lantern
    npcs.jonas_rusk.relationships.mara_quill.credit :: []
    npcs.jonas_rusk.relationships.mara_quill.grievance :: []
    npcs.jonas_rusk.relationships.mara_quill.tie :: city risk officer requesting routine paperwork
    npcs.jonas_rusk.relationships.orin_sable.attitude :: afraid of him
    npcs.jonas_rusk.relationships.orin_sable.believes_identity :: dealer in old salvage with rough friends
    npcs.jonas_rusk.relationships.orin_sable.credit :: []
    npcs.jonas_rusk.relationships.orin_sable.grievance :: []
    npcs.jonas_rusk.relationships.orin_sable.tie :: paying client
    npcs.jonas_rusk.state.due :: R74: 2026-10-19 rescheduled compliance meeting; immediately on police contact or Orin's call
    npcs.jonas_rusk.state.plan :: R74: stall compliance with sickness and "clerical error"; keep Orin's name out of it; may fold later if the audit and danger outweigh the pay
    npcs.jonas_rusk.state.position :: Merrow Canal Street field office, nights
    npcs.jonas_rusk.state.status :: R74: Merrow after-hours access to Halden suspended by Transit Safety 16:00 Oct 14; Merrow compliance has the two sets of sheets; phoned in sick 08:00 Oct 15 to dodge the compliance meeting (NO, BUT — stalling, not folding); told Orin that Halden is shut
    npcs.kiosk_owner :: R20: {name: kiosk owner (Ferris Yard corner, unnamed), job: runs the night coffee kiosk at Ferris Yard, belongs: [], gender: man, character: older, chatty when bored, crossword habit; temper roll 9 (ordinary), state: {position: night kiosk, Ferris Yard corner, status: on his night shift, plan: run the kiosk till morning, due: ordinary routine}, relationships: {rin_hale: {tie: customer, attitude: neutral, friendly, credit: [], grievance: [], believes_identity: contractor doing signal checks}}, knowledge: {facts: {vans: Merrow vans come down Halden Lane around 01:00–02:00 on nights the back half of the yard goes dark; 2–3 nights a week lately; Transit staff complain about lockouts for "Merrow works", guard: Bernie, night security, walks the fence about hourly and buys coffee around midnight}}, capability: {overall_level: 1}}
    npcs.l_warren.belongs :: []
    npcs.l_warren.capability.overall_level :: 1
    npcs.l_warren.character :: wary, opportunistic and unusually attentive to noises beneath the machines
    npcs.l_warren.discovered_information :: {}
    npcs.l_warren.drives.fears :: ["the boiler-basement creature", "loss of work", "angry cell courier"]
    npcs.l_warren.drives.values :: ["survival", "getting paid"]
    npcs.l_warren.drives.wants :: ["cash for overdue rent", "stay out of Orin's trouble"]
    npcs.l_warren.gender :: R59: woman
    npcs.l_warren.job :: part-time Suds & Spin attendant and occasional Ash Choir stock holder
    npcs.l_warren.knowledge.channels :: ["laundromat shifts", "Ash Choir stock contact", "local neighbours"]
    npcs.l_warren.knowledge.facts.cache :: three cinder-glass charms arrived in a reused Old Exchange carton via a cell contact; Warren wears one of them and two remain in the box; Warren does not know the seal or origin
    npcs.l_warren.knowledge.facts.creature :: the scorching and noises started after the stock was stored near the boiler
    npcs.l_warren.name :: R59: Lucy Warren
    npcs.l_warren.relationships :: {}
    npcs.l_warren.relationships.rin_hale :: R27: {tie: the hunter who took the box, attitude: scared, apologetic, credit: [killed the basement creature], grievance: [took the stock Warren was paid to hold], believes_identity: Pike's hunter, Rin Hale}
    npcs.l_warren.relationships.rin_hale.attitude :: R28: scared, dependent, apologetic
    npcs.l_warren.relationships.rin_hale.credit :: R58: [killed the basement creature; came to the 22:00 pickup; checked on Warren's health]
    npcs.l_warren.state.carries :: R28: phone with the M (Choir) thread; no charm
    npcs.l_warren.state.due :: R66: 2026-10-28 follow-up; immediately on contact from the Choir
    npcs.l_warren.state.plan :: R59: warmth, fluids, food, sleep; results Wednesday at the clinic
    npcs.l_warren.state.position :: R41: going home from Suds & Spin 22:20 Oct 8
    npcs.l_warren.state.status :: R85: texted Rin Oct 19: appetite back, no dreams, still cold hands; Rosa gave her shifts back
    npcs.laundromat_cinderling :: R12: {name: cinderling (Suds & Spin), job: lesser demon scavenger, belongs: [], gender: none, character: territorial at its nest, drawn by the cache's heat, state: {position: storage recess, Suds & Spin basement, status: awake, facing Rin at the recess mouth, hp: 7, plan: hold the nest beside the warm box; drive off what comes close; flee only if badly hurt with a clear way out, due: immediately if Rin closes or attacks; else stays}, drives: {wants: [the cache's heat, food], fears: [strong light, superior force]}, capability: {overall_level: 3, size: small}}
    npcs.laundromat_cinderling.state.plan :: R13: no longer holds — dead
    npcs.laundromat_cinderling.state.status :: R13: killed by Rin 2026-10-07 09:56 in the Suds & Spin basement; cooled to inert slag
    npcs.lina_dalen.belongs :: []
    npcs.lina_dalen.capability.overall_level :: 1
    npcs.lina_dalen.character :: observant, practical, unwilling to accept dismissive answers
    npcs.lina_dalen.discovered_information :: {}
    npcs.lina_dalen.drives.fears :: ["losing him to unexplained illness"]
    npcs.lina_dalen.drives.values :: ["persistence", "family"]
    npcs.lina_dalen.drives.wants :: ["help Imran"]
    npcs.lina_dalen.gender :: woman
    npcs.lina_dalen.job :: night-shift diner server; Imran's spouse
    npcs.lina_dalen.knowledge.channels :: ["home", "Imran's workmates", "diner regulars"]
    npcs.lina_dalen.knowledge.facts.bellamy :: R69: Rin gave her the Bellamy Street clinic address; stone must never be brought inside
    npcs.lina_dalen.knowledge.facts.imran_schedule :: R69: Imran sleeps until ~04:00 and starts his cab shift at 05:30; never takes the stone off, not to shower or sleep
    npcs.lina_dalen.knowledge.facts.rin_number :: R74: Rin's card and number, 2026-10-15
    npcs.lina_dalen.knowledge.facts.symptom_timeline :: changes began after Imran started wearing Gallo's stone; she has the approximate date and knows which cab rank and shifts may have witnesses
    npcs.lina_dalen.name :: Lina Dalen
    npcs.lina_dalen.relationships.imran_dalen.attitude :: worried, protective
    npcs.lina_dalen.relationships.imran_dalen.believes_identity :: overworked husband whose strange symptoms need medical help
    npcs.lina_dalen.relationships.imran_dalen.credit :: []
    npcs.lina_dalen.relationships.imran_dalen.grievance :: []
    npcs.lina_dalen.relationships.imran_dalen.tie :: spouse
    npcs.lina_dalen.relationships.rin_hale :: R68: {tie: the investigator who asked her, attitude: hopeful, desperate, credit: [], grievance: [], believes_identity: a PI looking into the stones}
    npcs.lina_dalen.relationships.rin_hale.attitude :: R85: grateful; trusts him fully
    npcs.lina_dalen.relationships.rin_hale.credit :: R76: [took the stone off Imran and got him to hospital, 2026-10-14]
    npcs.lina_dalen.state.due :: R85: none pending; on Rin's contact
    npcs.lina_dalen.state.plan :: R69: let Rin in when he says; get Imran to the Bellamy doctor once the stone is off; keep the stone out of the clinic
    npcs.lina_dalen.state.position :: R72: Ashfall General ER with Imran
    npcs.lina_dalen.state.status :: R85: gave her signed statement to Mara 15:00 Oct 19 (Gallo's, under the counter, ~6 weeks ago, $60, a luck stone, and what followed); witness fee arranged; back with Imran
    npcs.mara_quill.belongs :: ["lantern_office"]
    npcs.mara_quill.capability.overall_level :: 4
    npcs.mara_quill.capability.skills.bureaucracy :: T2
    npcs.mara_quill.capability.skills.investigation :: T2
    npcs.mara_quill.capability.skills.occult_lore :: T2
    npcs.mara_quill.character :: dry, procedural, overworked; trusts paper, then people who bring paper; occasionally very funny by accident
    npcs.mara_quill.discovered_information :: {}
    npcs.mara_quill.drives.fears :: ["false alarms closing the Office", "a breach outrunning it"]
    npcs.mara_quill.drives.values :: ["verification", "civilian safety"]
    npcs.mara_quill.drives.wants :: ["contain real hazards quietly", "evidence strong enough to act"]
    npcs.mara_quill.gender :: woman
    npcs.mara_quill.job :: municipal risk analyst; quietly, Lantern Office field coordinator
    npcs.mara_quill.knowledge.channels :: ["municipal incident reports", "Lantern archive", "restricted databases", "Transit safety liaison"]
    npcs.mara_quill.knowledge.facts.capacity :: the Office has no ready two-person assault or containment team; Mara can assess, pay small fees and request narrow safety action with proof
    npcs.mara_quill.knowledge.facts.document_request :: a normal October 5 request to Merrow for Ferris outage reasons is pending; this request neither accuses Rusk nor identifies any magical cause.
    npcs.mara_quill.knowledge.facts.eli_statement :: R53: Eli Voss's signed statement 2026-10-10 (name kept under a reference number in her file): windows, Halden Lane, door 7-B, Rusk, crates, the shard, the chase, the hut, and a figure on the far platform he described against the doorframe
    npcs.mara_quill.knowledge.facts.haller_saying :: R86: Rin's email 2026-10-19: Haller's words on raw ember glass — straight out of a wall; "what you take from below, below comes looking for"; keep cold, closed, away from people, never sold back
    npcs.mara_quill.knowledge.facts.imran_footage :: R75: Rin's footage of the removal and Imran's mumbling (audio), 2026-10-14
    npcs.mara_quill.knowledge.facts.imran_recording :: R82: Rin forwarded Lina's recording of Imran's sleep-talk 2026-10-17; Mara told him not to play it to anyone else
    npcs.mara_quill.knowledge.facts.jo_statement :: R75: Jo Kestrel's written statement 2026-10-15: strong detector readings behind Gallo's counter Oct 9, Gallo's denials, the courier and plate photos
    npcs.mara_quill.knowledge.facts.lina_statement :: R85: Lina Dalen's signed statement 2026-10-19: Imran bought a luck stone under the counter at Gallo's ~6 weeks ago for $60
    npcs.mara_quill.knowledge.facts.m_cutoff :: R60: M cut the laundromat holder loose 2026-10-11; holder under a doctor's care
    npcs.mara_quill.knowledge.facts.orin_call :: R60: Rin's word-for-word notes of the 2026-10-09 call from a man calling himself Orin: $2,000 for "two small pieces", a standing job offer, "careful people live a long time in this city"; the window ran exactly to booking that night after
    npcs.mara_quill.knowledge.facts.pattern :: three outages near old routes in two months including Ferris Yard on Sept 15; no link to Eli or the illicit Merrow operation established at Round 0
    npcs.mara_quill.knowledge.facts.public_summary :: public risk summaries list the three outage locations and dates; they omit covert theory.
    npcs.mara_quill.knowledge.facts.rin_account :: R36: full account as above, from Rin 2026-10-08; Rin's Transit witness unnamed
    npcs.mara_quill.knowledge.facts.rin_folder :: R47: Rin's evidence folder 2026-10-09: site photos, M thread, OX-9 carton, courier photos and plate KT 72 VRN, timeline of seven window dates, Eli's notes with his name blacked out
    npcs.mara_quill.knowledge.facts.rm12_0417 :: R32: R. Hale, licensed PI, reported cinderlings drawn to dark-glass lucky charms being sold, fire damage in a Kettering basement, carriers ill, 2026-10-08
    npcs.mara_quill.knowledge.facts.runner_footage :: R90: Rin's Southport footage 2026-10-21 04:06–04:13: a small slag creature came out through the outfall grate at low water, exchanged a red chip and a paper message with the Choir courier, and went back
    npcs.mara_quill.knowledge.facts.rusk_footage :: R63: Rin's clips 2026-10-11 16:20: Rusk in a Merrow pickup checking the Halden service door padlock; plate readable; also Rin's exact words to Orin
    npcs.mara_quill.knowledge.facts.tanner_lane_bag :: R79: Rin saw Gallo carry a small zipped bag to his house at 14 Tanner Lane 15:40 Oct 13 and return without it
    npcs.mara_quill.knowledge.facts.transit_safety_liaison :: R48: has a liaison at Transit Safety, separate from Transit management and Merrow
    npcs.mara_quill.name :: Mara Quill
    npcs.mara_quill.relationships.jonas_rusk.attitude :: professionally skeptical, no personal accusation
    npcs.mara_quill.relationships.jonas_rusk.believes_identity :: supervisor responsible for requested records, not known corrupt
    npcs.mara_quill.relationships.jonas_rusk.credit :: []
    npcs.mara_quill.relationships.jonas_rusk.grievance :: []
    npcs.mara_quill.relationships.jonas_rusk.tie :: identified Merrow night supervisor in an outage report
    npcs.mara_quill.relationships.rin_hale :: R35: {tie: analyst handling Rin's hazard report, attitude: neutral, professionally sceptical, credit: [], grievance: [], believes_identity: licensed PI R. Hale}
    npcs.mara_quill.relationships.rin_hale.attitude :: R81: trusts him; wants to keep working with him
    npcs.mara_quill.relationships.rin_hale.credit :: R47: [brought her the first real evidence on the outages, 2026-10-09]
    npcs.mara_quill.state.due :: R90: 2026-10-22 afternoon LO-04 request and Transit Safety mesh request; 2026-10-23 payment
    npcs.mara_quill.state.plan :: R90: request the sealed part of the 2004 file (LO-04) today on the strength of the footage; ask Transit Safety this afternoon for fine stainless "vermin mesh" on the Southport outfall grate and the Mercer sump screen; keep the seized glass sealed; retainer draft; pay Rin $2,000 Friday
    npcs.mara_quill.state.position :: city risk management office
    npcs.mara_quill.state.status :: R90: watched Rin's Southport runner footage 09:30 Oct 22; frightened; now holds physical proof of something coming out of the old route
    npcs.mrs_okafor.belongs :: []
    npcs.mrs_okafor.capability.overall_level :: 1
    npcs.mrs_okafor.character :: cheerful, nosy, brings food whether asked or not
    npcs.mrs_okafor.discovered_information :: {}
    npcs.mrs_okafor.drives.fears :: ["an empty unit"]
    npcs.mrs_okafor.drives.values :: ["fairness"]
    npcs.mrs_okafor.drives.wants :: ["rent", "a tenant who keeps the block safe"]
    npcs.mrs_okafor.gender :: woman
    npcs.mrs_okafor.job :: landlady, owns the Hale Workshop block
    npcs.mrs_okafor.knowledge.channels :: ["the block"]
    npcs.mrs_okafor.knowledge.facts :: {}
    npcs.mrs_okafor.knowledge.facts.jo_at_shop :: R22: saw a woman wait outside the workshop ~22:30–23:05 Oct 7; Rin said they know each other
    npcs.mrs_okafor.name :: Grace Okafor
    npcs.mrs_okafor.relationships.rin_hale.attitude :: fond; thinks Rin works too late and eats too little
    npcs.mrs_okafor.relationships.rin_hale.believes_identity :: null
    npcs.mrs_okafor.relationships.rin_hale.credit :: R80: [Rin chased off the man who was breaking into her car; paid November rent early, 2026-10-15]
    npcs.mrs_okafor.relationships.rin_hale.grievance :: []
    npcs.mrs_okafor.relationships.rin_hale.tie :: tenant for three years
    npcs.mrs_okafor.state.due :: 2026-10-07 08:00 normal building round; immediately on a real tenant or property emergency
    npcs.mrs_okafor.state.plan :: keep the block in order; feed Rin when she thinks Rin looks thin
    npcs.mrs_okafor.state.position :: upstairs flat on the Hale Workshop block
    npcs.mrs_okafor.state.status :: R78: got November's rent two weeks early; delighted; gave Rin a tub of stew
    npcs.nadia_voss.belongs :: []
    npcs.nadia_voss.capability.overall_level :: 1
    npcs.nadia_voss.character :: blunt, funny when exhausted, keeps lists, hates being handled; pays her debts to the cent
    npcs.nadia_voss.discovered_information :: {}
    npcs.nadia_voss.drives.fears :: ["Eli hurt", "being humoured"]
    npcs.nadia_voss.drives.values :: ["family", "follow-through"]
    npcs.nadia_voss.drives.wants :: ["find Eli", "a straight answer"]
    npcs.nadia_voss.gender :: woman
    npcs.nadia_voss.job :: restaurant shift manager
    npcs.nadia_voss.knowledge.channels :: ["family contact", "Eli's messages", "police", "Eli's flat"]
    npcs.nadia_voss.knowledge.facts.eli_missing :: Eli vanished during a night maintenance call on the night of Oct 4.
    npcs.nadia_voss.knowledge.facts.papers :: She holds a spare key to Eli's Lowfield flat; his Red Line work orders and a map with the Red Spur circled are there.
    npcs.nadia_voss.knowledge.facts.phone_last_seen :: R1: family-plan locator shows Eli's phone last seen Mon Oct 5 06:40, Canal Street embankment area, ~300 m accuracy
    npcs.nadia_voss.knowledge.facts.phone_plan :: Eli's phone is on her family plan; she has never thought to check its location history.
    npcs.nadia_voss.knowledge.facts.voicemail :: 01:12 Oct 5, Eli says the lights went off after sign-out, someone is sending crews down when nobody should be there, and not to call his work.
    npcs.nadia_voss.name :: Nadia Voss
    npcs.nadia_voss.relationships.eli_voss.attitude :: protective, exasperated
    npcs.nadia_voss.relationships.eli_voss.believes_identity :: null
    npcs.nadia_voss.relationships.eli_voss.credit :: []
    npcs.nadia_voss.relationships.eli_voss.grievance :: []
    npcs.nadia_voss.relationships.eli_voss.tie :: older sister
    npcs.nadia_voss.relationships.rin_hale.attitude :: R77: grateful; trusts him
    npcs.nadia_voss.relationships.rin_hale.believes_identity :: freelance finder of people
    npcs.nadia_voss.relationships.rin_hale.credit :: R8: [found Eli alive and brought him safe, 2026-10-06]
    npcs.nadia_voss.relationships.rin_hale.grievance :: []
    npcs.nadia_voss.relationships.rin_hale.tie :: R1: hired PI, client since 2026-10-06
    npcs.nadia_voss.state.due :: R19: none pending; checks in with Rin if Eli is threatened
    npcs.nadia_voss.state.plan :: R9: go home and rest; work her shift tomorrow; text Eli and expect quick answers; tell police he is found; wants Rin to call after the clinic with the cost
    npcs.nadia_voss.state.position :: R49: at work, shift Oct 9
    npcs.nadia_voss.state.status :: R82: fed Rin and Eli at Marisol's Saturday 17 Oct; tore up the food bill; charged only the drinks
    npcs.orin_sable.belongs :: ["ash_choir"]
    npcs.orin_sable.capability.overall_level :: 5
    npcs.orin_sable.capability.skills.deception :: T2
    npcs.orin_sable.capability.skills.influence :: T2
    npcs.orin_sable.capability.skills.occult_lore :: T3
    npcs.orin_sable.character :: courteous, amused, generous with small things; collects people the way he collects objects; never raises his voice
    npcs.orin_sable.discovered_information :: {}
    npcs.orin_sable.drives.fears :: ["the Surveyor replacing him", "being made common"]
    npcs.orin_sable.drives.values :: ["rarity", "control", "good manners"]
    npcs.orin_sable.drives.wants :: ["control of the only steady residue supply in Ashfall", "leverage over the Lantern Office"]
    npcs.orin_sable.gender :: man
    npcs.orin_sable.job :: occult broker
    npcs.orin_sable.knowledge.channels :: ["Ash Choir cells", "Rusk", "the Surveyor's messengers", "half the pawnshops in Ashfall"]
    npcs.orin_sable.knowledge.facts.cinder_glass :: Residue from the old sealed breach under the spur; it makes small workings stronger and draws lesser demons.
    npcs.orin_sable.knowledge.facts.fallback :: Orin knows the Southport runoff route can transport small parcels via the Mercer sump, but the pumps and small grilles limit bulk freight; Halden is the useful route for big crates.
    npcs.orin_sable.knowledge.facts.jo_lead :: Gallo once mentioned Kestrel questioning the charms; Orin can find her through ordinary hunting work contacts but has not hired or met her at Round 0.
    npcs.orin_sable.knowledge.facts.risk_audit :: Rusk mentioned municipal questions about Ferris; Orin does not know Mara's covert affiliation.
    npcs.orin_sable.knowledge.facts.seal :: Taking residue out slowly weakens the seal; the Surveyor pays for exactly that.
    npcs.orin_sable.name :: Orin Sable
    npcs.orin_sable.relationships.jo_kestrel.attitude :: competent but untested
    npcs.orin_sable.relationships.jo_kestrel.believes_identity :: independent human hunter who works through Pike
    npcs.orin_sable.relationships.jo_kestrel.credit :: []
    npcs.orin_sable.relationships.jo_kestrel.grievance :: []
    npcs.orin_sable.relationships.jo_kestrel.tie :: prospective contractor only; no deal at Round 0
    npcs.orin_sable.relationships.jonas_rusk.attitude :: useful, replaceable
    npcs.orin_sable.relationships.jonas_rusk.believes_identity :: null
    npcs.orin_sable.relationships.jonas_rusk.credit :: []
    npcs.orin_sable.relationships.jonas_rusk.grievance :: []
    npcs.orin_sable.relationships.jonas_rusk.tie :: supplier
    npcs.orin_sable.relationships.rin_hale :: R51: {tie: holder of his lost stock; potential recruit, attitude: interested, courteous, credit: [], grievance: [took the Kettering stock], believes_identity: capable independent hunter-PI, Pike's man}
    npcs.orin_sable.relationships.rin_hale.attitude :: R52: amused, wary, interested; sees him as a threat to the supply and a possible recruit
    npcs.orin_sable.relationships.the_surveyor.attitude :: fascinated and afraid
    npcs.orin_sable.relationships.the_surveyor.believes_identity :: null
    npcs.orin_sable.relationships.the_surveyor.credit :: []
    npcs.orin_sable.relationships.the_surveyor.grievance :: []
    npcs.orin_sable.relationships.the_surveyor.tie :: patron and buyer
    npcs.orin_sable.state.due :: R89: next low water at Mercer; the Surveyor's reply by runner
    npcs.orin_sable.state.plan :: R89: keep his standing with the Surveyor; run small parcels through Mercer/Southport at low water; lie low on the surface; keep the work offer to Rin open
    npcs.orin_sable.state.position :: private dealer's flat in the Old Exchange district; known by phone and by reputation
    npcs.orin_sable.state.status :: R89: chose not to pressure Rin this week (NO, AND); answered the Surveyor's token through the runner 04:11 Wed 21 Oct: the city has seized surface stock; asks patience; promises the Mercer route will carry what Halden can't
    npcs.pike_adeyemi.belongs :: []
    npcs.pike_adeyemi.capability.overall_level :: 2
    npcs.pike_adeyemi.character :: unhurried, nosy, generous with coffee and stingy with credit; knows everybody's business and calls it customer service
    npcs.pike_adeyemi.discovered_information :: {}
    npcs.pike_adeyemi.drives.fears :: ["trouble following a job back to his door"]
    npcs.pike_adeyemi.drives.values :: ["paying debts", "reputation"]
    npcs.pike_adeyemi.drives.wants :: ["his cut", "a quiet bar"]
    npcs.pike_adeyemi.gender :: man
    npcs.pike_adeyemi.job :: owner of The Last Stop, a bar under the elevated line; passes along odd jobs for 15%
    npcs.pike_adeyemi.knowledge.channels :: ["bar talk", "regular clients", "Kestrel", "Rin"]
    npcs.pike_adeyemi.knowledge.facts.laundromat_job :: a Kettering laundromat owner says something in the basement is killing rats and cats and scorching the pipes; pays $400
    npcs.pike_adeyemi.knowledge.facts.rin_cover_story :: R64: Rin's cover story for strangers: in Ashfall ~5 years, parents in the countryside, farm people (a lie Rin asked him to tell)
    npcs.pike_adeyemi.name :: Pike Adeyemi
    npcs.pike_adeyemi.relationships.jo_kestrel.attitude :: respects her
    npcs.pike_adeyemi.relationships.jo_kestrel.believes_identity :: null
    npcs.pike_adeyemi.relationships.jo_kestrel.credit :: []
    npcs.pike_adeyemi.relationships.jo_kestrel.grievance :: []
    npcs.pike_adeyemi.relationships.jo_kestrel.tie :: job broker
    npcs.pike_adeyemi.relationships.rin_hale.attitude :: likes Rin, would never say so
    npcs.pike_adeyemi.relationships.rin_hale.believes_identity :: demon-blooded hunter (he guessed; has never said it aloud)
    npcs.pike_adeyemi.relationships.rin_hale.credit :: ["Rin cleared a nest from his cellar last winter"]
    npcs.pike_adeyemi.relationships.rin_hale.grievance :: []
    npcs.pike_adeyemi.relationships.rin_hale.tie :: job broker for three years
    npcs.pike_adeyemi.state.due :: R64: immediately if the stranger or anyone else asks about Rin again; weekly work check
    npcs.pike_adeyemi.state.plan :: R64: keep the bar boring; give the cover story if asked; watch who comes in; would rather Rin stayed away a few days
    npcs.pike_adeyemi.state.position :: the_last_stop
    npcs.pike_adeyemi.state.status :: R64: agreed 20:32 Oct 12 to give Rin's cover story if asked again: came to Ashfall about five years ago, parents in the countryside, farm people, never talks about them; delivered offhand like a barman who doesn't care
    npcs.police_sergeant_tip :: R81: {name: police sergeant (Mara's contact, unnamed), job: Ashfall Police Department sergeant, belongs: [ashfall_police], gender: unknown, character: unknown; trusted by Mara, state: {status: receiving Mara's anonymous-source tip with the Tanner Lane footage, plan: assess the assault/threat on Gallo, due: 2026-10-19}, capability: {overall_level: 3}}
    npcs.police_sergeant_tip.state.due :: R83: this week
    npcs.police_sergeant_tip.state.plan :: R83: identify and pursue the shaven-headed man for the assault/threat on Gallo
    npcs.police_sergeant_tip.state.status :: R83: called Mara 10:30 Oct 19: wants the shaven-headed man from the Tanner Lane footage
    npcs.spur_warden.belongs :: ["cinder_court"]
    npcs.spur_warden.capability.overall_level :: 6
    npcs.spur_warden.capability.skills.combat :: T2
    npcs.spur_warden.character :: a heavy armoured thing of slag and rail iron; territorial, not clever; hates light
    npcs.spur_warden.discovered_information :: {}
    npcs.spur_warden.drives.fears :: ["strong light", "losing its binding"]
    npcs.spur_warden.drives.values :: []
    npcs.spur_warden.drives.wants :: ["hold the seam"]
    npcs.spur_warden.gender :: none
    npcs.spur_warden.job :: demon bound to guard the residue seam in the Red Spur
    npcs.spur_warden.knowledge.channels :: ["its territory"]
    npcs.spur_warden.knowledge.facts :: {}
    npcs.spur_warden.name :: the spur warden
    npcs.spur_warden.relationships :: {}
    npcs.spur_warden.state.due :: when the sealed seam or far platform is actually entered or physically disturbed; otherwise continue guard routine
    npcs.spur_warden.state.plan :: kill anything that touches the far seam or the seal
    npcs.spur_warden.state.position :: sealed_red_spur, far platform
    npcs.spur_warden.state.status :: guarding the residue face; lets Orin's crews take crates from the near end only
    npcs.suds_and_spin_owner :: R11: {name: Rosa Fenn, job: owner of Suds & Spin laundromat, Kettering, belongs: [], gender: woman, character: practical, sturdy, unfussy; temper roll 9 (ordinary), state: {position: kettering_laundromat counter, status: hired Rin through Pike; will not go into the basement, plan: let Rin work the basement; pay $400 on completion, due: when Rin reports the job done or fails}, relationships: {rin_hale: {tie: hired through Pike, attitude: neutral, practical, credit: [], grievance: [], believes_identity: Pike's pest-and-odd-job person}}, knowledge: {facts: {basement: cats stopped coming in through the grate; cooked rat by the boiler; scorched pipes}}, capability: {overall_level: 1}}
    npcs.suds_and_spin_owner.relationships.rin_hale.attitude :: R15: grateful
    npcs.suds_and_spin_owner.relationships.rin_hale.credit :: R15: [cleared the basement creature, 2026-10-07]
    npcs.suds_and_spin_owner.state.due :: R15: none pending; ordinary shop routine
    npcs.suds_and_spin_owner.state.plan :: R15: get the cats back; run the shop
    npcs.suds_and_spin_owner.state.status :: R39: closing the laundromat 22:00 Oct 8; inside, lights going off
    npcs.taxi_driver_lowfield :: R68: {name: older Sikh cab driver at the Lowfield rank (unnamed), job: taxi driver, belongs: [], gender: man, character: steady, observant, flask of tea; temper roll pending, state: {position: lowfield_cab_rank, status: told Rin about Imran Dalen's stone and pointed him to Lina, plan: ordinary shifts, due: ordinary routine}, knowledge: {facts: {imran: Imran shows off a stone from Gallo's as his luck and has been sick and missing shifts}}, capability: {overall_level: 1}}
    npcs.teodor_varga :: R86: {name: Teodor Varga, job: ironworker, Ironside Lane, Lower Docks; in his seventies, belongs: [], gender: man, character: unknown (not met); sworn to confidentiality after 2004 city contract work, state: {position: Ironside Lane, Lower Docks, status: retired or semi-retired ironworker, plan: unknown until Mara's letter, due: on Mara's letter (2026-10-21 or later)}, knowledge: {facts: {2004: made iron fittings in 2004 for a city job under the Red Line (Mara's file)}}, capability: {overall_level: 4, skills: {ironwork: T3}}}
    npcs.teodor_varga.state.due :: R89: 2026-10-22 15:00 at Ironside Lane
    npcs.teodor_varga.state.plan :: R89: meet Rin Thursday 2026-10-22 15:00; show him his 2004 notebook
    npcs.teodor_varga.state.status :: R89: replied to Mara by handwritten letter Oct 20 (YES, AND): will see Rin Thursday 15:00 at the green door, Ironside Lane; "Tell the young man I kept my notebook"
    npcs.the_surveyor.belongs :: ["cinder_court"]
    npcs.the_surveyor.capability.overall_level :: 9
    npcs.the_surveyor.capability.skills.bargaining :: T2
    npcs.the_surveyor.capability.skills.combat :: T3
    npcs.the_surveyor.capability.skills.demonic_channeling :: T3
    npcs.the_surveyor.character :: precise, patient, speaks like a contract; enjoys a good bargain more than a kill
    npcs.the_surveyor.discovered_information :: {}
    npcs.the_surveyor.drives.fears :: ["premature exposure", "rivals in the Court"]
    npcs.the_surveyor.drives.values :: ["binding bargains", "territory"]
    npcs.the_surveyor.drives.wants :: ["a stable route to the surface", "the sealer's line"]
    npcs.the_surveyor.gender :: unknown
    npcs.the_surveyor.job :: demonic route-broker for the Cinder Court
    npcs.the_surveyor.knowledge.channels :: ["Cinder Court", "sensing within its territory", "the original seal responding to its sealer's bloodline, plus site-specific traces through carried residue", "Orin", "bleed-drain runner via Mercer/Southport"]
    npcs.the_surveyor.knowledge.facts.resonance :: A sealer-line surge is recognizable only inside connected old routes or within 50 metres of exposed, unneutralized Red Spur cinder glass; an approach within 20 metres of the main seal also registers. The signal provides neither identity nor exact location; Orin and physical scouts must investigate.
    npcs.the_surveyor.knowledge.facts.runner_route :: A corroded bleed slit lets small bound messengers reach the Mercer outer gallery at low water, then the Southport outfall. It cannot carry the Surveyor or its full forces; flooding, shut grilles or a repair can block it.
    npcs.the_surveyor.knowledge.facts.seal :: the seal was set in 2004 by a demon who broke from the Court; its mark is in the masonry and would answer that demon's blood
    npcs.the_surveyor.name :: The Surveyor
    npcs.the_surveyor.relationships.orin_sable.attitude :: useful, watched
    npcs.the_surveyor.relationships.orin_sable.believes_identity :: null
    npcs.the_surveyor.relationships.orin_sable.credit :: ["steady residue removal"]
    npcs.the_surveyor.relationships.orin_sable.grievance :: []
    npcs.the_surveyor.relationships.orin_sable.tie :: surface broker
    npcs.the_surveyor.state.due :: R89: next low water; seam check
    npcs.the_surveyor.state.plan :: R89: weigh Orin against other means; seam assessment 2026-10-20 delayed into the next low water; may try the bleed-drain itself for a closer look
    npcs.the_surveyor.state.position :: lower_works; sends a voice up through the spur
    npcs.the_surveyor.state.status :: R89: received Orin's word by runner after 04:13 Oct 21: surface stock seized, Halden shut, Mercer route promised
    npcs.tomas_reyes.belongs :: ["ashfall_transit_authority"]
    npcs.tomas_reyes.capability.overall_level :: 1
    npcs.tomas_reyes.character :: loyal, jumpy, overshares when nervous, terrible at keeping a straight face
    npcs.tomas_reyes.discovered_information :: {}
    npcs.tomas_reyes.drives.fears :: ["being next"]
    npcs.tomas_reyes.drives.values :: ["friends first"]
    npcs.tomas_reyes.drives.wants :: ["keep his job", "Eli safe"]
    npcs.tomas_reyes.gender :: man
    npcs.tomas_reyes.job :: Transit track maintainer
    npcs.tomas_reyes.knowledge.channels :: ["work", "friends"]
    npcs.tomas_reyes.knowledge.facts.relay_huts :: Eli goes to the old Canal Street relay huts to think; Tomas has not connected this to the disappearance.
    npcs.tomas_reyes.knowledge.facts.windows :: Eli showed him the mismatched end times two weeks ago.
    npcs.tomas_reyes.name :: Tomas Reyes
    npcs.tomas_reyes.relationships.eli_voss.attitude :: loyal
    npcs.tomas_reyes.relationships.eli_voss.believes_identity :: null
    npcs.tomas_reyes.relationships.eli_voss.credit :: []
    npcs.tomas_reyes.relationships.eli_voss.grievance :: []
    npcs.tomas_reyes.relationships.eli_voss.tie :: best friend
    npcs.tomas_reyes.state.due :: R11: immediately if Eli or Nadia contacts him with specific evidence; else his day shifts
    npcs.tomas_reyes.state.plan :: keep his head down; would help Eli at once if asked
    npcs.tomas_reyes.state.position :: his Lowfield flat; day shifts
    npcs.tomas_reyes.state.status :: R76: hearing yard gossip about the Halden lockdown and audit; texted Eli Oct 15
    npcs.unit9_keeper :: R80: {name: older thin man in a cardigan at Unit 9 (unnamed), job: keeps Unit 9 for Brannock; receives stock and notes, belongs: [ash_choir], gender: man, character: unknown; temper roll pending, state: {position: Unit 9, Exchange Yard, status: took Gallo's stones and notebook 23:50 Oct 16, plan: store them; report to M or Orin's people, due: 2026-10-17 morning report}, capability: {overall_level: 2}}
    npcs.unit9_keeper.state.due :: R82: on Trading Standards summons
    npcs.unit9_keeper.state.status :: R82: present at the 10:00 Oct 19 inspection; gave name and lawyer only
    npcs.vic.belongs :: ["merrow_utility_solutions"]
    npcs.vic.capability.overall_level :: 2
    npcs.vic.character :: quiet, nervous, wants out
    npcs.vic.discovered_information :: {}
    npcs.vic.drives.fears :: ["police", "the spur at night"]
    npcs.vic.drives.values :: ["money"]
    npcs.vic.drives.wants :: ["cash", "out of the side job"]
    npcs.vic.gender :: man
    npcs.vic.job :: Merrow night labourer on Rusk's side payroll
    npcs.vic.knowledge.channels :: ["Rusk"]
    npcs.vic.knowledge.facts.crates :: they carry sealed crates out of 7-B to a van; he once saw something move in the spur
    npcs.vic.knowledge.facts.schedules :: remembers the October 4 run, late sign-outs and which van was used; did not see Eli's hiding place; can identify 7-B
    npcs.vic.name :: R59: Vic Moreno
    npcs.vic.relationships.dale.attitude :: goes along with him
    npcs.vic.relationships.dale.believes_identity :: null
    npcs.vic.relationships.dale.credit :: []
    npcs.vic.relationships.dale.grievance :: []
    npcs.vic.relationships.dale.tie :: crewmate
    npcs.vic.relationships.jonas_rusk.attitude :: uneasy
    npcs.vic.relationships.jonas_rusk.believes_identity :: null
    npcs.vic.relationships.jonas_rusk.credit :: []
    npcs.vic.relationships.jonas_rusk.grievance :: []
    npcs.vic.relationships.jonas_rusk.tie :: boss on the side payroll
    npcs.vic.state.due :: R53: when Rusk calls him back to work
    npcs.vic.state.plan :: keep working while he needs the money and look for an excuse to quit; during an inspection follow Rusk's public story unless contradictory evidence or personal risk breaks it
    npcs.vic.state.position :: Ferris Yard on window nights; Lowfield some evenings
    npcs.vic.state.status :: R53: told by Rusk 21:00 Oct 9: no runs for two weeks; relieved
    quests.ash_beneath.child_quests :: ["find_eli_voss"]
    quests.ash_beneath.objective :: Find out what happened to Eli Voss and who is sending crews below the Red Line.
    quests.ash_beneath.participants :: []
    quests.ash_beneath.role :: MAIN
    quests.ash_beneath.source_ref :: nadia_voss
    quests.ash_beneath.status :: available
    quests.ash_beneath.type :: CHAIN
    quests.find_eli_voss.objective :: Find Eli Voss and get him somewhere safe.
    quests.find_eli_voss.participants :: []
    quests.find_eli_voss.quest_level :: 3
    quests.find_eli_voss.role :: SIDE
    quests.find_eli_voss.source_ref :: nadia_voss
    quests.find_eli_voss.status :: R6: completed 2026-10-06 21:30 — Eli brought safe to hale_workshop; quest XP 29 paid (R3, meaningful)
    quests.find_eli_voss.support_refs :: []
    quests.find_eli_voss.type :: SHORT
    quests.laundromat_job.objective :: Clear whatever is in the Suds & Spin basement; $400 via Pike.
    quests.laundromat_job.participants :: []
    quests.laundromat_job.quest_level :: 3
    quests.laundromat_job.role :: SIDE
    quests.laundromat_job.source_ref :: pike_adeyemi
    quests.laundromat_job.status :: R13: completed 2026-10-07 09:57 — basement creature killed; quest XP 29 paid (R3, meaningful)
    quests.laundromat_job.support_refs :: []
    quests.laundromat_job.type :: SHORT
    rights_obligations.ada_bank_visit :: R55: {type: appointment, parties: [rin_hale, ada_hale], state: {terms: Ada takes Rin to Harland's Bank, Wexley, 2026-10-12 at opening to open the deposit box holding his parent's letters, status: active}}
    rights_obligations.ada_bank_visit.state.status :: R62: done 09:30 Oct 12; deposit box opened; Rin holds his parent's letter
    rights_obligations.charm_custody :: R49: {type: chain of custody, parties: [rin_hale, mara_quill], state: {item: Rosa's steel coin vault, locked, with 2 dark glass stones on black cords, transferred 2026-10-09 14:52; now in Mara's locked office filing cabinet; Rin holds the receipt copy}}
    rights_obligations.charm_custody_2 :: R65: {type: chain of custody, parties: [rin_hale, mara_quill], state: {item: 1 dark glass stone on black cord, worn by the Kettering holder ~11 days, in Rin's steel cash box, transferred 2026-10-13 09:20; in Mara's office drawer with the vault}}
    rights_obligations.charm_custody_3 :: R75: {type: chain of custody, parties: [rin_hale, mara_quill], state: {item: 1 dark glass stone on cut black cord, removed from a living patient now in hospital 2026-10-14 23:05, in Rin's third steel box, transferred 2026-10-15 10:05; plus USB of Rin's footage; in Mara's drawer}}
    rights_obligations.city_contract :: R49: {type: contract, parties: [rin_hale, city_risk_office (Mara Quill)], state: {jobs: [report and custody of charms — $750, done, paid by bank transfer by 2026-10-14; documented Halden window from outside, no entry via 7-B — $1,500 on delivery, open], terms: confidentiality; no authority to enter restricted municipal or Transit premises; payment on delivery of documented work, signed: 2026-10-09 14:50}}
    rights_obligations.city_contract.state.jobs :: R83: [report and custody — $750 paid 2026-10-14; documented Halden window from outside — $1,500 on delivery, open; documented surveillance resulting in the Unit 9 seizure — $1,500, approved 2026-10-19, paid by Fri 2026-10-23; Tanner Lane assault footage bonus — $500, approved 2026-10-19, paid by Fri 2026-10-23]
    rights_obligations.eli_case :: R19: {type: contract (terms unsettled), parties: [rin_hale, eli_voss], state: {work: look into the Halden Lane / Red Spur crates and who is behind them, offer: Eli offered ~3 days at the day rate from ~$800 savings, status: Rin began work 2026-10-07 without fixing terms; payment not yet agreed}}
    rights_obligations.eli_case.state.status :: R77: closed 2026-10-15 17:35; Eli paid $375 by transfer (half the ~$750 he offered; Rin cut it because the city paid); nothing owed either way
    rights_obligations.eli_clinic_promise :: R9: {type: informal promise, parties: [rin_hale, nadia_voss], state: {terms: Rin takes Eli to a no-questions clinic on 2026-10-07 and calls Nadia after with the cost, status: active}}
    rights_obligations.eli_clinic_promise.state.status :: R19: closed 2026-10-07 19:30; Nadia told the cost and repaid Rin $250
    rights_obligations.eli_statement :: R50: {type: appointment, parties: [eli_voss, mara_quill, rin_hale], state: {terms: Eli gives a signed statement in room 3-14, 2026-10-10 10:00, Rin present; Mara then sends a Transit Safety whistleblower letter and pays $150, status: active}}
    rights_obligations.eli_statement.state.status :: R53: done 2026-10-10 10:00–11:05; signed and initialled statement; witnesses Mara and Rin; Nadia present; Transit Safety letter Monday 2026-10-12; $150 by transfer to Eli
    rights_obligations.footage_custody :: R81: {type: chain of custody, parties: [rin_hale, mara_quill], state: {item: USB with the Tanner Lane collection footage, the tail and Unit 9, transferred 2026-10-17 10:20}}
    rights_obligations.haller_knives :: R44: {type: commission, parties: [rin_hale, dutch_haller], state: {work: two treated 4-inch fixed blades, price: $600, paid: $300 deposit 2026-10-08 23:50, balance: $300 on collection, ready: Sunday 2026-10-11 after 21:00 at the back loading door, proof: Haller's paper receipt, status: active}}
    rights_obligations.haller_knives.state.status :: R62: completed 22:00 Oct 11; $300 balance paid with the receipt; two treated knives collected
    rights_obligations.jo_camera_job :: R61: {type: hire, parties: [rin_hale, jo_kestrel], state: {work: recover Rin's clip camera from the Halden drainpipe after dark, fee: $100, paid: up front 20:05 Oct 11 with the $200 owed, status: done 21:05 Oct 11}}
    rights_obligations.jo_cover_job :: R37: {type: hire, parties: [rin_hale, jo_kestrel], state: {work: covert photographs and cover at the Suds & Spin 22:00 pickup, Oct 8; Jo picks her own spot; witness not bodyguard unless she chooses, fee: $200 flat cash (Jo's terms), status: agreed by Jo 16:55 Oct 8; payment due after}}
    rights_obligations.jo_cover_job.state.status :: R61: closed; Jo paid $200 owed, 20:05 Oct 11
    rights_obligations.laundromat_deal :: R2: {type: brokered job, parties: [rin_hale, pike_adeyemi, suds_and_spin_owner], state: {work: clear what is in the Suds & Spin basement, fee: $400 paid by owner on completion, broker cut: Pike 15%, start: Rin agreed to go 2026-10-07, owner opens 07:00, status: active}}
    rights_obligations.laundromat_deal.state.status :: R19: closed 2026-10-07 14:00; Pike's $60 paid; nothing owed
    rights_obligations.lucy_consent :: R68: {type: consent, parties: [l_warren, rin_hale], state: {terms: Lucy's medical report may be used by the City Risk Management Office and Trading Standards with her name withheld, signed 2026-10-14 11:45}}
    rights_obligations.mara_meeting :: R36: {type: appointment, parties: [rin_hale, mara_quill], state: {terms: Rin brings one sealed charm to the City Risk Management Office 2026-10-09 14:00; Mara may then commission paid work; meanwhile Rin emails photos and the M thread, status: active}}
    rights_obligations.mara_meeting.state.status :: R47: meeting held 14:03 Oct 9; Mara offered a contractor form for two paid jobs
    rights_obligations.mara_retainer :: R84: {type: proposed retainer, parties: [rin_hale, mara_quill], state: {status: Rin agreed in principle 2026-10-19; terms to be drafted}}
    rights_obligations.pi_licence.parties :: ["rin_hale", "city_of_ashfall"]
    rights_obligations.pi_licence.state.grants :: work as a private investigator; request public records; serve papers
    rights_obligations.pi_licence.state.holder :: rin_hale
    rights_obligations.pi_licence.state.limits :: no police authority; no right of entry; no carry permit
    rights_obligations.pi_licence.state.status :: valid
    rights_obligations.pi_licence.type :: licence
    rights_obligations.varga_meeting :: R89: {type: appointment, parties: [rin_hale, teodor_varga], state: {terms: meet 2026-10-22 15:00, green door, Ironside Lane; Varga says he kept his 2004 notebook, status: active}}
    rights_obligations.voss_trace :: R1: {type: contract, parties: [rin_hale, nadia_voss], state: {service: missing person trace for Eli Voss, fee: $700 flat, paid: $350 deposit 2026-10-06 cash, balance: $350 on finding Eli, timeframe: Rin estimated 3+ days, expenses: only if pre-agreed, status: active}}
    rights_obligations.voss_trace.state.paid :: R8: $700 total
    rights_obligations.voss_trace.state.status :: R8: completed 2026-10-06 22:20; $350 balance paid in cash; nothing owed either way
    rights_obligations.warren_medical :: R59: {type: paid service, parties: [rin_hale, bellamy_doctor, l_warren], state: {terms: exam today $80 and bloods $120, paid by Rin 2026-10-11; signed written report with results for Rin and Lucy, due 2026-10-14, status: active}}
    rights_obligations.warren_medical.state.status :: R66: done 10:30 Oct 14; signed report delivered to Rin and Lucy: mild anaemia, low white cell count, slightly raised liver enzyme, low core temperature, weight loss — "sustained metabolic strain of unclear origin, improving since exposure to an unidentified warm object ceased"; follow-up in two weeks
    rights_obligations.wharf_room_hold :: R78: {type: room rental, parties: [rin_hale, agnieszka_wolak], state: {terms: back room held a month for $150 cash, 2026-10-16 to 2026-11-16, no ID, no police, no trouble upstairs, status: active}}
    rights_obligations.workshop_lease.parties :: ["rin_hale", "mrs_okafor"]
    rights_obligations.workshop_lease.state.holder :: rin_hale
    rights_obligations.workshop_lease.state.limits :: ordinary commercial lease
    rights_obligations.workshop_lease.state.premises :: hale_workshop
    rights_obligations.workshop_lease.state.rent :: $800 a month, due on the 1st
    rights_obligations.workshop_lease.state.status :: R78: current; November rent $800 paid early 2026-10-15 18:00
    rights_obligations.workshop_lease.type :: leasehold
    world_state.glossary.zh_hans.ada_hale :: Ada Hale = 艾达·霍尔
    world_state.glossary.zh_hans.ash_choir :: the Ash Choir = 灰烬诗班
    world_state.glossary.zh_hans.ashfall_city :: Ashfall City = 灰烬城
    world_state.glossary.zh_hans.bands :: YES, AND = 是，而且; YES = 是; NO, BUT = 否，但是; NO, AND = 否，而且
    world_state.glossary.zh_hans.breach :: breach = 裂口
    world_state.glossary.zh_hans.canal_street :: Canal Street embankment = 运河街堤岸
    world_state.glossary.zh_hans.cinder_court :: the Cinder Court = 余烬宫廷
    world_state.glossary.zh_hans.cinder_glass :: cinder glass = 余烬玻璃
    world_state.glossary.zh_hans.cinderling :: cinderling = 余烬犬
    world_state.glossary.zh_hans.city_risk_office :: City Risk Management Office = 城市风险管理办公室
    world_state.glossary.zh_hans.court_runner :: Slag Runner = 矿渣信使
    world_state.glossary.zh_hans.dale :: Dale = 戴尔
    world_state.glossary.zh_hans.demon :: demon = 恶魔 (lesser = 低等, higher = 高等)
    world_state.glossary.zh_hans.demon_blooded :: demon-blooded = 恶魔血裔
    world_state.glossary.zh_hans.demonic_surge :: demonic surge = 恶魔涌动
    world_state.glossary.zh_hans.door_7b :: door 7-B = 7-B 号门
    world_state.glossary.zh_hans.eli_voss :: Eli Voss = 伊莱·沃斯
    world_state.glossary.zh_hans.ferris_yard :: Ferris Yard = 费里斯车场
    world_state.glossary.zh_hans.gallo_pawn :: Gallo Pawn & Loan = 加洛典当行
    world_state.glossary.zh_hans.gate :: the gate = 大门
    world_state.glossary.zh_hans.grace_okafor :: Grace Okafor, Mrs Okafor = 格蕾丝·奥卡福, 奥卡福太太
    world_state.glossary.zh_hans.halden_lane :: Halden Lane = 哈尔登巷
    world_state.glossary.zh_hans.hale_workshop :: Hale Workshop = 霍尔工作室
    world_state.glossary.zh_hans.hollowed :: the hollowed, hollowing = 空壳人, 空壳化
    world_state.glossary.zh_hans.hunter :: hunter = 猎人
    world_state.glossary.zh_hans.imran_dalen :: Imran Dalen = 伊姆兰·达伦
    world_state.glossary.zh_hans.jo_kestrel :: Jo Kestrel = 乔·凯斯特尔 (Kestrel = 凯斯特尔)
    world_state.glossary.zh_hans.jonas_rusk :: Jonas Rusk = 乔纳斯·拉斯克
    world_state.glossary.zh_hans.kettering :: Kettering = 凯特林
    world_state.glossary.zh_hans.l_warren :: L. Warren = L. 沃伦
    world_state.glossary.zh_hans.lantern_office :: the Lantern Office = 灯笼办公室
    world_state.glossary.zh_hans.lina_dalen :: Lina Dalen = 莉娜·达伦
    world_state.glossary.zh_hans.lower_works :: the Lower Works = 下层工程
    world_state.glossary.zh_hans.lowfield :: Lowfield = 洛菲尔德
    world_state.glossary.zh_hans.lowfield_cab_rank :: Lowfield taxi rank = 洛菲尔德出租车候车点
    world_state.glossary.zh_hans.luck_stone :: luck stone = 幸运石
    world_state.glossary.zh_hans.mara_quill :: Mara Quill = 玛拉·奎尔
    world_state.glossary.zh_hans.mercer_pump :: Mercer flood pump = 默瑟排洪泵站
    world_state.glossary.zh_hans.merrow :: Merrow Utility Solutions = 梅罗公用事业公司
    world_state.glossary.zh_hans.morrow_ward :: Morrow Ward = 莫罗区
    world_state.glossary.zh_hans.nadia_voss :: Nadia Voss = 娜迪亚·沃斯
    world_state.glossary.zh_hans.nightglass_blade :: Nightglass Blade = 夜晶刃
    world_state.glossary.zh_hans.odd_job :: odd job = 零活
    world_state.glossary.zh_hans.old_exchange :: Old Exchange district = 旧交易所区
    world_state.glossary.zh_hans.orin_sable :: Orin Sable = 奥林·塞布尔
    world_state.glossary.zh_hans.outcomes :: Success = 成功; Failure = 失败; Difficulty = 难度
    world_state.glossary.zh_hans.pi :: PI, PI licence = 私家侦探, 私家侦探执照
    world_state.glossary.zh_hans.pike_adeyemi :: Pike Adeyemi = 派克·阿德耶米 (Pike = 派克)
    world_state.glossary.zh_hans.police :: Ashfall Police Department = 灰烬城警察局
    world_state.glossary.zh_hans.red_line :: Red Line = 红线
    world_state.glossary.zh_hans.red_spur :: Red Spur = 红色支线 (sealed = 封闭的红色支线)
    world_state.glossary.zh_hans.relay_hut :: relay hut = 中继小屋
    world_state.glossary.zh_hans.residue :: residue = 残渣
    world_state.glossary.zh_hans.rin_hale :: Rin Hale = 林恩·霍尔 (Rin = 林恩)
    world_state.glossary.zh_hans.round :: ROUND N = 第 N 回合; saved R40 = 已存 R40; save R50 = 下次存档 R50
    world_state.glossary.zh_hans.sal_gallo :: Sal Gallo = 萨尔·加洛
    world_state.glossary.zh_hans.seal :: seal, sealer = 封印, 封印者
    world_state.glossary.zh_hans.southport_outfall :: Southport outfall = 南港排水口
    world_state.glossary.zh_hans.spur_warden :: the spur warden = 支线守卫
    world_state.glossary.zh_hans.stats :: HP = 生命, MP = 魔力, XP = 经验, Level = 等级, fatigue = 疲劳, money = 金钱
    world_state.glossary.zh_hans.suds_and_spin :: Suds & Spin laundromat = 泡泡旋转洗衣店
    world_state.glossary.zh_hans.the_last_stop :: The Last Stop = 末班站酒吧
    world_state.glossary.zh_hans.the_surveyor :: the Surveyor = 勘测者
    world_state.glossary.zh_hans.tomas_reyes :: Tomas Reyes = 托马斯·雷耶斯
    world_state.glossary.zh_hans.transit_authority :: Ashfall Transit Authority = 灰烬城交通局
    world_state.glossary.zh_hans.vic :: Vic = 维克
    world_state.glossary.zh_hans.wexley :: Wexley = 韦克斯利
    world_state.material_history.barnes_rd_check :: R29: 2026-10-08 ~10:05 routine traffic plate-and-helmet check on Barnes Road; Rin waved on; bag not searched
    world_state.material_history.corran_st_awning :: R16: 2026-10-07 ~10:35 wind tore a shop awning loose on Corran Street; Rin swerved past; no effect
    world_state.material_history.delivery_disguise :: R61: 2026-10-11 Rin worked Ferris Road as a food-delivery rider (red rain jacket, thermal bag hiding the blade bag, face-buff, helmet); not linked to the hi-vis contractor at the kiosk
    world_state.material_history.eli_notes :: R19: Eli gave Rin his written notes 2026-10-07: 7 window dates with remembered real sign-out times, van plate (photo), door 7-B, Rusk plus two unnamed men, Tomas can confirm end times, gate camera on the left post aimed at the gate
    world_state.material_history.encounter_cinderling_canal :: R3: 2026-10-06 Rin killed the embankment cinderling; combat XP 12 paid (R2, minor)
    world_state.material_history.encounter_cinderling_suds :: R13: 2026-10-07 Rin killed the Suds & Spin basement cinderling (paid as quest XP for laundromat_job, not combat XP)
    world_state.material_history.evidence_folder :: R45: night of Oct 8 Rin printed and assembled an evidence folder at hale_workshop: site photos, M thread screenshots, OX-9 carton, Jo's courier and plate photos, a timeline Oct 4–8, Eli's notes with his name blacked out, the RM-12 slip
    world_state.material_history.gale_st_night_works :: R62: 2026-10-11 ~22:40 night roadworks closed Gale Street; detour; no effect
    world_state.material_history.gale_st_roadworks :: R17: 2026-10-07 ~11:00 roadworks on Gale Street slowed traffic; no effect
    world_state.material_history.jogger_disguise :: R86: 2026-10-20 dawn Rin ran the canal towpath as a jogger (tights, hoodie, cap, earbuds) to place the camera
    world_state.material_history.kingsway_bus :: R46: 2026-10-09 ~13:30 a city bus broke down across the Kingsway Bridge; long jam; Rin arrived at the Annex at 14:03, three minutes late
    world_state.material_history.kingsway_speedcam :: R76: 2026-10-15 ~11:20 speed-camera van on the Kingsway; not Rin
    world_state.material_history.knife_practice :: R78: 2026-10-16 morning Rin practised drawing Haller's knives (small-of-back sheath and left boot), a hundred draws each
    world_state.material_history.lowfield_blackout :: R70: 2026-10-14 22:40 a Lowfield substation tripped; whole district dark; ordinary fault, cause not announced; diner closed early
    world_state.material_history.lowfield_power_restored :: R72: Lowfield power came back ~23:45 Oct 14
    world_state.material_history.lurcher_walker :: R45: 2026-10-09 ~08:05 a man walked a grey lurcher along the embankment service road; Rin waited till he left
    world_state.material_history.mercer_low_oct21 :: R89: Mercer sump bottomed at 9% ~04:00 Wed 21 Oct; pumps restarted 05:00 (Eli's telemetry)
    world_state.material_history.mercer_sump_oct20 :: R88: 2026-10-20 08:20 Transit telemetry: Mercer sump 38% and falling after weekend drizzle; dry night forecast; expected low (under 15%) ~03:00–05:00 Wed 21 Oct
    world_state.material_history.mill_road_flood :: R11: 2026-10-07 ~09:25 short downpour flooded the Mill Road junction; Rin detoured; no other effect
    world_state.material_history.night_oct10 :: R57: Rin home 02:05 Oct 11, texted Ada, slept till 09:00
    world_state.material_history.night_oct14 :: R74: Rin home 03:20 Oct 15 by taxi and bike; slept until ~07:30
    world_state.material_history.night_oct16 :: R81: Rin left Exchange Yard ~00:10 Oct 17 unseen; copied the footage to laptop, USB and cloud; slept till ~08:30
    world_state.material_history.night_oct6 :: R10: night of Oct 6–7 Rin and Eli slept at hale_workshop; nothing disturbed it
    world_state.material_history.night_oct7 :: R25: night of Oct 7–8 Rin slept at hale_workshop; undisturbed
    world_state.material_history.night_oct8 :: R45: Rin slept at hale_workshop ~00:30–07:00 Oct 9; undisturbed
    world_state.material_history.orin_call_notes :: R53: Rin wrote up the Orin call word for word the evening of Oct 9
    world_state.material_history.r0_01 :: Rin has known since sixteen that the family blood is partly demonic, and has one controlled demonic ability.
    world_state.material_history.r0_02 :: Rin owns the Nightglass Blade and has used it in prior minor demonic encounters.
    world_state.material_history.r0_03 :: Rin cleared a nest from Pike's cellar last winter and finished a job Kestrel had been working last spring.
    world_state.material_history.r0_04 :: Eli Voss disappeared during a night maintenance call on the night of Oct 4.
    world_state.material_history.r0_05 :: Ferris Yard had an overnight outage on Sept 15, publicly blamed on aging equipment.
    world_state.material_history.r0_06 :: Mara sent an ordinary risk-management records request on Oct 5 based on the separate cluster of outages; its existence is not proof of any covert collaboration or known occult cause.
    world_state.material_history.r0_07 :: Nadia Voss came to Hale Workshop with Eli's badge, a map, and his voicemail; Rin has not accepted the job.
    world_state.material_history.rest_oct10 :: R56: Rin slept the afternoon of Oct 10 at the workshop
    world_state.material_history.rest_oct15 :: R76: Rin slept 11:40–15:10 Oct 15
    world_state.material_history.rest_oct8 :: R34: Rin slept at hale_workshop from ~14:30 Oct 8, alarm set for 20:30
    world_state.material_history.rest_oct8_evening :: R38: Rin rested at hale_workshop ~17:10–20:30 Oct 8; HP and MP full
    world_state.material_history.rest_oct9 :: R46: Rin slept again at hale_workshop 09:30–12:30 Oct 9
    world_state.material_history.shard_test :: R7: 2026-10-06 Rin tried to sense the shard's resonance through plastic, cardboard, glass and a steel tin; no reliable reading (failure); learned only that it stays warm and heats any container
    world_state.material_history.tanner_st_patrol :: R66: 2026-10-13 ~17:45 a routine Lowfield patrol worked Tanner Street; Rin had already left; no contact
    world_state.material_history.traffic_harrow_ave :: R6: 2026-10-06 ~21:10 minor van–taxi crash on Harrow Avenue, patrol officer waving traffic past; no contact with Rin
    world_state.material_history.wexley_train :: R62: 2026-10-12 08:40 train to Wexley; routine ticket check
    world_state.material_history.wren_bus_breakdown :: R17: 2026-10-07 ~11:50 city 14 bus broke down at the Wren Bridge ramp; passengers waiting for a replacement under the bridge
    world_state.material_history.xp_halden_falsification :: R83: event XP 29 paid (R3, meaningful) — Eli's statement and Transit sheets exposed the falsified windows
    world_state.material_history.xp_imran_rescue :: R83: event XP 29 paid (R3, meaningful) — Imran's stone cut off and him rushed to hospital
    world_state.material_history.xp_lucy_rescue :: R83: event XP 12 paid (R2, minor) — Lucy Warren's stone removed, M thread, medical case
    world_state.material_history.xp_unit9_discovery :: R83: event XP 55 paid (R4, major) — Tanner Lane collection filmed, the Nissan tailed to Unit 9, leading to the seizure
    world_state.unowned_facts.hidden :: []
    world_state.unowned_facts.visible :: ["Most Ashfall residents treat demon stories as rumour, hoax, crime, or urban legend.", "In Morrow Ward Rin is known as someone who finds things and people; a few regulars know Rin handles stranger jobs.", "Municipal summaries show old-line outages without an agreed explanation; a PI may request public copies."]
```
