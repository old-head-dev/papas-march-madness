import csv

PARTICIPANTS = ["Papa","Jon","Drew","Aubrey","Miles","Mariah","Jada","Katy","Lisa","Aaron","Mason","Journey","Sara","Paige","Korbin","Doug"]
HEADER = ["Round","Points","Region","Team1","Team2","Actual_Winner"] + PARTICIPANTS

with open(r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv", newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
# Map column indices
col = {name: i for i, name in enumerate(header)}

# Collect R64 rows
r64_rows = [r for r in rows[1:] if r[0] == 'R64']

print("=" * 140)
print("SECTION 1: R64 GAME-BY-GAME PICKS TABLE")
print("=" * 140)

errors = []
pick_counts = {p: 0 for p in PARTICIPANTS}

regions_order = ["East", "South", "West", "Midwest"]
game_num_by_region = {r: 0 for r in regions_order}

for row in r64_rows:
    region = row[col["Region"]]
    t1 = row[col["Team1"]]
    t2 = row[col["Team2"]]
    game_num_by_region[region] += 1
    gn = game_num_by_region[region]

    print(f"\n{region} Game {gn}: {t1} vs {t2}")
    print("-" * 80)

    for p in PARTICIPANTS:
        pick = row[col[p]]
        flag = ""
        if pick == "":
            if p != "Jon":
                flag = " *** BLANK ***"
                errors.append(f"{p}: BLANK pick for {region} {t1} vs {t2}")
        elif pick != t1 and pick != t2:
            flag = f" *** MISMATCH ('{pick}' not in [{t1}, {t2}]) ***"
            errors.append(f"{p}: MISMATCH '{pick}' for {region} {t1} vs {t2}")

        if pick:
            pick_counts[p] += 1

        print(f"  {p:10s}: {pick:20s}{flag}")

print("\n")
print("=" * 140)
print("SECTION 2: PLAY-IN VERIFICATION")
print("=" * 140)

# Check South 16-seed (Florida vs Prairie View)
# Check Midwest 11-seed (Tennessee vs Miami (Ohio))
for row in r64_rows:
    region = row[col["Region"]]
    t1 = row[col["Team1"]]
    t2 = row[col["Team2"]]

    if region == "South" and "Florida" in t1:
        status = "OK" if "FF:" not in t2 else "STILL FF FORMAT"
        print(f"South 16-seed: {t1} vs {t2} -> {status}")
        if "Prairie View" not in t2 and "FF:" not in t2:
            print(f"  WARNING: Expected 'Prairie View' but got '{t2}'")

    if region == "Midwest" and "Tennessee" in t1:
        status = "OK" if "FF:" not in t2 else "STILL FF FORMAT"
        print(f"Midwest 11-seed: {t1} vs {t2} -> {status}")
        if "Miami (Ohio)" not in t2 and "FF:" not in t2:
            print(f"  WARNING: Expected 'Miami (Ohio)' but got '{t2}'")

print("\n")
print("=" * 140)
print("SECTION 3: PICK COUNT SUMMARY")
print("=" * 140)

for p in PARTICIPANTS:
    expected = 0 if p == "Jon" else 32
    status = "OK" if pick_counts[p] == expected else f"*** EXPECTED {expected} ***"
    print(f"  {p:10s}: {pick_counts[p]:3d} picks  {status}")

print("\n")
print("=" * 140)
print("SECTION 4: ERRORS FOUND")
print("=" * 140)
if errors:
    for e in errors:
        print(f"  {e}")
else:
    print("  No errors found!")

print("\n")
print("=" * 140)
print("SECTION 5: INDIVIDUAL PARTICIPANT PICKS (bracket order: East 1-8, South 1-8, West 1-8, Midwest 1-8)")
print("=" * 140)

# Order: East games 1-8, South 1-8, West 1-8, Midwest 1-8
region_order = ["East", "South", "West", "Midwest"]
ordered_games = []
for reg in region_order:
    reg_games = [r for r in r64_rows if r[col["Region"]] == reg]
    ordered_games.extend(reg_games)

for p in PARTICIPANTS:
    if p == "Jon":
        print(f"\n{p.upper()}: (no picks submitted)")
        continue
    print(f"\n{p.upper()}:")
    picks_list = []
    for row in ordered_games:
        region = row[col["Region"]]
        t1 = row[col["Team1"]]
        t2 = row[col["Team2"]]
        pick = row[col[p]]
        # Show which team they picked against
        matchup = f"{t1} vs {t2}"
        picks_list.append(f"  {region:8s} | {matchup:35s} | Pick: {pick}")
    for line in picks_list:
        print(line)
