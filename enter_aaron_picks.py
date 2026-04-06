import csv

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
AARON_COL = 15  # 0-based

# Aaron's picks: pick_team -> (opponent context for disambiguation)
picks = [
    "TCU", "Nebraska", "South Florida", "Wisconsin", "Duke", "Vanderbilt",
    "Michigan St", "Arkansas", "VCU", "Michigan", "BYU", "Saint Mary's",
    "Illinois", "Georgia", "Gonzaga", "Houston", "Kentucky", "Akron",
    "Arizona", "Virginia", "Iowa St", "Alabama", "Utah St", "Tennessee",
    "Clemson", "St. John's", "UCF", "Purdue", "Florida", "Kansas",
    "UConn", "Missouri"
]

# Read CSV
with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

# For each pick, find the R64 row and set Aaron's column
matched = 0
for pick in picks:
    pick_lower = pick.lower()
    found = False
    for i, row in enumerate(rows):
        if len(row) < 6 or row[0] != 'R64':
            continue
        team1 = row[3]
        team2 = row[4]
        if team1.lower() == pick_lower or team2.lower() == pick_lower:
            # Use exact value from CSV
            exact = team1 if team1.lower() == pick_lower else team2
            if row[AARON_COL] != '':
                print(f"WARNING: Aaron already has a pick for row {i}: {row[AARON_COL]}")
            row[AARON_COL] = exact
            matched += 1
            found = True
            break
    if not found:
        # Try partial match for Tennessee (avoid Tennessee St)
        print(f"ERROR: Could not find R64 row for pick: {pick}")

print(f"Matched {matched} of {len(picks)} picks")

# Verify all rows have exactly 22 fields
for i, row in enumerate(rows):
    if len(row) != 22:
        print(f"ERROR: Row {i} has {len(row)} fields (expected 22): {row[:5]}")

# Write CSV
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Done. Aaron's R64 picks written to bracket.csv")
