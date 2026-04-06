import csv
import sys

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
PAPA_COL = 6  # 0-based index

# Papa's R64 picks mapped by region
picks = {
    "East": ["Duke", "Ohio St", "St. John's", "Kansas", "Louisville", "Michigan St", "UCLA", "UConn"],
    "South": ["Florida", "Iowa", "Vanderbilt", "Nebraska", "VCU", "Illinois", "Saint Mary's", "Houston"],
    "West": ["Arizona", "Utah St", "Wisconsin", "Arkansas", "BYU", "Gonzaga", "Missouri", "Purdue"],
    "Midwest": ["Michigan", "Saint Louis", "Texas Tech", "Alabama", "Miami (Ohio)", "Virginia", "Kentucky", "Iowa St"],
}

# Read CSV
with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

# Verify header
assert len(rows[0]) == 22, f"Header has {len(rows[0])} columns, expected 22"
assert rows[0][PAPA_COL] == "Papa", f"Column 6 is '{rows[0][PAPA_COL]}', expected 'Papa'"

# Build lookup: for each R64 row, map lowercase team names to (row_index, exact_team_name)
matched = 0
for pick_region, pick_list in picks.items():
    for pick_name in pick_list:
        pick_lower = pick_name.lower()
        found = False
        for i, row in enumerate(rows):
            if len(row) < 6:
                continue
            if row[0] != "R64":
                continue
            region = row[2]
            if region.lower() != pick_region.lower():
                continue
            team1 = row[3]
            team2 = row[4]
            if pick_lower == team1.lower() or pick_lower == team2.lower():
                # Set Papa's pick to the exact CSV value
                exact = team1 if pick_lower == team1.lower() else team2
                rows[i][PAPA_COL] = exact
                matched += 1
                found = True
                print(f"  {pick_region}: {pick_name} -> {exact} (row {i+1})")
                break
        if not found:
            print(f"  WARNING: No match for {pick_name} in {pick_region}!")

print(f"\nMatched {matched} of 32 picks")

# Verify all rows have 22 fields
for i, row in enumerate(rows):
    assert len(row) == 22, f"Row {i+1} has {len(row)} columns, expected 22"

# Write back
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("CSV written successfully. All rows verified at 22 columns.")
