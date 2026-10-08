# SAVE — Ashfall: Hunter — R110

For `NEW ENGINE v5.0` · background `BACKGROUND_ASHFALL_HUNTER_v5_0.md`

# PART A — READABLE

## 1. Current state

```yaml
background_ref: {id: ashfall_hunter_gemini_combined_v4_4}
language: en
round:
  last_completed_round: 110
  saved_completed_round: 110
world_state:
  location: wexford_road
  time:
    season: autumn
    day_index: 24
    date: '2026-10-30'
    clock_minutes: 920
    daypart: afternoon
    precision: exact
  environment:
    weather: dry, cold
    place: Irene Calloway's house, Wexford Road; Frank's shed open; key to lock-up 6 found
    rin: ordinary clothes; blade in its bag
profile: full
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
    opened: 24
    credited: []
  progression:
    system: numeric_level_xp
    state:
      level: 4
      xp: 214
  condition:
    hp: 16
    mp: 16
    injuries: []
    fatigue: rested
    last_rest: night of Oct 29–30 at the workshop
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
  - item_id: clip_camera_2
    name: Clip-on night-mode camera (second one; with Rin)
    type: camera
    capability_domain: surveillance
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: varga_photos
    name: Photos of all 41 pages of Varga's 2004 notebook (on phone and laptop)
    type: documents
    capability_domain: records
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: clip_camera_1
    name: Clip-on night-mode camera (first one; returned by Mara)
    type: camera
    capability_domain: surveillance
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  - item_id: contractor_lanyard
    name: City contractor lanyard "CONTRACTOR — RISK MANAGEMENT" and Southport camera authorisation letter
    type: credential
    capability_domain: access
    condition: serviceable
    special_properties: []
    tier: T1
    abilities: []
  money:
    cash_and_accessible_funds: 5220
    currency: USD
    note: 'Plus $400 hidden in the wharf go-bag. Nothing owed either way. Retainer: $1,200 from the city on the
      1st of each month. Calloway job $350 on completion (Pike 15%).'
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
      imran: 'Imran Dalen: out of high-dependency; discharge delayed over the sleep-talk; neurologist Sat 31 Oct.'
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
      varga: 'Teodor Varga, ironworker (seventies, Ironside Lane, green door): in 2004 he built an iron cage round
        the patched masonry under the Red Line. His notebook (Rin photographed all 41 pages) shows the mark — the
        closed eye crossed by a line, same as Rin''s parent''s letter — labelled ''do not cover, do not touch'';
        bolted iron bands round it (''iron goes round, never across''); and a side drain with a 9 cm iron throat
        (''water must get out or the patch fails — keep it narrow''). He saw the sealer: tall, didn''t move like
        a man, its hand made the brick glow. He felt the Nightglass warm ''like that wall was''; says nobody living
        made it. He stares at Rin''s face and says nothing.'
      brannock: 'Brannock Freight: grey Nissan KT 72 VRN and white Transit van AF 19 KXT; only premises Unit 9;
        director Aidan Brannock lives in Saltgate.'
      lucy: Lucy Warren is eating again, no dreams, cold hands; Rosa gave her shifts back.
      forge: 'Varga''s forge: Saturdays 09:00 with Jo; next 31 Oct and 7 Nov.'
      mesh: Transit Safety fitted fine stainless 'vermin mesh' on the Southport outfall grate and the Mercer sump
        screen on Mon 26 Oct. The mesh crew found Rin's footbridge camera and it went to Mara; she says no more
        cameras on city property. Eli watches the Transit board for Mercer sump levels and any Mercer/Southport
        work orders; next Mercer low ~04:00 Wed 28 Oct.
      jobs: 'Pike''s jobs: Hollins kennels — a vixen and four cubs in the old well ($250, done); Demir''s Grocery
        — nephew Kemal and a friend used his key ($300, no bonus, done). Pike''s 15% ($82.50) owed.'
      city_paid: City paid $3,500 on Fri 23 Oct (Unit 9 $1,500 + Tanner Lane $500 + Halden job closed as delivered
        via the Southport footage $1,500). Expenses on receipts to come. Retainer proposed; terms being drafted.
      retainer: 'Signed a city retainer with Mara on Tue 27 Oct: $1,200 a month on the 1st, on call up to ten working
        days, $250/day beyond plus expenses, per-job fees; no entry to restricted premises without her written authorisation;
        reports only to her; 30 days'' notice. Expenses $288 paid Oct 30.'
      lantern: 'Mara is the Lantern Office''s field coordinator (her plus a part-time assistant). On Fri 30 Oct
        she read Rin the sealed part of LO-04: the 2004 breach under the Red Spur, two of four Lantern staff dead,
        a human-passing demon who sealed it and left, Varga''s cage, and ''Mrs A. Hale of Wexley with an infant
        said to be the entity''s''. Rin told her yes, he is that child. She keeps it off every record, says Rin
        must never enter 7-B or Mercer, and wants Ada told she knows. The weak point is the narrow drain throat
        through the patch; she''s seeking a way to get a grout crew into the outer gallery to close it.'
      mercer_alarm: 'Wed 28 Oct, Mercer low water: sump-screen pressure alarm 04:14–04:31 — something pushed at
        the new mesh from the wet side for 17 minutes. Jo: something that wants out; stand above and upwind. Mara
        now gets every alarm. Rin has authorised cameras at Southport (footbridge + far-bank lamp post) since 28
        Oct.'
      hollis: The shaven-headed man is Dean Hollis, Brannock's cousin; arrested 29 Oct for threatening Gallo; Brannock
        pays his lawyer (via Pike, from the sergeant).
      nadia: Waited for Nadia after her shift with orange chrysanthemums (26 Oct). Not tonight — she said ask her
        on a Sunday after she's slept; she's off Sundays. Don't tell Eli.
      calloway: 'Pike''s job: Irene Calloway, widow, Wexford Road. Frank (Red Line signal fitter 31 years, died
        June) rented lock-up 6 behind the Kettering parade for 30 years and never let her in. His notebook ''RL
        1958'' and ~400 phone photos show a huge model of the old Red Line, incl. Ferris sidings and a branch into
        a painted tunnel. Rin found the key taped inside his red toolbox lid. Opening it with Irene Sat 31 Oct 10:00.
        $350 + cake.'
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
    mara_quill: Mara Quill — Lantern Office; Rin's retainer; knows his parentage
    gallo_pawnbroker: Sal Gallo — Gallo Pawn & Loan, Lowfield; sells the stones (per Jo)
    orin_sable: Orin — "a dealer in old things"; phoned with an offer
    bellamy_doctor: the Bellamy Street doctor — Rin's GP contact
    lina_dalen: Lina Dalen — Imran's wife; night-diner server
    imran_dalen: Imran Dalen — recovering on a general ward
    agnieszka_wolak: Agnieszka Wolak — wharf landlady, cash room
    brannock_heavy: Dean Hollis — Brannock's cousin; arrested
    unit9_keeper: older man in a cardigan — keeps Unit 9
    ashfall_general_er: Ashfall General ER staff
    teodor_varga: Teodor Varga — ironworker; 2004 cage builder; forging Jo's blade
    court_runner: small slag creature — came out of the Southport grate
    police_sergeant_tip: police sergeant (Mara's contact)
    harun_demir: Harun Demir — Demir's Grocery; job done
    pat_okonjo: Pat Okonjo — Hollins kennels; job done
    irene_calloway: Irene Calloway — widow; lock-up job client
  factions:
    merrow_utility_solutions: Merrow Utility Solutions — infrastructure contractor
    ashfall_transit_authority: Ashfall Transit Authority — runs the Red Line
    ash_choir: the Choir — name on M's contact; moves the charms
    brannock_freight: Brannock Freight Services — Unit 9, Exchange Yard (the courier's car)
    lantern_office: the Lantern Office — Mara and a part-time assistant
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
    demir_grocery: Demir's Grocery, Corran Street
    wexford_road: Irene Calloway's house, Wexford Road
  quests:
    find_eli_voss: Find Eli Voss and get him somewhere safe — completed
    laundromat_job: Clear whatever is in the Suds & Spin basement; $400 via Pike — completed
    ash_beneath: Find out what happened to Eli Voss and who is sending crews below the Red Line — completed
    hollins_well: Why the Hollins dogs howl at the well — completed
    demir_stockroom: Who raids Demir's stockroom — completed
    calloway_lockup: Open Frank Calloway's lock-up with Irene and list it — active
  rights_obligations:
    workshop_lease: leasehold — Rin, Mrs Okafor
    pi_licence: licence — Rin, City of Ashfall
    voss_trace: contract — Rin, Nadia (completed, paid)
    laundromat_deal: brokered job — Rin, Pike, Rosa Fenn (closed, paid)
    eli_clinic_promise: informal promise — Rin, Nadia (closed, repaid)
    eli_case: contract — Rin, Eli (closed, paid $375)
    jo_cover_job: hire — Rin, Jo ($200 owed to Jo)
    city_contract: contract — Rin, City (closed; all paid; expenses pending)
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
    mara_retainer: retainer — Rin, City Risk Management (signed 27 Oct)
    varga_meeting: appointment — Rin, Varga (done 22 Oct)
    footage_custody: chain of custody — Rin to Mara (Tanner/Unit 9 footage)
    varga_blade: commission — Rin, Varga (Jo's blade; Saturdays)
    calloway_job: brokered job — Rin, Irene, Pike
    southport_camera_authority: authorisation — Rin, Mara (Southport cameras)
```

---

# PART B — CAPSULE

```yaml
capsule:
  save_round: 110
  encoding: plain
  delta_of: ashfall_hunter_gemini_combined_v4_4   # records equal to this BACKGROUND are not repeated
  supersedes_deltas_through: 110
  records:
    active_world_pressures.glass_spread.clock.due :: R100: 2026-10-30 — checks at 22 and 26 Oct found no wearer and no new stock (process stopped), no fill; holds at 4/6
    active_world_pressures.glass_spread.clock.filled :: R82: 4 — 2026-10-14 (3, Imran still wearing until 23:05 and stock moving; missed at the time) and 2026-10-18 (4, cell stock still moving via Mercer/Southport)
    active_world_pressures.glass_spread.state.current :: R96: no known wearer remains (Lucy's and Imran's stones removed; Gallo's stock and Unit 9 seized); cell stock limited to small Mercer parcels at low water — clock halted at 4/6 while nobody wears contaminated glass and no new stock circulates
    active_world_pressures.seal_erosion.clock.due :: R100: 2026-11-20 — extraction stopped; monthly pace from load cycling only
    active_world_pressures.seal_erosion.clock.filled :: R100: 2 — check due 2026-10-20 (Oct 6 + 2 weeks); extraction operated Oct 6–9 → one fill
    active_world_pressures.seal_erosion.state.current :: R96: extraction through 7-B stopped after 9 Oct (Halden shut 14 Oct); the unrepaired crack still under slow load cycling — next fill only ~2026-11-09 under the one-month pace, unless extraction or deliberate damage resumes
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
    continuity_status.player_corrected.92 :: R92: main quest ash_beneath answered by R67 but never checked out → marked completed; XP already paid at R83, none added (I8)
    continuity_status.player_corrected.100 :: R100: cash was reduced by Pike's unpaid cut at R95/R97 → corrected: cash $5,059 before dinner, $82.50 still owed to Pike
    continuity_status.round0_revisions.l_warren_gender :: R59: {field: npcs.l_warren.gender, was: unspecified, now: woman (about 23), reason: Rin has met her in person; background left it unset, round: 59}
    continuity_status.round0_revisions.names_completed :: R59: {field: npcs.l_warren.name / npcs.dale.name / npcs.vic.name, was: "L. Warren" / "Dale" / "Vic", now: Lucy Warren / Dale Brennan / Vic Moreno, reason: background left names incomplete; player asked to correct, round: 59}
    continuity_status.round0_revisions.nightglass_origin :: R17: {field: Nightglass Blade origin, was: unstated, now: Ada gave it to Rin at sixteen from the sealer parent's things; maker unknown to Rin and Ada, reason: player asked to commit it from the world, round: 17}
    factions.brannock_freight :: R65: {name: Brannock Freight Services Ltd, role: small courier, light freight and storage company at Unit 9, Exchange Yard, Old Exchange; inc. 2019; director Aidan Brannock; accounts tiny and late; moves Choir stock (OX-9 stencils), state: {public_status: ordinary small firm}, capability: {reach: a few vans and cars, one unit}}
    factions.brannock_freight.state.summons :: R82: Trading Standards summoned Brannock Freight after the Unit 9 seizure, 2026-10-19
    factions.brannock_freight.state.vehicles :: R85: grey Nissan KT 72 VRN and white Ford Transit van AF 19 KXT; only premises Unit 9; director Aidan Brannock, home address in Saltgate; no other leases
    locations.ashfall_general :: R72: {name: Ashfall General Hospital, emergency department, conditions: {surface: city hospital ER, ambulance bay, triage desk}, challenge_band: {min: 1, max: 2, basis: hospital}}
    locations.ashfall_general.conditions.er_record :: R73: ER notes 2026-10-15: prolonged exposure to an unknown warm pendant, removed 23:05, rigors 23:15; anonymised GP comparison report photographed from Rin's phone; doctor recorded Rin's name and PI licence as the man who brought him in and holds the object for the city
    locations.bellamy_clinic :: R11: {name: walk-in clinic, Bellamy Street, Morrow Ward, conditions: {surface: cash accepted, first name only, older doctor who does not ask how injuries happened; Rin has used it before}, challenge_band: {min: 1, max: 2, basis: ordinary clinic}}
    locations.canal_embankment.conditions.hut_3_door :: R2: hasp rusted through; Eli pulled the door shut and wedged it from inside on Oct 5; fresh claw scratches outside from the cinderling
    locations.canal_embankment.conditions.hut_3_lock :: R45: hut 3 door still chained with Rin's padlock; empty inside
    locations.city_risk_office.conditions.counter_3 :: R30: public hazard counter, Form RM-12 (name and contact optional); clerk logs reports to an analyst, flags urgent ones the same day; Q3 service interruption summary on the notice board lists three "cause undetermined" lines incl. Ferris Yard Sept 15 overnight
    locations.city_risk_office.conditions.counter_3_clerk :: R31: young clerk at Counter 3; did not recognise the word "cinderling"; routes plain pest reports to Environmental Health (1st floor, Room 4) and logs pest-caused hazards (fire, structural, wiring, gas, flooding) on RM-12 for an analyst
    locations.city_risk_office.conditions.rm12_0417 :: R32: hazard report RM-12 ref 26-1008-0417 filed by Rin 12:20 Oct 8: pest-caused fire hazard, multiple locations, example Kettering commercial basement, "cinderlings" drawn to dark-glass "lucky charms" being sold, carriers ill; Rin's card attached; flagged fire priority for an analyst today
    locations.demir_grocery :: R95: {name: Demir's Grocery, Corran Street, Morrow Ward, conditions: {surface: narrow corner shop; stockroom behind a strip curtain with one deadlocked alley door; shop camera faces the till; Rin's hidden clip camera on a high stockroom shelf behind a tea box facing the alley door from 11:00 Oct 23}, challenge_band: {min: 1, max: 2, basis: corner shop}}
    locations.demir_grocery.conditions.rin_camera :: R97: no longer holds — Rin took the camera back 07:00 Oct 25
    locations.exchange_yard :: R80: {name: Exchange Yard, Old Exchange, conditions: {surface: iron-gated cobbled courtyard of numbered roller-shutter trade units in the old merchants' quarter}, challenge_band: {min: 2, max: 5, basis: private trade yard}}
    locations.exchange_yard_unit9 :: R65: {name: Unit 9, Exchange Yard, Old Exchange, conditions: {surface: registered address of Brannock Freight Services; the OX-9 freight code}, challenge_band: {min: 2, max: 5, basis: private freight unit tied to the charm trade}}
    locations.exchange_yard_unit9.conditions.inside :: R80: steel shelving and stacked cardboard cartons stencilled OX-9, seen through the half-raised shutter 23:50 Oct 16
    locations.exchange_yard_unit9.conditions.seized :: R82: Trading Standards seized 3 cartons (72 charms) and a raw-glass crate with Merrow tape from Unit 9, 10:00 Oct 19; unit under notice
    locations.ferris_yard.conditions.night_guard :: R20: Bernie, depot night security, gatehouse at the main entrance; fence walk about hourly; coffee at the kiosk ~midnight (per the kiosk owner)
    locations.fishmarket_arcade :: R24: {name: Fishmarket Arcade, wharf district, conditions: {surface: covered market arcade; Haller's knife-grinding stall}, challenge_band: {min: 1, max: 3, basis: public market}}
    locations.gallo_pawn.conditions.gallo_home_emptied :: R79: Gallo's stones and batch notes taken from 14 Tanner Lane 23:20 Oct 16 by the courier and a shaven-headed man
    locations.hartley_allotments :: R29: {name: Hartley allotments, Kettering edge, conditions: {surface: council-closed allotments behind a broken gate, overgrown, collapsing tool sheds; nobody through in months, shed_box: Warren's worn charm in Rin's second locked steel cash box (key with Rin) under rotted seed trays in the last shed, 2026-10-08 10:45; unexposed}, challenge_band: {min: 1, max: 2, basis: abandoned allotments}}
    locations.hartley_allotments.conditions.shed_box :: R45: no longer holds — cash box with Warren's charm taken out by Rin 08:50 Oct 9
    locations.ironside_lane :: R86: {name: Ironside Lane, Lower Docks, conditions: {surface: old dockside street; Teodor Varga's ironworks}, challenge_band: {min: 1, max: 2, basis: quiet trade street}}
    locations.kettering_laundromat.conditions.back_alley :: R38: narrow alley behind the block: back door under one caged bulb, wheelie bins, garages opposite; exits to the side street and to the delivery yard of a closed carpet warehouse
    locations.kettering_laundromat.conditions.problem :: a cinderling nests beside a small cache of stock held by tenant L. Warren for a later Ash Choir collection; the cache gives off heat and scorch marks. Warren is not guaranteed to stay or hand it over.
    locations.lowfield.conditions.dalen_flat :: R70: 31B Rook Street, above the bakery; Lina gave Rin a spare key
    locations.marisols_grill :: R82: {name: Marisol's, Lowfield high street, conditions: {surface: busy little grill where Nadia is shift manager}, challenge_band: {min: 1, max: 2, basis: restaurant}}
    locations.mercer_pump.conditions.mesh :: R98: fine stainless mesh on the Mercer sump screen from 26 Oct
    locations.mercer_pump.conditions.oct10_traces :: R53: fresh black-red grit at the sump screen and disturbed baffle after the 04:00 Oct 10 low water
    locations.signal_box_pub :: R61: {name: The Signal Box, Ferris Road, conditions: {surface: railworkers' pub two streets from Ferris Yard; brown wood, timetables, darts, football on the telly}, challenge_band: {min: 1, max: 2, basis: neighbourhood pub}}
    locations.southport_outfall.conditions.mesh :: R98: fine stainless mesh bolted over the outfall grate bars from 26 Oct
    locations.southport_outfall.conditions.oct10_traces :: R53: wet three-toed prints on the outfall apron and a loosened grate fastener, morning of Oct 10
    locations.southport_outfall.conditions.rin_cameras :: R106: authorised: camera one under the footbridge rail aimed at the outfall grate and mesh; camera two high on a far-bank lamp post covering the footbridge and the outfall; both from 14:30 Oct 28; batteries ~2 days
    locations.wharf_room :: R78: {name: back room above the old chandlery, wharf, conditions: {surface: Mrs Wolak's cash room; Rin's bolt-hole, key on a fisherman's float; go-bag in the wardrobe with $400 sewn in the lining, spare clothes, delivery jacket, vest and clipboard, first-aid kit, torch, charger, food}, challenge_band: {min: 1, max: 2, basis: quiet lodging}}
    locations.wren_bridge_toll_hut :: R17: {name: old tollkeeper's hut, Wren Bridge approach ramp, Morrow Ward edge, conditions: {surface: brick hut with steel shutter, empty for decades, usually deserted; Rin knows it from courier work, now: city 14 bus broken down at the ramp foot 11:50 Oct 7, ~20 passengers waiting under the bridge, some sheltering at the hut}, challenge_band: {min: 1, max: 2, basis: abandoned roadside structure}}
    locations.wren_bridge_toll_hut.conditions.now :: R18: bus replaced 12:20; ramp empty again apart from the broken bus and its driver
    locations.wren_bridge_toll_hut.conditions.shard_box :: R18: Eli's shard in Rin's locked steel cash box (key with Rin), back corner behind a broken chair, shutter bolted as found, 2026-10-07 12:25; unexposed
    locked_case_truths.calloway_lockup :: R107: {cause: Frank Calloway kept a large model railway layout of the 1950s Red Line he built over thirty years, plus a biscuit tin of savings bonds and letters; he hid the key taped inside the lid of his toolbox at home, state: {lockup: behind the Kettering parade, number 6, padlocked}, evidence: {key: taped inside the lid of Frank's red toolbox in Irene's shed, landlord: has no spare, neighbours: the next lock-up tenant heard "trains" through the door at weekends}, discovered_information: {}}
    locked_case_truths.calloway_lockup.discovered_information :: R110: {key: Rin found it taped inside the red toolbox lid in the shed, 2026-10-30; notebook: "RL 1958", track drawings incl. Ferris approach and spur junction; phone: ~400 photos of a large Red Line model layout incl. Ferris sidings and a branch into a painted tunnel; rent receipts lock-up 6 since 1995}
    locked_case_truths.civic_collision.discovered_information.crew_moved :: R82: via Eli/Tomas 2026-10-17: Merrow's night crew moved to Kettering depot; Rusk still off sick and unseen
    locked_case_truths.civic_collision.discovered_information.halden_suspended :: R74: Mara told Rin 2026-10-15: Transit Safety suspended Merrow's after-hours Halden access 16:00 Oct 14; Rusk phoned in sick to his compliance meeting
    locked_case_truths.civic_collision.discovered_information.kiosk_account :: R20: kiosk owner told Rin 2026-10-07: back half of the yard goes dark 2–3 nights a week, Merrow vans in Halden 01:00–02:00, Transit staff locked out for "Merrow works"
    locked_case_truths.civic_collision.discovered_information.lantern_office :: R108: Mara revealed the Lantern Office (her and a part-time assistant) to Rin 2026-10-30
    locked_case_truths.civic_collision.discovered_information.mara_contact :: R36: Mara Quill (City Risk Management) took Rin's report; reacted to Ferris Yard / Halden Lane; asked for evidence and a meeting
    locked_case_truths.civic_collision.discovered_information.mara_offer :: R47: Mara told Rin 2026-10-09 that Merrow blames aging equipment for Ferris, that she requested Transit's original sign-out sheets for Sept–Oct, and offered $750 for the report and custody of the charms, $1,500 for a documented Halden window from outside
    locked_case_truths.civic_collision.discovered_information.mara_tipoff :: R60: Mara reads the on-time window after Rin's call with Orin as a tip-off, 2026-10-11
    locked_case_truths.civic_collision.discovered_information.public_summary :: R30: Rin read the posted Q3 summary 2026-10-08: three "cause undetermined" interruptions incl. Ferris Yard Sept 15
    locked_case_truths.civic_collision.discovered_information.sheets_verdict :: R67: Mara confirmed 2026-10-14: Transit's original sheets show 1-hour windows; Merrow's copies show 2–3 hours with a non-existent Transit code; she is asking Transit Safety to suspend Merrow's after-hours Halden access and writing to Merrow compliance
    locked_case_truths.civic_collision.discovered_information.yard_gossip :: R76: via Eli and Tomas 2026-10-15: Halden locked after hours, Merrow night crew removed, audit talk, Rusk off sick
    locked_case_truths.demir_stockroom :: R94: {cause: Demir's nephew Kemal, 19, copies the stockroom key he's trusted with and lets in a school friend who sells the cigarettes and oil; no break-in because they use the key, state: {thefts: three this month, next likely Saturday night}, evidence: {key: a fresh brass copy on Kemal's ring that doesn't match the original's wear, cctv: the shop's camera faces the till not the stockroom door, friend: sells cut-price cigarettes at the Corran Street bus shelter}, discovered_information: {}}
    locked_case_truths.demir_stockroom.discovered_information :: R96: {footage: 00:40 Oct 25 two young men entered by key, took cigarettes, oil, coffee in a sports bag in four minutes; the one with the key is Kemal (clear face, gold chain); the lookout skinny in a grey tracksuit; door relocked with the key}
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
    locked_case_truths.glass_trade.evidence.warren :: L. Warren at Suds & Spin wore a charm for nine days and hides cell stock; a scheduled collector may move it. Warren can flee, bargain or be endangered before Rin arrives.
    locked_case_truths.hale_bloodline.discovered_information.ada_2004 :: R55: Ada told Rin 2026-10-10: his parent, a being from below who broke from a "court", sealed something under the Red Line in autumn 2004 after Rin's birth that spring; gave Rin to Ada and vanished; the blade was the parent's; letters in a deposit box at Harland's Bank, Wexley
    locked_case_truths.hale_bloodline.discovered_information.blade_no_ward :: R71: Rin learned 2026-10-14 the Nightglass has no warding or healing effect when laid on a person; it only bites what it strikes
    locked_case_truths.hale_bloodline.discovered_information.haller_exam :: R42: Haller judged the Nightglass not forged, uniform, glass-dark, ~20 years old by the grip wear, and would not treat it, 2026-10-08
    locked_case_truths.hale_bloodline.discovered_information.haller_lead :: R24: Jo named Dutch Haller (blade treater, not a forger) and says no one she knows could make Rin's blade, 2026-10-07
    locked_case_truths.hale_bloodline.discovered_information.lo04 :: R108: LO-04 names Mrs A. Hale of Wexley as witness with an infant said to be the sealer's; Mara has linked it to Rin
    locked_case_truths.hale_bloodline.discovered_information.mara_knows :: R109: Rin confirmed to Mara 2026-10-30 that he is the sealer's child; she will keep it off every record and wants Ada told
    locked_case_truths.hale_bloodline.discovered_information.parent_letter :: R62: Rin read his parent's letter 2026-10-12 (signed only with a sigil like a closed eye crossed by a line): the parent was of the court below and left it; after Rin's birth they sealed the old way under the Red Line with their own mark; the mark holds while nobody takes from it, weakens if dug at; it knows the parent's blood and Rin's; if Rin calls up his power near the old stones or near the black glass that grows from them, those below feel the blood is alive and close, though not his name or face; walking right up to the seal wakes it regardless; the blade is made from what the parent was and won't break against them; the parent doesn't know if Rin could mend the mark
    locked_case_truths.hale_bloodline.discovered_information.varga_blade :: R92: Varga says the Nightglass is warm to the hand like the wall he saw glow in 2004, and that nobody living in the city made it
    locked_case_truths.hale_bloodline.discovered_information.varga_witness :: R91: Varga saw the sealer in 2004 — tall, didn't move like a man, its hand made the brick glow — and stared at Rin's face without comment
    locked_case_truths.hollins_well :: R94: {cause: a vixen and four half-grown cubs denning in a collapsed side tunnel of the dry well; they come out to the field ~02:00 to hunt; the dogs hear and smell them, state: {den: active}, evidence: {tracks: fox prints and droppings around the well cap, smell: musky fox smell at the well, sightings: cubs visible on a night camera at the field edge ~02:00}, discovered_information: {}}
    locked_case_truths.hollins_well.discovered_information :: R95: {den: Rin filmed the vixen and four cubs leaving and returning to the collapsed well hollow 01:55–02:15 Oct 23; told Pat}
    locked_case_truths.old_seal.discovered_information.ada_2004 :: R55: Ada witnessed the end of the 2004 sealing under the Red Line; describes the thing below as old and nearly out
    locked_case_truths.old_seal.discovered_information.drain_repair :: R109: Mara 2026-10-30: the bleed-drain throat can be closed from the outer gallery with iron and grout by an ordinary crew; she is looking for a way in
    locked_case_truths.old_seal.discovered_information.haller_lore :: R41: Haller told Rin 2026-10-08: "ember glass" softens nearby steel edges, draws vermin and bigger things; old-trade talk says it sweats out of the walls at old bricked-up breaches where heat comes up from below
    locked_case_truths.old_seal.discovered_information.haller_saying :: R85: Haller 2026-10-19: raw fist-sized ember glass is straight out of a wall; old-trade saying "what you take from below, below comes looking for"; keep it cold, closed, away from people, never sold back
    locked_case_truths.old_seal.discovered_information.lo04 :: R108: Mara read Rin LO-04 2026-10-30: 2004 breach under the Red Spur; two Lantern staff died; a human-passing demonic entity sealed it with its mark and left; Varga built the iron cage
    locked_case_truths.old_seal.discovered_information.mara_2004_file :: R90: Mara told Rin 2026-10-22 she has an old 2004 file with a sealed part never opened for lack of physical proof; she is requesting it now
    locked_case_truths.old_seal.discovered_information.parent_letter :: R62: the seal holds while nobody takes from it; it weakens if dug at; its mark is the sigil on the letter
    locked_case_truths.old_seal.discovered_information.runner_seen :: R89: Rin saw on camera a small slag creature passing through the Southport grate at low water to meet the Choir courier, 2026-10-21
    locked_case_truths.old_seal.discovered_information.varga_lead :: R86: Mara named Teodor Varga, ironworker in Ironside Lane, who did city contract work in 2004 making iron fittings for a job under the Red Line; she'll ask him to see Rin
    locked_case_truths.old_seal.discovered_information.varga_notebook :: R91: Varga's 2004 notebook (Rin has photos of every page): measured drawings of the patched masonry with the mark (a closed eye crossed by a line — the same sigil as Rin's parent's letter) labelled "do not cover, do not touch"; a ring of bolted iron bands set round it ("iron goes round, never across"); a drain through the side of the patch with a 9 cm iron throat ("water must get out or the patch fails — keep it narrow")
    locked_case_truths.old_seal.discovered_information.varga_photos :: R92: Rin photographed all 41 pages of Varga's 2004 notebook twice, 2026-10-22
    locked_case_truths.red_line_case.discovered_information.clean_window :: R56: Rin watched the booked window 00:30–01:30 Oct 11 run exactly to time with no vans or crates; every earlier window in Eli's notes ran 1–2 hours over
    locked_case_truths.red_line_case.discovered_information.eli_account :: R5: Eli told Rin 2026-10-06: extended windows, Merrow van into Halden Lane, door 7-B into the sealed spur, crates carried out, Jonas Rusk present, took a shard, chased, fell on service stairs, phone off; blurry photo of something on the far platform
    locked_case_truths.red_line_case.discovered_information.embankment_signs :: R2: Rin found cinderling tracks, burned rat, and hut 3 wedged from inside, with someone silent inside, 2026-10-06 20:45
    locked_case_truths.red_line_case.discovered_information.jo_read :: R106: Jo's view 2026-10-28: seventeen minutes of pushing means something that wants out, not a scared small thing; not big, or careful; stand above and upwind with your back to something solid
    locked_case_truths.red_line_case.discovered_information.mercer_alarm :: R104: via Eli 2026-10-28: Mercer sump screen pressure alarm 04:14–04:31 at low water — something pressed on the new mesh from the wet side for 17 minutes
    locked_case_truths.red_line_case.discovered_information.mercer_low_forecast :: R88: Eli's telemetry reading 2026-10-20: Mercer sump expected low ~03:00–05:00 Wed 21 Oct
    locked_case_truths.red_line_case.discovered_information.mercer_route_eli :: R85: Eli told Rin 2026-10-19 that the Red Spur's old drainage runs to the Mercer flood pump, with service stairs into old galleries once linked to the spur's outer galleries, and overflow to the Southport outfall
    locked_case_truths.red_line_case.discovered_information.next_window :: R50: Rin knows the next Ferris back-half isolation is booked night of Oct 10–11, 00:30–01:30, per Eli's roster app
    locked_case_truths.red_line_case.discovered_information.phone_location :: R1: Rin saw the locator via Nadia 2026-10-06 20:00; area only, not hut
    locked_case_truths.red_line_case.discovered_information.runner_footage :: R89: Rin's Southport camera 04:06–04:13 Wed 21 Oct: the courier waited at the outfall; a cat-sized slag creature with glowing cracks came out through the grate at low water, gave him a tiny red glinting chip, took a folded paper message wrapped round something, and went back through the grate
    locked_case_truths.red_line_case.discovered_information.rusk_footage :: R62: Rin's camera filmed Rusk at the Halden gate 16:20 Oct 11 in a white Merrow pickup, checking the service door padlock; face clear in two frames, plate readable; the 00:30–01:30 window empty; clips saved in three places
    locked_case_truths.red_line_case.discovered_information.spur_map :: R1: Rin has Eli's map with RED SPUR (CLOSED) circled
    locked_case_truths.red_line_case.discovered_information.vermin_mesh :: R90: Mara is asking Transit Safety to fit fine vermin mesh on the Southport outfall grate and the Mercer sump screen, 2026-10-22
    npcs.ada_hale.knowledge.facts.nightglass_origin :: R17: the Nightglass Blade was left with infant Rin by the sealer parent in 2004; Ada kept it and gave it to Rin at sixteen saying only that it came from someone who'd want Rin to have it; she does not know who forged it
    npcs.ada_hale.knowledge.facts.rin_case :: R55: Rin told her 2026-10-10 everything: Eli, the cinderlings, the charms and the Choir, Haller's ember glass, the city contract, door 7-B and the sealed Red Spur, a figure on the far platform, the man calling himself Orin, and his plan to watch Halden tonight
    npcs.ada_hale.knowledge.facts.rin_glass_call :: R19: Rin described warm black glass with a red core that draws small demons, 2026-10-07 afternoon; would not say where it came from
    npcs.ada_hale.knowledge.facts.rin_promise :: R63: Rin promised 2026-10-12 not to call up his power near the stones
    npcs.ada_hale.relationships.rin_hale.attitude :: R55: loves Rin; frightened; relieved to have told him
    npcs.ada_hale.state.due :: R107: 2026-11-01 18:00 Sunday call
    npcs.ada_hale.state.plan :: R63: calls with Rin Wednesday and Sunday; ready to come back if he needs her
    npcs.ada_hale.state.position :: R63: her flat in Wexley, from 15:00 Oct 12
    npcs.ada_hale.state.status :: R107: Wednesday call 18:00 Oct 28: Rin told her about the retainer; proud
    npcs.agnieszka_wolak :: R78: {name: Agnieszka Wolak, job: lets four rooms above a closed chandlery on the wharf, cash by the week, no ID, belongs: [], gender: woman, character: sixty-five, thin, smokes at the window; temper roll 13 (ordinary), state: {position: wharf rooms above the old chandlery, status: holding her back room for Rin for a month, paid $150 cash 2026-10-16, plan: keep the room; no questions, due: 2026-11-16 room hold ends}, relationships: {rin_hale: {tie: landlady from his courier days, attitude: neutral, mildly fond, credit: [never dripped on her stairs], grievance: [], believes_identity: the polite courier boy}}, capability: {overall_level: 1}}
    npcs.ashfall_general_er :: R73: {name: Ashfall General ER staff, job: emergency department, belongs: [], gender: mixed, character: busy, professional, state: {position: ashfall_general, status: treating Imran; asked about the object, noted Rin's details, plan: treat; may ask the city about the object, due: ordinary}, capability: {overall_level: 2}}
    npcs.bellamy_doctor :: R59: {name: the Bellamy Street doctor (unnamed), job: GP at the Bellamy Street walk-in clinic, open Sundays till 14:00, belongs: [], gender: man, character: older, tired, cardigan; thorough; asks no questions he doesn't need; temper roll 14 (ordinary), state: {position: bellamy_clinic, status: examined Lucy Warren 10:40 Oct 11, plan: written report with blood results for Rin and Lucy, due: 2026-10-14 bloods back; Lucy's follow-up}, relationships: {rin_hale: {tie: doctor Rin uses, attitude: neutral, trusting, credit: [], grievance: [], believes_identity: PI who brings in odd cases}}, knowledge: {facts: {warren_exam: low core temperature, low BP, fast pulse, mild dehydration, recent weight loss, a healing walnut-sized thermal injury below the throat consistent with long contact with something warm}}, capability: {overall_level: 3}}
    npcs.bellamy_doctor.relationships.rin_hale.attitude :: R72: neutral turning wary; suspicious
    npcs.bellamy_doctor.state.due :: R66: 2026-10-28 Lucy's follow-up
    npcs.bellamy_doctor.state.status :: R72: refused to open at midnight 23:35 Oct 14 (NO, AND); told Rin to take Imran to Ashfall General; now suspicious of what Rin is mixed up in
    npcs.brannock_heavy :: R79: {name: shaven-headed man (unnamed), job: Brannock/Choir muscle; collected Gallo's stones and notes, belongs: [ash_choir], gender: man, character: short, wide, shaven head, leather jacket, swaggering; kicks gates, jabs people; temper roll 15 (difficult — a bully), state: {position: in the grey Nissan toward the ring road, 23:25 Oct 16, status: took Gallo's stones and batch notes, plan: deliver them to Unit 9 or M, due: 2026-10-17 00:00}, capability: {overall_level: 4}}
    npcs.brannock_heavy.name :: R109: Dean Hollis
    npcs.brannock_heavy.state.due :: R109: on court dates
    npcs.brannock_heavy.state.position :: R80: inside Unit 9, Exchange Yard, from 23:50 Oct 16
    npcs.brannock_heavy.state.status :: R109: arrested 2026-10-29 for threatening Gallo; Brannock paying his lawyer
    npcs.choir_contact_m :: R28: {name: M (Choir), job: Ash Choir cell stock contact; arranges holds and pickups by text, belongs: [ash_choir], gender: unknown, character: terse, unknown in person, state: {position: unknown, status: told Warren 2026-10-07 11:51 to stay put and be at the back door at 22:00, plan: send the courier to Suds & Spin 2026-10-08 22:00 to talk to Warren about the lost stock; reports to the cell and Orin's people, due: 2026-10-08 22:00}, knowledge: {facts: {loss: Warren says Pike's hunter Rin Hale of Hale Workshop took the box}}, capability: {overall_level: unknown}}
    npcs.choir_contact_m.state.due :: R104: on Orin's instruction
    npcs.choir_contact_m.state.plan :: R57: drop Suds & Spin as a holding point; use other holders; report to Orin's people
    npcs.choir_contact_m.state.status :: R104: 05:30 Oct 28 courier reported nothing came through at Southport; passed to Orin
    npcs.choir_courier :: R28: {name: hooded courier, job: picks up and drops off for M, belongs: [ash_choir], gender: man, character: big coat, hood always up; unknown, state: {position: unknown, plan: come to the Suds & Spin alley back door 2026-10-08 22:00 for M, due: 2026-10-08 22:00}, capability: {overall_level: unknown}}
    npcs.choir_courier.capability.description :: R40: forties, broad face, flattened nose, scar through one eyebrow
    npcs.choir_courier.capability.overall_level :: R39: 3
    npcs.choir_courier.character :: R39: big, slow, heavy-shouldered, long dark hooded parka with fur trim, stubble; flat local voice; temper roll 6 (ordinary)
    npcs.choir_courier.state.due :: R104: on M's next instruction
    npcs.choir_courier.state.plan :: R100: done delivering to Unit 9 (Oct 16); now Orin's watcher at the Southport outfall for the next low water
    npcs.choir_courier.state.position :: R80: inside Unit 9, Exchange Yard, Old Exchange, from 23:50 Oct 16
    npcs.choir_courier.state.status :: R104: waited at the Southport outfall 03:45–05:00 Oct 28; nothing came; reported to M
    npcs.choir_courier.state.vehicle :: R65: dark grey Nissan KT 72 VRN, registered keeper Brannock Freight Services Ltd, Unit 9, Exchange Yard, Old Exchange
    npcs.court_runner.state.due :: R104: 2026-10-28 06:00 reports
    npcs.court_runner.state.plan :: R104: report the blocked route to the Surveyor
    npcs.court_runner.state.status :: R104: 03:50–04:31 Oct 28 at Mercer low water passed the bleed-drain slit into the sump; blocked by the new mesh on the sump screen; pressed at it for 17 minutes (Transit screen alarm 04:14–04:31); could not reach the culvert; went back through the slit
    npcs.dale.name :: R59: Dale Brennan
    npcs.dale.state.due :: R53: when Rusk calls him back to work
    npcs.dale.state.status :: R53: told by Rusk 21:00 Oct 9: no runs for two weeks
    npcs.dutch_haller :: R24: {name: Dutch Haller, job: knife-grinder at a stall in the Fishmarket Arcade by the wharf; at night treats steel for a few hunters and sells occult odds and ends, belongs: [], gender: man, character: unknown (not yet met), state: {position: Fishmarket Arcade stall, status: working his trade, plan: ordinary trade; night work only for vouched clients, due: ordinary routine}, knowledge: {facts: {}}, capability: {overall_level: unknown until met}}
    npcs.dutch_haller.capability.overall_level :: R34: 3
    npcs.dutch_haller.character :: R34: big, slow, unhurried, burn-scarred hands; cautious; temper roll 5 (ordinary)
    npcs.dutch_haller.knowledge.facts.ember_glass :: R41: calls it "ember glass"; ~2011 a hunter brought him a thumbnail chip to set in a pommel; in three days nearby steel edges went soft as if over-tempered, rats got past his salt, something bigger tried his back door on the third night; he threw it off the pier; old trade talk says it grows where heat comes up from below at old breaches, places bricked shut long ago, sweating out of the walls; he doesn't know if that's true
    npcs.dutch_haller.knowledge.facts.nightglass_seen :: R42: Rin showed him the Nightglass Blade 2026-10-08; he could not identify its make; wants to meet whoever made it
    npcs.dutch_haller.knowledge.facts.raw_glass :: R85: Rin described the seized raw crate to him 2026-10-19
    npcs.dutch_haller.relationships.rin_hale :: R34: {tie: hunter asking trade talk, attitude: neutral, wary, credit: [], grievance: [], believes_identity: hunter Kestrel knows}
    npcs.dutch_haller.relationships.rin_hale.attitude :: R43: neutral; a paying customer
    npcs.dutch_haller.state.due :: R100: none pending — ordinary trade; night work after 21:00 on request
    npcs.dutch_haller.state.plan :: R44: cure and edge two treated 4-inch blades for Rin; ordinary trade by day
    npcs.dutch_haller.state.status :: R43: honed the nick out of the Nightglass Blade 23:30 Oct 8 for $20; quoted Rin: treated 4-inch fixed blade $300 (half up front, three-day cure, ready Sunday 2026-10-11); untreated legal lock-knife $45 tonight; second treated blade another $300 and three days
    npcs.eli_voss.knowledge.facts.mercer_route :: R85: told Rin 2026-10-19: the old spur drained south to the Mercer flood pump (still working); service stairs from the pump room down into old drainage galleries that once connected to the spur's outer galleries; overflow runs by culvert to the Southport outfall on the canal; often flooded, dangerous pumps; never been down
    npcs.eli_voss.knowledge.facts.mesh_done :: R99: Transit Safety completion note 26 Oct: vermin mesh fitted at the Southport outfall and the Mercer sump screen; no other orders yet
    npcs.eli_voss.knowledge.facts.next_window :: R50: Transit roster shows the Ferris back-half isolation booked Sat 10 Oct 00:30–01:30 (night of Oct 10–11); Eli expects the lights off at 00:30 and the vans after
    npcs.eli_voss.knowledge.facts.rin_warning :: R87: Rin told him 2026-10-20 someone may be using the Mercer–Southport route and a camera is on it; keep away
    npcs.eli_voss.knowledge.facts.shard_draws :: R5: Rin told him the shard is what draws the creatures
    npcs.eli_voss.knowledge.facts.telemetry :: R87: the yard office has a live Transit telemetry screen showing every pump station's sump level, including Mercer; he looks at it every morning
    npcs.eli_voss.knowledge.facts.yard_gossip :: R76: via Tomas 2026-10-15: Halden locked down after hours; Merrow's night crew removed from the Halden building by Transit Safety Oct 14; talk of an audit; Rusk off "sick"; Merrow staff tense
    npcs.eli_voss.relationships.rin_hale :: R5: {tie: PI hired by Nadia, attitude: relieved, still wary, credit: [killed the creature at his door], grievance: [], believes_identity: PI sent by Nadia}
    npcs.eli_voss.relationships.rin_hale.attitude :: R77: grateful, loyal; would help again
    npcs.eli_voss.relationships.rin_hale.credit :: R8: [found him and brought him safe, 2026-10-06]
    npcs.eli_voss.state.carries :: R7: phone (off); no longer the shard
    npcs.eli_voss.state.due :: R105: on the next Mercer low water (read off the board) and his daily texts
    npcs.eli_voss.state.hp :: R10: 12 — full night's rest
    npcs.eli_voss.state.plan :: R105: watch the Mercer sump telemetry live at the next low water with an alert set on the screen alarm; text Rin if it fires again; stay at his desk
    npcs.eli_voss.state.position :: R19: Nadia's flat, Lowfield, from ~20:00 Oct 7
    npcs.eli_voss.state.routines.telemetry :: R99: Eli texts Rin the Mercer sump level and any Mercer/Southport work orders or access requests each morning and at lunch
    npcs.eli_voss.state.status :: R104: saw the Mercer sump screen pressure alarm 04:14–04:31 Oct 28 on the telemetry board (auto-cleared, no work order); texted Rin 08:05
    npcs.embankment_cinderling :: R2: {name: cinderling (Canal embankment), job: lesser demon scavenger, belongs: [], gender: none, character: hungry, cautious, fixated on the shard's heat, state: {position: weeds ~20 m from hut 3, status: watching Rin, hp: 6, plan: keep distance while Rin is there; return to scratching at hut 3 once Rin leaves; withdraw if hurt, due: when Rin leaves the embankment or closes within a few metres}, drives: {wants: [the shard, warmth, food], fears: [strong light, superior force]}, capability: {overall_level: 2, size: small}}
    npcs.embankment_cinderling.state.plan :: R3: no longer holds — dead
    npcs.embankment_cinderling.state.status :: R3: killed by Rin 2026-10-06 20:47; body cooled to inert slag on the embankment
    npcs.gallo_pawnbroker.state.due :: R109: on Trading Standards' decision or a police witness request
    npcs.gallo_pawnbroker.state.plan :: R100: (NO, BUT) hired a lawyer; silent for now; will cooperate only if charged
    npcs.gallo_pawnbroker.state.status :: R109: Trading Standards interview 10:00 Oct 30 with his lawyer; said nothing; case continues; Hollis's arrest for threatening him makes him more frightened, not less
    npcs.harun_demir :: R94: {name: Harun Demir, job: owner, Demir's Grocery, Corran Street, Morrow Ward, belongs: [], gender: man, character: unknown (not met), state: {position: Demir's Grocery, status: stockroom raided at night three times this month, no break-in marks; cigarettes, tins, good olive oil taken; suspects a nephew, plan: hire someone through Pike for a name, due: on Rin's acceptance}, capability: {overall_level: 1}}
    npcs.harun_demir.character :: R95: heavy, anxious, fifties, reading glasses on his head; temper roll 7 (ordinary)
    npcs.harun_demir.relationships.rin_hale :: R95: {tie: client via Pike, attitude: anxious, hopeful, credit: [], grievance: [], believes_identity: PI}
    npcs.harun_demir.relationships.rin_hale.attitude :: R97: grateful, sad; will call him first next time
    npcs.harun_demir.relationships.rin_hale.credit :: R97: [found the thief fast and clean, 2026-10-25]
    npcs.harun_demir.state.due :: R97: none pending
    npcs.harun_demir.state.plan :: R97: deal with Kemal in the family; change the locks
    npcs.harun_demir.state.status :: R109: stockroom flooded by the Corran Street main burst Oct 30; Rin helped lift rice sacks
    npcs.imran_dalen.state.carries :: R70: no stone
    npcs.imran_dalen.state.due :: R107: 2026-10-31 11:00 neurology review; discharge decision after
    npcs.imran_dalen.state.plan :: R70: none — incapacitated by withdrawal
    npcs.imran_dalen.state.position :: R85: Ashfall General, general ward
    npcs.imran_dalen.state.status :: R107: discharge delayed (NO, BUT) — bloods good, but kept two more nights over the sleep-talk; neurologist Saturday; awake, impatient, asking for his cab
    npcs.irene_calloway :: R107: {name: Irene Calloway, job: retired; widow, Wexford Road, belongs: [], gender: woman, character: unknown (not met), state: {position: her house, Wexford Road, status: husband Frank died June 2026; his Kettering lock-up must be cleared by end of November; key lost; wants someone decent to open and list it with her, plan: hire through Pike, due: on Rin's acceptance}, capability: {overall_level: 1}}
    npcs.irene_calloway.character :: R110: small, upright, white hair set in waves, cardigan buttoned to the neck; assessing, dry, unsentimental; temper roll 16 (ordinary)
    npcs.irene_calloway.knowledge.facts.frank_trains :: R110: Frank spent thirty years building a model of the Red Line (phone photos, notebook "RL 1958")
    npcs.irene_calloway.relationships.rin_hale :: R110: {tie: hired through Pike, attitude: neutral, approving, credit: [found Frank's key], grievance: [], believes_identity: Pike's decent young man}
    npcs.irene_calloway.state.due :: R110: 2026-10-31 10:00 at lock-up 6, Kettering parade
    npcs.irene_calloway.state.plan :: R110: open lock-up 6 with Rin in daylight Saturday 2026-10-31 10:00 and list its contents; bring cake
    npcs.irene_calloway.state.status :: R110: told Rin Frank's history (Red Line signal fitter 31 years, retired 2009; lock-up 6 since 1995, weekends; died June 2026, heart); let Rin search his bureau, phone and shed; holds the lock-up key Rin found
    npcs.jo_kestrel.knowledge.facts.choir_thread :: R33: Rin sent her 2026-10-08 photos of the M (Choir) thread: paid holding, "keep one for yourself, good luck charm", pickup Oct 8 22:00 back door, Warren naming Rin; holder sick after wearing one
    npcs.jo_kestrel.knowledge.facts.mercer_alarm :: R106: Rin told her 2026-10-28 about the 17-minute pressure alarm on the Mercer sump mesh at low water
    npcs.jo_kestrel.knowledge.facts.rin_blade :: R24: has seen Rin's blade in use; knows no maker who could make it; wants to know if Rin finds out
    npcs.jo_kestrel.knowledge.facts.rin_claims :: R33: Rin admitted the receipt was a lie 2026-10-08; the nest claim stands
    npcs.jo_kestrel.relationships.orin_sable :: R19: {tie: client through a hunting-work contact (did not meet him), attitude: businesslike, credit: [paid half up front], grievance: [], believes_identity: a dealer recovering his client's antiques}
    npcs.jo_kestrel.relationships.orin_sable.attitude :: R33: done with him; feels used
    npcs.jo_kestrel.relationships.orin_sable.grievance :: R23: [story about "stored antiques" looks false to her, 2026-10-07]
    npcs.jo_kestrel.relationships.rin_hale.attitude :: R93: friendly; touched; a real ally now
    npcs.jo_kestrel.relationships.rin_hale.credit :: R93: [Rin pulled her out of a flooded culvert two years ago; warned her off a dirty client with real evidence, 2026-10-08; commissioned an iron blade for her, 2026-10-22]
    npcs.jo_kestrel.relationships.rin_hale.grievance :: R40: [Rin took and finished a job she had spent a week on last spring, and got paid for it; lied to her face about a receipt, admitted it 2026-10-08]
    npcs.jo_kestrel.relationships.teodor_varga :: R96: {tie: making her a blade, attitude: impressed — "the real thing", credit: [forging her a blade], grievance: [], believes_identity: an old master ironworker}
    npcs.jo_kestrel.state.due :: R106: 2026-10-31 09:00 forge; on Rin's call for a watch night
    npcs.jo_kestrel.state.plan :: R106: on call on Rin's watch nights if he asks; forge Saturday 31 Oct 09:00
    npcs.jo_kestrel.state.position :: R61: behind the shut tyre shop off Ferris Road, 21:06 Oct 11, holding Rin's camera
    npcs.jo_kestrel.state.status :: R106: declined to sit the Southport watch (NO, BUT); will be on call ten minutes out on Rin's watch nights for $100 a night
    npcs.jonas_rusk.state.due :: R100: 2026-11-02 10:00 Merrow investigation interview; immediately on police contact or Orin's call
    npcs.jonas_rusk.state.plan :: R74: stall compliance with sickness and "clerical error"; keep Orin's name out of it; may fold later if the audit and danger outweigh the pay
    npcs.jonas_rusk.state.status :: R100: (NO, BUT) attended the 19 Oct compliance meeting with a union rep, blamed a clerical error; suspended on pay pending investigation; still silent on Orin
    npcs.kiosk_owner :: R20: {name: kiosk owner (Ferris Yard corner, unnamed), job: runs the night coffee kiosk at Ferris Yard, belongs: [], gender: man, character: older, chatty when bored, crossword habit; temper roll 9 (ordinary), state: {position: night kiosk, Ferris Yard corner, status: on his night shift, plan: run the kiosk till morning, due: ordinary routine}, relationships: {rin_hale: {tie: customer, attitude: neutral, friendly, credit: [], grievance: [], believes_identity: contractor doing signal checks}}, knowledge: {facts: {vans: Merrow vans come down Halden Lane around 01:00–02:00 on nights the back half of the yard goes dark; 2–3 nights a week lately; Transit staff complain about lockouts for "Merrow works", guard: Bernie, night security, walks the fence about hourly and buys coffee around midnight}}, capability: {overall_level: 1}}
    npcs.l_warren.gender :: R59: woman
    npcs.l_warren.name :: R59: Lucy Warren
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
    npcs.lina_dalen.knowledge.facts.bellamy :: R69: Rin gave her the Bellamy Street clinic address; stone must never be brought inside
    npcs.lina_dalen.knowledge.facts.imran_schedule :: R69: Imran sleeps until ~04:00 and starts his cab shift at 05:30; never takes the stone off, not to shower or sleep
    npcs.lina_dalen.knowledge.facts.rin_number :: R74: Rin's card and number, 2026-10-15
    npcs.lina_dalen.relationships.rin_hale :: R68: {tie: the investigator who asked her, attitude: hopeful, desperate, credit: [], grievance: [], believes_identity: a PI looking into the stones}
    npcs.lina_dalen.relationships.rin_hale.attitude :: R85: grateful; trusts him fully
    npcs.lina_dalen.relationships.rin_hale.credit :: R76: [took the stone off Imran and got him to hospital, 2026-10-14]
    npcs.lina_dalen.state.due :: R85: none pending; on Rin's contact
    npcs.lina_dalen.state.plan :: R69: let Rin in when he says; get Imran to the Bellamy doctor once the stone is off; keep the stone out of the clinic
    npcs.lina_dalen.state.position :: R72: Ashfall General ER with Imran
    npcs.lina_dalen.state.status :: R107: texted Rin 10:30 Oct 29 about the delayed discharge; hopeful
    npcs.mara_quill.knowledge.facts.drain_repair :: R109: LO-04's 2004 crew notes match Varga's: the patch holds; the weak point is the narrow iron drain throat through it, closable from the outer gallery with iron and grout
    npcs.mara_quill.knowledge.facts.eli_statement :: R53: Eli Voss's signed statement 2026-10-10 (name kept under a reference number in her file): windows, Halden Lane, door 7-B, Rusk, crates, the shard, the chase, the hut, and a figure on the far platform he described against the doorframe
    npcs.mara_quill.knowledge.facts.haller_saying :: R86: Rin's email 2026-10-19: Haller's words on raw ember glass — straight out of a wall; "what you take from below, below comes looking for"; keep cold, closed, away from people, never sold back
    npcs.mara_quill.knowledge.facts.imran_footage :: R75: Rin's footage of the removal and Imran's mumbling (audio), 2026-10-14
    npcs.mara_quill.knowledge.facts.imran_recording :: R82: Rin forwarded Lina's recording of Imran's sleep-talk 2026-10-17; Mara told him not to play it to anyone else
    npcs.mara_quill.knowledge.facts.jo_statement :: R75: Jo Kestrel's written statement 2026-10-15: strong detector readings behind Gallo's counter Oct 9, Gallo's denials, the courier and plate photos
    npcs.mara_quill.knowledge.facts.lina_statement :: R85: Lina Dalen's signed statement 2026-10-19: Imran bought a luck stone under the counter at Gallo's ~6 weeks ago for $60
    npcs.mara_quill.knowledge.facts.lo04 :: R108: LO-04 sealed part: 2004 breach; human-passing demonic entity sealed it and left; Varga built the cage; Mrs A. Hale of Wexley witnessed the end with an infant said to be the entity's
    npcs.mara_quill.knowledge.facts.m_cutoff :: R60: M cut the laundromat holder loose 2026-10-11; holder under a doctor's care
    npcs.mara_quill.knowledge.facts.mercer_alarm :: R105: Mercer sump screen pressure alarm 04:14–04:31 Oct 28 at low water, auto-cleared (Eli's screenshot via Rin)
    npcs.mara_quill.knowledge.facts.orin_call :: R60: Rin's word-for-word notes of the 2026-10-09 call from a man calling himself Orin: $2,000 for "two small pieces", a standing job offer, "careful people live a long time in this city"; the window ran exactly to booking that night after
    npcs.mara_quill.knowledge.facts.rin_account :: R36: full account as above, from Rin 2026-10-08; Rin's Transit witness unnamed
    npcs.mara_quill.knowledge.facts.rin_folder :: R47: Rin's evidence folder 2026-10-09: site photos, M thread, OX-9 carton, courier photos and plate KT 72 VRN, timeline of seven window dates, Eli's notes with his name blacked out
    npcs.mara_quill.knowledge.facts.rin_is_sealer_child :: R109: Rin confirmed 2026-10-30 he is the sealer's child (kept off every record)
    npcs.mara_quill.knowledge.facts.rin_suspected :: R108: matched Ada Hale of Wexley to Rin's PI licence file; suspects Rin is the sealer's child
    npcs.mara_quill.knowledge.facts.rm12_0417 :: R32: R. Hale, licensed PI, reported cinderlings drawn to dark-glass lucky charms being sold, fire damage in a Kettering basement, carriers ill, 2026-10-08
    npcs.mara_quill.knowledge.facts.runner_footage :: R90: Rin's Southport footage 2026-10-21 04:06–04:13: a small slag creature came out through the outfall grate at low water, exchanged a red chip and a paper message with the Choir courier, and went back
    npcs.mara_quill.knowledge.facts.rusk_footage :: R63: Rin's clips 2026-10-11 16:20: Rusk in a Merrow pickup checking the Halden service door padlock; plate readable; also Rin's exact words to Orin
    npcs.mara_quill.knowledge.facts.tanner_lane_bag :: R79: Rin saw Gallo carry a small zipped bag to his house at 14 Tanner Lane 15:40 Oct 13 and return without it
    npcs.mara_quill.knowledge.facts.transit_safety_liaison :: R48: has a liaison at Transit Safety, separate from Transit management and Merrow
    npcs.mara_quill.relationships.rin_hale :: R35: {tie: analyst handling Rin's hazard report, attitude: neutral, professionally sceptical, credit: [], grievance: [], believes_identity: licensed PI R. Hale}
    npcs.mara_quill.relationships.rin_hale.attitude :: R109: protective; trusts him completely
    npcs.mara_quill.relationships.rin_hale.credit :: R47: [brought her the first real evidence on the outages, 2026-10-09]
    npcs.mara_quill.state.due :: R109: 2026-11-04 Transit Safety reply on gallery access; 2026-11-01 first retainer payment
    npcs.mara_quill.state.plan :: R109: Rin stays a contractor named Hale on paper; Rin must not enter 7-B or Mercer; close the bleed-drain throat from the outer gallery with iron and grout (a contractor job, no mark or blood needed) — ask Transit Safety how to get a grout crew into the flooded gallery; asked Rin to tell Ada she knows and will keep it
    npcs.mara_quill.state.status :: R109: Rin confirmed 09:25 Oct 30 that he is the 2004 sealer's child; she will keep it off every record; locked LO-04 away
    npcs.mrs_okafor.knowledge.facts.jo_at_shop :: R22: saw a woman wait outside the workshop ~22:30–23:05 Oct 7; Rin said they know each other
    npcs.mrs_okafor.relationships.rin_hale.credit :: R80: [Rin chased off the man who was breaking into her car; paid November rent early, 2026-10-15]
    npcs.mrs_okafor.state.due :: R107: 2026-11-04 08:00 building round; immediately on a tenant or property emergency
    npcs.mrs_okafor.state.plan :: R100: weekly building round, Wednesdays 08:00
    npcs.mrs_okafor.state.status :: R107: Wednesday building round 08:00 Oct 28 done; nothing to report
    npcs.nadia_voss.knowledge.facts.phone_last_seen :: R1: family-plan locator shows Eli's phone last seen Mon Oct 5 06:40, Canal Street embankment area, ~300 m accuracy
    npcs.nadia_voss.knowledge.facts.rin_flowers :: R101: Rin waited three hours after her shift with orange chrysanthemums, 2026-10-26
    npcs.nadia_voss.relationships.rin_hale.attitude :: R101: grateful; trusts him; touched and a little flustered by the flowers
    npcs.nadia_voss.relationships.rin_hale.credit :: R8: [found Eli alive and brought him safe, 2026-10-06]
    npcs.nadia_voss.relationships.rin_hale.tie :: R1: hired PI, client since 2026-10-06
    npcs.nadia_voss.state.due :: R102: on Rin asking her on a Sunday (earliest 2026-11-01)
    npcs.nadia_voss.state.plan :: R101: rest; told Rin to ask her on a Sunday after she's slept (she's off Sundays); keep it from Eli
    npcs.nadia_voss.state.position :: R49: at work, shift Oct 9
    npcs.nadia_voss.state.status :: R102: declined a bike ride home (NO, BUT); let Rin wait at the bus stop with her 23:00–23:12 Oct 26; took the 23:12 night bus with the flowers; reminded him "Sunday"
    npcs.orin_sable.relationships.rin_hale :: R51: {tie: holder of his lost stock; potential recruit, attitude: interested, courteous, credit: [], grievance: [took the Kettering stock], believes_identity: capable independent hunter-PI, Pike's man}
    npcs.orin_sable.relationships.rin_hale.attitude :: R52: amused, wary, interested; sees him as a threat to the supply and a possible recruit
    npcs.orin_sable.state.due :: R104: 2026-11-05 02:00 Southport panel "vandalism"
    npcs.orin_sable.state.plan :: R104: loosen one Southport outfall mesh panel to look like vandalism, and the Mercer sump screen too if it can be reached; lie low; work offer to Rin open
    npcs.orin_sable.state.status :: R104: learned 06:00 Oct 28 the runner did not come; concludes the mesh blocks it
    npcs.pat_okonjo :: R94: {name: Pat Okonjo, job: runs Hollins Boarding Kennels past the ring road, belongs: [], gender: woman, character: unknown (not met), state: {position: Hollins Boarding Kennels, status: forty dogs howl at the old back-field well ~02:00 nightly for a week; council, vet and a priest found nothing, plan: hire someone to sit up one night, due: on Rin's acceptance}, capability: {overall_level: 1}}
    npcs.pat_okonjo.character :: R95: broad, practical, fleece and wellies; temper roll 13 (ordinary)
    npcs.pat_okonjo.relationships.rin_hale :: R95: {tie: client via Pike, attitude: amused, grateful, credit: [solved the howling], grievance: [], believes_identity: Pike's investigator}
    npcs.pat_okonjo.state.due :: R95: none pending
    npcs.pat_okonjo.state.status :: R95: shown Rin's night video of the fox family; laughed; paid $250 cash; given the city wildlife line to move them humanely
    npcs.pike_adeyemi.knowledge.facts.rin_cover_story :: R64: Rin's cover story for strangers: in Ashfall ~5 years, parents in the countryside, farm people (a lie Rin asked him to tell)
    npcs.pike_adeyemi.state.due :: R109: 2026-11-05 18:00 weekly check
    npcs.pike_adeyemi.state.plan :: R64: keep the bar boring; give the cover story if asked; watch who comes in; would rather Rin stayed away a few days
    npcs.pike_adeyemi.state.status :: R109: paid $82.50; passed on the sergeant's news; set the Calloway meeting for 14:00
    npcs.police_sergeant_tip :: R81: {name: police sergeant (Mara's contact, unnamed), job: Ashfall Police Department sergeant, belongs: [ashfall_police], gender: unknown, character: unknown; trusted by Mara, state: {status: receiving Mara's anonymous-source tip with the Tanner Lane footage, plan: assess the assault/threat on Gallo, due: 2026-10-19}, capability: {overall_level: 3}}
    npcs.police_sergeant_tip.state.due :: R109: none pending — case with the courts
    npcs.police_sergeant_tip.state.plan :: R83: identify and pursue the shaven-headed man for the assault/threat on Gallo
    npcs.police_sergeant_tip.state.status :: R109: identified the shaven-headed man as Dean Hollis, Brannock's cousin, with a long record; arrested him Oct 29 for the threat on Gallo (YES, AND); Brannock paying his lawyer
    npcs.suds_and_spin_owner :: R11: {name: Rosa Fenn, job: owner of Suds & Spin laundromat, Kettering, belongs: [], gender: woman, character: practical, sturdy, unfussy; temper roll 9 (ordinary), state: {position: kettering_laundromat counter, status: hired Rin through Pike; will not go into the basement, plan: let Rin work the basement; pay $400 on completion, due: when Rin reports the job done or fails}, relationships: {rin_hale: {tie: hired through Pike, attitude: neutral, practical, credit: [], grievance: [], believes_identity: Pike's pest-and-odd-job person}}, knowledge: {facts: {basement: cats stopped coming in through the grate; cooked rat by the boiler; scorched pipes}}, capability: {overall_level: 1}}
    npcs.suds_and_spin_owner.relationships.rin_hale.attitude :: R15: grateful
    npcs.suds_and_spin_owner.relationships.rin_hale.credit :: R15: [cleared the basement creature, 2026-10-07]
    npcs.suds_and_spin_owner.state.due :: R15: none pending; ordinary shop routine
    npcs.suds_and_spin_owner.state.plan :: R15: get the cats back; run the shop
    npcs.suds_and_spin_owner.state.status :: R39: closing the laundromat 22:00 Oct 8; inside, lights going off
    npcs.taxi_driver_lowfield :: R68: {name: older Sikh cab driver at the Lowfield rank (unnamed), job: taxi driver, belongs: [], gender: man, character: steady, observant, flask of tea; temper roll pending, state: {position: lowfield_cab_rank, status: told Rin about Imran Dalen's stone and pointed him to Lina, plan: ordinary shifts, due: ordinary routine}, knowledge: {facts: {imran: Imran shows off a stone from Gallo's as his luck and has been sick and missing shifts}}, capability: {overall_level: 1}}
    npcs.teodor_varga :: R86: {name: Teodor Varga, job: ironworker, Ironside Lane, Lower Docks; in his seventies, belongs: [], gender: man, character: unknown (not met); sworn to confidentiality after 2004 city contract work, state: {position: Ironside Lane, Lower Docks, status: retired or semi-retired ironworker, plan: unknown until Mara's letter, due: on Mara's letter (2026-10-21 or later)}, knowledge: {facts: {2004: made iron fittings in 2004 for a city job under the Red Line (Mara's file)}}, capability: {overall_level: 4, skills: {ironwork: T3}}}
    npcs.teodor_varga.character :: R91: small, stooped, seventies, huge scarred hands, close-cropped white hair, pale sharp eyes; careful, quiet; temper roll 13 (ordinary)
    npcs.teodor_varga.knowledge.facts.2004_witness :: R91: built an iron cage round the patched masonry under the Red Line in 2004; saw a tall being that didn't move like a man lay its hand on the wall and make the brick glow, then walk away into the tunnel; signed confidentiality papers
    npcs.teodor_varga.knowledge.facts.nightglass :: R92: touched the Nightglass 2026-10-22: warm like the 2004 wall; not forged or cast; nobody living made it
    npcs.teodor_varga.relationships.jo_kestrel :: R96: {tie: the friend the blade is for, attitude: respects her grip, credit: [], grievance: [], believes_identity: a working hunter}
    npcs.teodor_varga.relationships.rin_hale :: R91: {tie: the young man Quill sent about 2004, attitude: wary, curious, kindly, credit: [], grievance: [], believes_identity: Quill's careful field man; privately wonders more}
    npcs.teodor_varga.relationships.rin_hale.attitude :: R96: approving; warming
    npcs.teodor_varga.state.due :: R96: 2026-10-31 09:00
    npcs.teodor_varga.state.plan :: R92: forge Rin a short honest-iron blade over three Saturdays if Rin works the bellows and hammer; $200 for iron and coal; watch how Rin handles a fire
    npcs.teodor_varga.state.status :: R96: first forge day with Rin and Jo; measured Jo's grip (left, reverse, short heavy spine); "you'll do"
    npcs.the_surveyor.state.due :: R104: 2026-11-05 04:00 first low water after Orin's promised fix, if the water is low
    npcs.the_surveyor.state.plan :: R104: wait: no force on the thinned seal (fears rupture before it is ready); expects Orin to reopen the drainage; tries again at the first low water after
    npcs.the_surveyor.state.status :: R104: 06:00 Oct 28 runner reported the drainage blocked by new metal at the sump
    npcs.tomas_reyes.state.due :: R11: immediately if Eli or Nadia contacts him with specific evidence; else his day shifts
    npcs.tomas_reyes.state.status :: R76: hearing yard gossip about the Halden lockdown and audit; texted Eli Oct 15
    npcs.unit9_keeper :: R80: {name: older thin man in a cardigan at Unit 9 (unnamed), job: keeps Unit 9 for Brannock; receives stock and notes, belongs: [ash_choir], gender: man, character: unknown; temper roll pending, state: {position: Unit 9, Exchange Yard, status: took Gallo's stones and notebook 23:50 Oct 16, plan: store them; report to M or Orin's people, due: 2026-10-17 morning report}, capability: {overall_level: 2}}
    npcs.unit9_keeper.state.due :: R82: on Trading Standards summons
    npcs.unit9_keeper.state.status :: R82: present at the 10:00 Oct 19 inspection; gave name and lawyer only
    npcs.vic.name :: R59: Vic Moreno
    npcs.vic.state.due :: R53: when Rusk calls him back to work
    npcs.vic.state.status :: R53: told by Rusk 21:00 Oct 9: no runs for two weeks; relieved
    quests.ash_beneath.status :: R92: completed 2026-10-22 — Eli found (R6); Rusk's Merrow crew ran falsified extended windows (sheets verdict R67); value already paid as event XP xp_halden_falsification (R83), no further XP
    quests.calloway_lockup :: R109: {role: SIDE, type: SHORT, source_ref: irene_calloway, objective: open Frank Calloway's lock-up with Irene and list what is in it, quest_level: 1, status: active — accepted via Pike 2026-10-30}
    quests.calloway_lockup.status :: R110: active — key found 2026-10-30; opening with Irene 2026-10-31 10:00
    quests.demir_stockroom :: R95: {role: SIDE, type: SHORT, source_ref: harun_demir, objective: find who raids Demir's stockroom at night, quest_level: 2, status: active — accepted via Pike 2026-10-22; camera placed 2026-10-23}
    quests.demir_stockroom.status :: R97: completed 2026-10-25 10:30 — footage showed nephew Kemal letting himself and a friend in with his key; Harun paid $300 (no bonus, family); quest XP 12 paid (R2, minor)
    quests.find_eli_voss.status :: R6: completed 2026-10-06 21:30 — Eli brought safe to hale_workshop; quest XP 29 paid (R3, meaningful)
    quests.hollins_well :: R95: {role: SIDE, type: SHORT, source_ref: pat_okonjo, objective: find out why the Hollins kennel dogs howl at the old well at night, quest_level: 1, status: completed 2026-10-23 02:15 — a vixen and four cubs den in a collapsed side hollow of the well; quest XP 7 paid (R1, minor)}
    quests.laundromat_job.status :: R13: completed 2026-10-07 09:57 — basement creature killed; quest XP 29 paid (R3, meaningful)
    rights_obligations.ada_bank_visit :: R55: {type: appointment, parties: [rin_hale, ada_hale], state: {terms: Ada takes Rin to Harland's Bank, Wexley, 2026-10-12 at opening to open the deposit box holding his parent's letters, status: active}}
    rights_obligations.ada_bank_visit.state.status :: R62: done 09:30 Oct 12; deposit box opened; Rin holds his parent's letter
    rights_obligations.calloway_job :: R109: {type: brokered job, parties: [rin_hale, irene_calloway, pike_adeyemi], state: {work: open and inventory the Kettering lock-up with Irene, decently, fee: $350 plus cake, Pike's 15% from it, status: active}}
    rights_obligations.calloway_job.state.next :: R110: open lock-up 6 with Irene 2026-10-31 10:00
    rights_obligations.charm_custody :: R49: {type: chain of custody, parties: [rin_hale, mara_quill], state: {item: Rosa's steel coin vault, locked, with 2 dark glass stones on black cords, transferred 2026-10-09 14:52; now in Mara's locked office filing cabinet; Rin holds the receipt copy}}
    rights_obligations.charm_custody_2 :: R65: {type: chain of custody, parties: [rin_hale, mara_quill], state: {item: 1 dark glass stone on black cord, worn by the Kettering holder ~11 days, in Rin's steel cash box, transferred 2026-10-13 09:20; in Mara's office drawer with the vault}}
    rights_obligations.charm_custody_3 :: R75: {type: chain of custody, parties: [rin_hale, mara_quill], state: {item: 1 dark glass stone on cut black cord, removed from a living patient now in hospital 2026-10-14 23:05, in Rin's third steel box, transferred 2026-10-15 10:05; plus USB of Rin's footage; in Mara's drawer}}
    rights_obligations.city_contract :: R49: {type: contract, parties: [rin_hale, city_risk_office (Mara Quill)], state: {jobs: [report and custody of charms — $750, done, paid by bank transfer by 2026-10-14; documented Halden window from outside, no entry via 7-B — $1,500 on delivery, open], terms: confidentiality; no authority to enter restricted municipal or Transit premises; payment on delivery of documented work, signed: 2026-10-09 14:50}}
    rights_obligations.city_contract.state.jobs :: R95: [all jobs closed and paid: $750 (2026-10-14) + $3,500 (2026-10-23); expenses on receipts pending]
    rights_obligations.city_contract.state.status :: R108: closed; $288 expenses paid 2026-10-30
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
    rights_obligations.mara_lo04_meeting :: R107: {type: appointment, parties: [rin_hale, mara_quill], state: {terms: Friday 2026-10-30 09:00, Room 3-14, door closed, Rin alone, status: active}}
    rights_obligations.mara_lo04_meeting.state.status :: R108: held 09:00 Oct 30
    rights_obligations.mara_meeting :: R36: {type: appointment, parties: [rin_hale, mara_quill], state: {terms: Rin brings one sealed charm to the City Risk Management Office 2026-10-09 14:00; Mara may then commission paid work; meanwhile Rin emails photos and the M thread, status: active}}
    rights_obligations.mara_meeting.state.status :: R47: meeting held 14:03 Oct 9; Mara offered a contractor form for two paid jobs
    rights_obligations.mara_retainer :: R84: {type: proposed retainer, parties: [rin_hale, mara_quill], state: {status: Rin agreed in principle 2026-10-19; terms to be drafted}}
    rights_obligations.mara_retainer.state.status :: R104: signed 2026-10-27 10:40; active; first $1,200 due 2026-11-01
    rights_obligations.mara_retainer.state.terms :: R103: $1,200 a month paid on the 1st; on call up to ten working days a month; field work beyond at $250 a day plus approved expenses; per-job fees for documented outcomes; confidentiality; no authority to enter restricted premises without the office's written authorisation; reports only to Mara; thirty days' notice either side
    rights_obligations.pike_offers_oct22 :: R94: {type: brokered job offers, parties: [rin_hale, pike_adeyemi], state: {demir: $300 + bonus if not family, find who raids the stockroom; okonjo: $250, sit up one night at the well; Pike takes 15%, status: offered}}
    rights_obligations.pike_offers_oct22.state.status :: R109: closed 2026-10-30 11:30; Pike's $82.50 paid
    rights_obligations.southport_camera_authority :: R106: {type: authorisation, parties: [rin_hale, mara_quill], state: {terms: retainer contractor authorised to place monitoring cameras at the Southport outfall and footbridge for the vermin mesh, letter signed 2026-10-28 noon, copied to Transit Safety; lanyard "CONTRACTOR — RISK MANAGEMENT", status: active}}
    rights_obligations.varga_blade :: R93: {type: commission, parties: [rin_hale, teodor_varga], state: {work: short honest-iron bodkin-length blade, for Rin's friend Jo Kestrel (reverse grip, left hand, short heavy spine), terms: Rin works the bellows and hammer three Saturdays from 2026-10-24 09:00; $200 for iron and coal paid 2026-10-22, status: active}}
    rights_obligations.varga_blade.state.status :: R96: first forge Saturday done 2026-10-24 09:00–12:00 (Rin on bellows and hammer; Jo present); a rough iron bar drawn to a point; two Saturdays left (31 Oct, 7 Nov)
    rights_obligations.varga_meeting :: R89: {type: appointment, parties: [rin_hale, teodor_varga], state: {terms: meet 2026-10-22 15:00, green door, Ironside Lane; Varga says he kept his 2004 notebook, status: active}}
    rights_obligations.varga_meeting.state.status :: R100: done 2026-10-22
    rights_obligations.voss_trace :: R1: {type: contract, parties: [rin_hale, nadia_voss], state: {service: missing person trace for Eli Voss, fee: $700 flat, paid: $350 deposit 2026-10-06 cash, balance: $350 on finding Eli, timeframe: Rin estimated 3+ days, expenses: only if pre-agreed, status: active}}
    rights_obligations.voss_trace.state.paid :: R8: $700 total
    rights_obligations.voss_trace.state.status :: R8: completed 2026-10-06 22:20; $350 balance paid in cash; nothing owed either way
    rights_obligations.warren_medical :: R59: {type: paid service, parties: [rin_hale, bellamy_doctor, l_warren], state: {terms: exam today $80 and bloods $120, paid by Rin 2026-10-11; signed written report with results for Rin and Lucy, due 2026-10-14, status: active}}
    rights_obligations.warren_medical.state.status :: R66: done 10:30 Oct 14; signed report delivered to Rin and Lucy: mild anaemia, low white cell count, slightly raised liver enzyme, low core temperature, weight loss — "sustained metabolic strain of unclear origin, improving since exposure to an unidentified warm object ceased"; follow-up in two weeks
    rights_obligations.wharf_room_hold :: R78: {type: room rental, parties: [rin_hale, agnieszka_wolak], state: {terms: back room held a month for $150 cash, 2026-10-16 to 2026-11-16, no ID, no police, no trouble upstairs, status: active}}
    rights_obligations.workshop_lease.state.status :: R78: current; November rent $800 paid early 2026-10-15 18:00
    world_state.glossary.zh_hans.l_warren :: L. Warren = L. 沃伦
    world_state.material_history.barnes_rd_check :: R29: 2026-10-08 ~10:05 routine traffic plate-and-helmet check on Barnes Road; Rin waved on; bag not searched
    world_state.material_history.corran_main_burst :: R109: 2026-10-30 ~10:30 a water main burst on Corran Street; street flooded; Demir's stockroom flooded again; Rin helped lift stock and detoured
    world_state.material_history.corran_st_awning :: R16: 2026-10-07 ~10:35 wind tore a shop awning loose on Corran Street; Rin swerved past; no effect
    world_state.material_history.delivery_disguise :: R61: 2026-10-11 Rin worked Ferris Road as a food-delivery rider (red rain jacket, thermal bag hiding the blade bag, face-buff, helmet); not linked to the hi-vis contractor at the kiosk
    world_state.material_history.eli_notes :: R19: Eli gave Rin his written notes 2026-10-07: 7 window dates with remembered real sign-out times, van plate (photo), door 7-B, Rusk plus two unnamed men, Tomas can confirm end times, gate camera on the left post aimed at the gate
    world_state.material_history.encounter_cinderling_canal :: R3: 2026-10-06 Rin killed the embankment cinderling; combat XP 12 paid (R2, minor)
    world_state.material_history.encounter_cinderling_suds :: R13: 2026-10-07 Rin killed the Suds & Spin basement cinderling (paid as quest XP for laundromat_job, not combat XP)
    world_state.material_history.evidence_folder :: R45: night of Oct 8 Rin printed and assembled an evidence folder at hale_workshop: site photos, M thread screenshots, OX-9 carton, Jo's courier and plate photos, a timeline Oct 4–8, Eli's notes with his name blacked out, the RM-12 slip
    world_state.material_history.gale_st_crash :: R103: 2026-10-26 ~23:35 a young nurse's hatchback hit a lamp post at the foot of Gale Street (swerved for a fox); Rin gave first aid until the ambulance; patrol officer took his name as a witness, not involved
    world_state.material_history.gale_st_night_works :: R62: 2026-10-11 ~22:40 night roadworks closed Gale Street; detour; no effect
    world_state.material_history.gale_st_roadworks :: R17: 2026-10-07 ~11:00 roadworks on Gale Street slowed traffic; no effect
    world_state.material_history.jogger_disguise :: R86: 2026-10-20 dawn Rin ran the canal towpath as a jogger (tights, hoodie, cap, earbuds) to place the camera
    world_state.material_history.kingsway_bus :: R46: 2026-10-09 ~13:30 a city bus broke down across the Kingsway Bridge; long jam; Rin arrived at the Annex at 14:03, three minutes late
    world_state.material_history.kingsway_speedcam :: R76: 2026-10-15 ~11:20 speed-camera van on the Kingsway; not Rin
    world_state.material_history.knife_practice :: R78: 2026-10-16 morning Rin practised drawing Haller's knives (small-of-back sheath and left boot), a hundred draws each
    world_state.material_history.lowfield_blackout :: R70: 2026-10-14 22:40 a Lowfield substation tripped; whole district dark; ordinary fault, cause not announced; diner closed early
    world_state.material_history.lowfield_power_restored :: R72: Lowfield power came back ~23:45 Oct 14
    world_state.material_history.lurcher_walker :: R45: 2026-10-09 ~08:05 a man walked a grey lurcher along the embankment service road; Rin waited till he left
    world_state.material_history.mercer_alarm_oct28 :: R104: Transit telemetry: Mercer sump 7% at 03:50 Oct 28; sump screen differential-pressure alarm 04:14, cleared 04:31, no work order
    world_state.material_history.mercer_low_oct21 :: R89: Mercer sump bottomed at 9% ~04:00 Wed 21 Oct; pumps restarted 05:00 (Eli's telemetry)
    world_state.material_history.mercer_low_schedule :: R100: Transit telemetry (via Eli): next Mercer low water ~04:00 Wed 28 Oct; later lows follow dry spells and are read off the same board
    world_state.material_history.mercer_sump_oct20 :: R88: 2026-10-20 08:20 Transit telemetry: Mercer sump 38% and falling after weekend drizzle; dry night forecast; expected low (under 15%) ~03:00–05:00 Wed 21 Oct
    world_state.material_history.mercer_sump_oct26 :: R98: 2026-10-26 07:45 Mercer 52%, dropping slowly; low maybe Wed 28 early (Eli)
    world_state.material_history.mesh_fitted :: R98: Transit Safety fitted fine stainless vermin mesh on the Southport outfall grate and the Mercer sump screen, Mon 26 Oct
    world_state.material_history.mill_road_flood :: R11: 2026-10-07 ~09:25 short downpour flooded the Mill Road junction; Rin detoured; no other effect
    world_state.material_history.night_oct10 :: R57: Rin home 02:05 Oct 11, texted Ada, slept till 09:00
    world_state.material_history.night_oct14 :: R74: Rin home 03:20 Oct 15 by taxi and bike; slept until ~07:30
    world_state.material_history.night_oct16 :: R81: Rin left Exchange Yard ~00:10 Oct 17 unseen; copied the footage to laptop, USB and cloud; slept till ~08:30
    world_state.material_history.night_oct6 :: R10: night of Oct 6–7 Rin and Eli slept at hale_workshop; nothing disturbed it
    world_state.material_history.night_oct7 :: R25: night of Oct 7–8 Rin slept at hale_workshop; undisturbed
    world_state.material_history.night_oct8 :: R45: Rin slept at hale_workshop ~00:30–07:00 Oct 9; undisturbed
    world_state.material_history.orin_call_notes :: R53: Rin wrote up the Orin call word for word the evening of Oct 9
    world_state.material_history.rain_oct23 :: R96: rain from Friday night 23 Oct through the weekend; Mercer sump filling; no low water expected before Mon/Tue 26–27 Oct (Eli's text)
    world_state.material_history.rest_oct10 :: R56: Rin slept the afternoon of Oct 10 at the workshop
    world_state.material_history.rest_oct15 :: R76: Rin slept 11:40–15:10 Oct 15
    world_state.material_history.rest_oct8 :: R34: Rin slept at hale_workshop from ~14:30 Oct 8, alarm set for 20:30
    world_state.material_history.rest_oct8_evening :: R38: Rin rested at hale_workshop ~17:10–20:30 Oct 8; HP and MP full
    world_state.material_history.rest_oct9 :: R46: Rin slept again at hale_workshop 09:30–12:30 Oct 9
    world_state.material_history.shard_test :: R7: 2026-10-06 Rin tried to sense the shard's resonance through plastic, cardboard, glass and a steel tin; no reliable reading (failure); learned only that it stays warm and heats any container
    world_state.material_history.tanner_st_patrol :: R66: 2026-10-13 ~17:45 a routine Lowfield patrol worked Tanner Street; Rin had already left; no contact
    world_state.material_history.traffic_harrow_ave :: R6: 2026-10-06 ~21:10 minor van–taxi crash on Harrow Avenue, patrol officer waving traffic past; no contact with Rin
    world_state.material_history.transit_mesh_survey :: R96: 2026-10-24 ~14:00 two Transit Safety workers measured and photographed the Southport outfall grate for mesh; did not notice Rin's camera
    world_state.material_history.wexley_train :: R62: 2026-10-12 08:40 train to Wexley; routine ticket check
    world_state.material_history.wren_bus_breakdown :: R17: 2026-10-07 ~11:50 city 14 bus broke down at the Wren Bridge ramp; passengers waiting for a replacement under the bridge
    world_state.material_history.xp_halden_falsification :: R83: event XP 29 paid (R3, meaningful) — Eli's statement and Transit sheets exposed the falsified windows
    world_state.material_history.xp_imran_rescue :: R83: event XP 29 paid (R3, meaningful) — Imran's stone cut off and him rushed to hospital
    world_state.material_history.xp_lucy_rescue :: R83: event XP 12 paid (R2, minor) — Lucy Warren's stone removed, M thread, medical case
    world_state.material_history.xp_unit9_discovery :: R83: event XP 55 paid (R4, major) — Tanner Lane collection filmed, the Nissan tailed to Unit 9, leading to the seizure
  retired:
    locations.southport_outfall.conditions.rin_camera :: found by the Transit Safety mesh crew 26 Oct morning (YES); logged and handed to Mara's liaison
```
