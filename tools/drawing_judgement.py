"""Judgement of drawings per ONE unit of each equipment type, Stage 1 and Stage 2.

Assumptions (see notes per equipment):
- Additions to an EXISTING gas plant: many drawings are revisions of existing plant drawings
  (P&ID, PFD, plot plan, hazardous area, one-line, load tabulation). Where one drawing is shared by
  several new items, a fraction is used (e.g. 0.25 = one sheet shared by about four items).
- Stage 2 = every Stage 1 drawing again (updated / reworked for the bid issue) + the drawings added
  in Stage 2, including tie-in isometrics showing the connection to existing piping.
- Stage 3 (detailed design by the contractor) is excluded: full piping isometrics, fabrication details,
  loop/wiring diagrams, terminal layouts, rebar schedules, hydrotest and on-stream inspection drawings.
- Project-level items (face sheets, drawing control sheet, key plan, overall scope) are not per
  equipment; they belong in Other Deliverables.
"""
import csv, json, re, sys

APP = sys.argv[1]          # index.html (to read the drawing type list)
SRC = sys.argv[2]          # user's equipment_types CSV export
OUT = sys.argv[3]          # importable CSV
NOTES = sys.argv[4]        # readable summary CSV

h = open(APP, encoding='utf-8').read()
STD = json.loads(re.search(r'var STD=(\[.*?\]);\n', h, re.S).group(1))
ABBR = [a for a, _ in STD]
NAME = dict(STD)

# ---------- building blocks ----------
VESSEL_S1 = dict(PID=1, PFD=0.5, DAT=1, MSD=0.25, LDT=0.5, SCH=0.5, FPP=0.25, HAZ=0.25, DOC=0.5)
VESSEL_S2 = dict(EQD=1, FDN=1, PPL=1, PDT=1, ISS=3, IIS=0.5, IPL=0.5, IPD=0.5,
                 CBL=0.5, CCS=0.5, ISD=0.5, SIS=1, MTL=1, DOC=0.5)

def merge(base, **over):
    d = dict(base); d.update(over)
    return {k: v for k, v in d.items() if v}

J = {}   # (name, variant) -> (stage1, stage2, note)

def put(name, variant, s1, s2, note, iso=0):
    s2 = dict(s2)
    if iso: s2['ISO'] = s2.get('ISO', 0) + iso
    full = dict(s1)                       # Stage 1 drawings are reworked in Stage 2
    for k, v in s2.items(): full[k] = full.get(k, 0) + v
    if iso: note += f' Tie-in isometrics: {iso:g}.'
    J[(name, variant)] = (s1, full, note)

# ---------- Process ----------
put('Desander', '', VESSEL_S1, VESSEL_S2,
    'Pressure vessel with sand drain: own P&ID sheet, data sheet; bid package adds vessel GA, foundation, piping plan/details, ~3 instrument spec sheets (DP, level, PSV), SIS for the relief device.', iso=1)
put('Condensate Filter', '', VESSEL_S1, VESSEL_S2,
    'Filter vessel (often duplicated duty/standby on one P&ID). Same package as a small vessel.', iso=1)
put('Produced Water Filter', '', VESSEL_S1, VESSEL_S2,
    'Same as condensate filter.', iso=1)
put('Slug Catcher', '',
    merge(VESSEL_S1, PID=2, PFD=1, FPP=0.5, HAZ=0.5, SCH=1, DOC=1),
    merge(VESSEL_S2, EQD=2, FDN=2, PPL=2, PDT=2, ISS=8, IIS=1, IPL=1, IPD=1, CBL=1, CCS=1, ISD=1,
          LOG=1, SIS=2, SDT=1, CAT=0.5, GAP=0.5, LTG=0.25, MTL=2, DOC=1),
    'Largest item: 2 P&ID sheets, plot-plan and hazardous-area changes, many level/pressure instruments with trips (logic diagram), platforms (structural), buried connections (cathodic protection), grading.', iso=3)
put('Condensate Water Flush Drum', '', VESSEL_S1, merge(VESSEL_S2, ISS=2),
    'Small drum, few instruments.', iso=1)
put('Gas Jet Compressor', '',
    VESSEL_S1,
    merge(VESSEL_S2, FDN=0.5, ISS=3, LOG=0.5, SIS=0),
    'Ejector (no motor): P&ID and data sheet at Stage 1; GA, supports, piping, motive/suction instruments and control logic at Stage 2.', iso=1)
put('Condensate Transfer Pump', '',
    dict(PID=0.5, PFD=0.25, DAT=1, LDT=0.25, SCH=0.25, FPP=0.25, DOC=0.5),
    dict(EQD=1, FDN=1, PPL=1, PDT=1, ISS=3, IIS=0.5, IPL=0.5, IPD=0.5, CBL=0.5, CCS=0.5,
         LOG=0.5, LTG=0.25, GAP=0.25, MTL=1),
    'Pump shown with its drum on a shared P&ID; pump data sheet; Stage 2 adds pump outline/GA, foundation, suction/discharge piping, discharge PT/FT/vibration instruments, start/stop permissives (logic).', iso=1)
put('Condensate Transfer Pump Motor', '',
    dict(E1L=0.25, TAB=0.25, DAT=1),
    dict(ELM=1, ECD=0.5, CBL=1, CCS=1, EDT=0.5, MCC=0.5, MTL=0.5),
    'Electrical side of the pump: motor data sheet, new feeder on the one-line and load tabulation; Stage 2 adds starter elementary diagram, interconnection, power/control cable routing and schedule, grounding/LCS details, MCC bucket update.')

# ---------- Electrical ----------
put('Switchgear Expansion', '',
    dict(E1L=1, TAB=0.5, SWG=1, DAT=1, EQA=0.5, DOC=1),
    dict(SWG=1, ELM=2, ECD=1, EPD=0.5, SCM=0.5, CBL=1, CCS=1, EDT=1, MTL=1, DOC=0.5),
    'New sections/breakers in an existing switchgear: one-line, load tabulation, switchgear spec & arrangement, substation layout; Stage 2 adds front elevation, breaker control elementaries, interconnections, protection block diagram, cabling.')
put('Outdoor Switchrack', '',
    dict(E1L=0.5, TAB=0.25, DAT=0.5, EQA=1, FPP=0.25, HAZ=0.25),
    dict(RAK=1, FDN=1, SDT=1, ELM=1, ECD=0.5, CBL=1, CCS=1, EDT=1, LTG=0.5, MTL=1),
    'Rack with starters/disconnects/panelboard: location and one-line at Stage 1; rack face elevation, foundation, sunshade structure, elementaries, cabling, grounding and lighting at Stage 2.')
put('Power Cable', '500m',
    dict(E1L=0.25, EPD=0.5),
    dict(CBL=1, CCS=0.5, EDT=0.5, MTL=0.5),
    'One feeder run: route on the power distribution diagram at Stage 1; routing layout (1 sheet), schedule, trench/duct details at Stage 2.')
put('Power Cable', '2000m',
    dict(E1L=0.25, EPD=1, KEY=0.5),
    dict(CBL=4, CCS=0.5, EDT=1, MTL=0.5),
    'Long run: route needs a key plan; about 4 routing sheets (~500 m each) plus road/pipe crossing details.')

# ---------- Flare ----------
put('Flare KO Drum', '',
    merge(VESSEL_S1, PFD=1, FPP=0.5, HAZ=0.5, SCH=1),
    merge(VESSEL_S2, PPL=1.5, ISS=5, LOG=1, SIS=1, SDT=1, LTG=0.25, GAP=0.25),
    'Critical safety vessel: sized at Stage 1 (PFD, data sheet, P&ID, plot plan, hazardous area). Stage 2 adds high-level trips (logic), more instruments, platform structure, flare header piping.', iso=2)
put('Flare Blowcase Drum', '',
    VESSEL_S1,
    merge(VESSEL_S2, ISS=4, LOG=0.5),
    'Small drum emptied by gas pressure: level switches and on/off valves need a sequence (logic).', iso=1)

# ---------- Utility ----------
LINE_S1 = dict(PID=0.5, LDT=0.25, SCH=0.5, MSD=0.25)
put('Oil Water Drainage Line', '150m',
    dict(UTI=0.5, PID=0.25, LDT=0.25, SCH=0.5, FPP=0.25),
    dict(UTI=1, PRF=0.5, PDT=1, GAP=0.25, MTL=0.5),
    'Underground gravity sewer: route on utility plan at Stage 1; plan & profile, manhole/connection details and reinstatement at Stage 2.', iso=1)
put('Cast Iron Catch Basin', '',
    dict(UTI=0.25),
    dict(STD=0.5, PDT=0.25, MTL=0.25),
    'Mostly a standard drawing: location at Stage 1, standard detail + connection at Stage 2.')
put('Closed Drainage Line', '200',
    dict(LINE_S1, FPP=0.25),
    dict(PPL=1, PRF=0.5, PDT=1, UTI=0.5, CAT=0.5, MTL=0.5),
    'Buried hydrocarbon drain (assumed 200 m): P&ID and tie-ins at Stage 1; underground plan, profile, details and cathodic protection at Stage 2.', iso=1)
put('Instrument Air Line', '150m',
    dict(PID=0.5, LDT=0.25, SCH=0.5),
    dict(PPL=1, PDT=0.5, UTI=0.5, MTL=0.5),
    'Small above-ground line on existing racks: utility P&ID update; piping plan and supports.', iso=1)
put('Potable Water Line', '100m',
    dict(UTI=0.5, PID=0.25, LDT=0.25, SCH=0.5),
    dict(UTI=1, PDT=0.5, MTL=0.5),
    'Short buried non-hazardous line, mostly utility plan + details.', iso=1)
put('Firewater Line', '150m',
    dict(FPS=0.5, PID=0.25, LDT=0.25, SCH=0.5, MSD=0.25),
    dict(FPS=1, PRF=0.5, PDT=1, CAT=0.5, MTL=0.5),
    'Ring-main extension: fire protection layout and tie-ins at Stage 1; layout, profile, thrust block / valve pit details and cathodic protection at Stage 2.', iso=1)
put('Fire Hydrant', '',
    dict(FPS=0.25),
    dict(STD=0.5, PDT=0.25, MTL=0.25),
    'Location on fire protection plan; standard installation detail.', iso=0.5)
put('Fire Monitor', '',
    dict(FPS=0.25, DAT=0.5),
    dict(STD=0.5, PDT=0.5, FDN=0.25, MTL=0.25),
    'Location and coverage on fire protection plan, monitor data sheet; standard/installation details at Stage 2.', iso=0.5)

# ---------- read user's equipment list and write the importable CSV ----------
rows = list(csv.reader(open(SRC, encoding='utf-8-sig')))
head = rows[0]
out_head = ['Discipline', 'Equipment', 'Variant'] + [n + ' (Stage 1)' for _, n in STD] + [n + ' (Stage 2)' for _, n in STD]

for k, (s1, s2, _) in J.items():
    for d in (s1, s2):
        bad = [a for a in d if a not in ABBR]
        assert not bad, (k, bad)

with open(OUT, 'w', newline='', encoding='utf-8') as f, open(NOTES, 'w', newline='', encoding='utf-8-sig') as g:
    w = csv.writer(f); w.writerow(out_head)
    n = csv.writer(g)
    n.writerow(['Discipline', 'Equipment', 'Variant', 'Stage 1 (per unit)', 'Stage 2 (per unit)',
                'Stage 1 drawings', 'Stage 2 drawings', 'Reasoning'])
    missing = []
    for r in rows[1:]:
        disc, name, var = r[0], r[1], r[2]
        key = (name, var)
        if key not in J:
            missing.append(key); continue
        s1, s2, note = J[key]
        w.writerow([disc, name, var] + [s1.get(a, 0) for a in ABBR] + [s2.get(a, 0) for a in ABBR])
        fmt = lambda d: ', '.join(f'{a} {v:g}' for a, v in d.items())
        n.writerow([disc, name, var, fmt(s1), fmt(s2), f'{sum(s1.values()):g}', f'{sum(s2.values()):g}', note])
    assert not missing, missing
    extra = set(J) - {(r[1], r[2]) for r in rows[1:]}
    assert not extra, extra
print('ok', len(rows) - 1, 'equipment types')
