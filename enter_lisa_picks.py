import csv
import sys

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
LISA_COL = 14  # 0-based

# Lisa's R64 picks in bracket order (East 1-8, South 1-8, West 1-8, Midwest 1-8)
lisa_picks = [
    # East
    "Duke", "Ohio St", "St. John's", "Kansas", "Louisville", "Michigan St", "UCLA", "UConn",
    # South
    "Florida", "Iowa", "McNeese", "Nebraska", "N. Carolina", "Illinois", "Saint Mary's", "Houston",
    # West
    "Arizona", "Utah St", "Wisconsin", "Arkansas", "BYU", "Gonzaga", "Miami FL", "Purdue",
    # Midwest
    "Michigan", "Saint Louis", "Texas Tech", "Alabama", "Tennessee", "Virginia", "Kentucky", "Iowa St",
]

# Read CSV
with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

# Find all R64 rows grouped by region in bracket order
r64_rows = []
for i, row in enumerate(rows):
    if len(row) >= 5 and row[0] == 'R64':
        r64_rows.append(i)

# Order: East(8), South(8) -- wait, let me check actual order in file
# From the file: East(8), West(8), South(8), Midwest(8) -- but picks are East, South, West, Midwest
# Let me map by region
region_games = {}
for idx in r64_rows:
    region = rows[idx][2]
    if region not in region_games:
        region_games[region] = []
    region_games[region].append(idx)

# Build pick mapping: region order as given in picks
pick_order = [
    ("East", 8),
    ("South", 8),
    ("West", 8),
    ("Midwest", 8),
]

pick_idx = 0
changes = []

for region, count in pick_order:
    game_indices = region_games[region]
    assert len(game_indices) == count, f"Expected {count} games for {region}, got {len(game_indices)}"
    for i, row_idx in enumerate(game_indices):
        row = rows[row_idx]
        team1 = row[3]
        team2 = row[4]
        pick = lisa_picks[pick_idx]

        # Fuzzy match - case insensitive
        matched = None
        if pick.lower() == team1.lower():
            matched = team1
        elif pick.lower() == team2.lower():
            matched = team2
        else:
            # Try substring match
            if pick.lower() in team1.lower() or team1.lower() in pick.lower():
                matched = team1
            elif pick.lower() in team2.lower() or team2.lower() in pick.lower():
                matched = team2

        if matched is None:
            print(f"ERROR: Could not match pick '{pick}' to {team1} or {team2} in {region} game {i+1}")
            sys.exit(1)

        rows[row_idx][LISA_COL] = matched
        changes.append(f"  {region} G{i+1}: {team1} vs {team2} -> Lisa picks {matched}")
        pick_idx += 1

print(f"Lisa's R64 picks ({len(changes)} games):")
for c in changes:
    print(c)

# Verify all rows have exactly 22 fields
for i, row in enumerate(rows):
    if len(row) != 22:
        print(f"ERROR: Row {i+1} has {len(row)} fields (expected 22): {row[:5]}")
        sys.exit(1)

print("\nAll rows verified: 22 fields each.")

# Write CSV
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("bracket.csv updated successfully.")
