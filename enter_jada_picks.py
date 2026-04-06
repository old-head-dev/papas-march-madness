import csv
import sys

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
JADA_COL = 12  # 0-based

# Jada's picks: mapping of pick name -> team she picked
# We'll match each to the R64 row by checking Team1/Team2
jada_picks = [
    "Duke",
    "Ohio St",
    "St. John's",
    "Kansas",
    "Louisville",
    "Michigan St",
    "UCLA",
    "UConn",
    "Florida",
    "Iowa",
    "Vanderbilt",
    "Nebraska",
    "N. Carolina",
    "Illinois",
    "Texas A&M",
    "Houston",
    "Arizona",
    "Utah St",
    "Wisconsin",
    "Arkansas",
    "BYU",
    "Gonzaga",
    "Missouri",
    "Purdue",
    "Michigan",
    "Georgia",
    "Akron",
    "Alabama",
    "Tennessee",
    "Virginia",
    "Kentucky",
    "Iowa St",
]

# Read CSV
with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

# Verify header
assert len(rows[0]) == 22, f"Header has {len(rows[0])} columns, expected 22"
assert rows[0][JADA_COL] == "Jada", f"Column 12 is '{rows[0][JADA_COL]}', expected 'Jada'"

# Find all R64 rows
r64_rows = []
for i, row in enumerate(rows):
    if len(row) >= 5 and row[0] == "R64":
        r64_rows.append(i)

print(f"Found {len(r64_rows)} R64 game rows")
assert len(r64_rows) == 32, f"Expected 32 R64 rows, found {len(r64_rows)}"

# For each Jada pick, find the matching R64 row and set her column
matched = 0
for pick in jada_picks:
    pick_lower = pick.lower()
    found = False
    for i in r64_rows:
        row = rows[i]
        team1 = row[3]
        team2 = row[4]
        # Check if pick matches Team1 or Team2 (case-insensitive)
        if team1.lower() == pick_lower or team2.lower() == pick_lower:
            # Use exact value from the CSV
            if team1.lower() == pick_lower:
                exact_pick = team1
            else:
                exact_pick = team2
            # Check if already filled
            if rows[i][JADA_COL] and rows[i][JADA_COL].strip():
                print(f"  WARNING: Jada already has '{rows[i][JADA_COL]}' for {team1} vs {team2}, overwriting with '{exact_pick}'")
            rows[i][JADA_COL] = exact_pick
            print(f"  {pick} -> row {i}: {team1} vs {team2} => {exact_pick}")
            matched += 1
            found = True
            break
        # Also check for partial matches on FF: entries
        if "FF:" in team2 and pick_lower in [team1.lower()]:
            exact_pick = team1
            rows[i][JADA_COL] = exact_pick
            print(f"  {pick} -> row {i}: {team1} vs {team2} => {exact_pick} (FF game)")
            matched += 1
            found = True
            break
    if not found:
        print(f"  ERROR: Could not find R64 game for pick '{pick}'")
        sys.exit(1)

print(f"\nMatched {matched} of {len(jada_picks)} picks")
assert matched == 32, f"Expected 32 matches, got {matched}"

# Verify all rows still have 22 columns
for i, row in enumerate(rows):
    if len(row) != 22:
        print(f"  ERROR: Row {i} has {len(row)} columns instead of 22")
        sys.exit(1)

print("All rows have 22 columns - alignment verified")

# Write back
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("bracket.csv updated successfully with Jada's R64 picks")
