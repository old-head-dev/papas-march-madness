import csv
import sys

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
MILES_COL = 10  # 0-based index

# Miles's R64 picks: map pick team name -> True
picks = [
    "Duke", "Ohio St", "N. Iowa", "Kansas", "South Florida", "Michigan St",
    "UCF", "UConn", "Florida", "Iowa", "Vanderbilt", "Nebraska", "VCU",
    "Illinois", "Saint Mary's", "Houston", "Arizona", "Utah St", "High Point",
    "Arkansas", "BYU", "Gonzaga", "Missouri", "Purdue", "Michigan",
    "Saint Louis", "Akron", "Alabama", "Tennessee", "Virginia", "Kentucky",
    "Iowa St"
]

# Read CSV
with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

header = rows[0]
assert len(header) == 22, f"Expected 22 columns in header, got {len(header)}"
assert header[MILES_COL] == "Miles", f"Column 10 is '{header[MILES_COL]}', expected 'Miles'"

matched = set()

for i, row in enumerate(rows):
    if len(row) < 6:
        continue
    if row[0] != "R64":
        continue

    team1 = row[3]
    team2 = row[4]

    # Try to match each pick to this game
    for pick in picks:
        pick_lower = pick.lower()
        if team1.lower() == pick_lower:
            row[MILES_COL] = team1  # Use exact CSV value
            matched.add(pick)
            print(f"Row {i+1}: {team1} vs {team2} -> Miles picks {team1}")
            break
        elif team2.lower() == pick_lower:
            row[MILES_COL] = team2  # Use exact CSV value
            matched.add(pick)
            print(f"Row {i+1}: {team1} vs {team2} -> Miles picks {team2}")
            break
        # Handle FF: entries - check if pick team appears in the FF: string
        elif team2.startswith("FF:") and pick_lower in team2.lower():
            # For FF entries, pick the non-FF team (the opponent)
            # But the pick is for the main team, not the FF team
            pass
        elif team1.lower().startswith(pick_lower) or pick_lower.startswith(team1.lower()):
            pass  # Don't do partial matches here

    # Special handling for Florida vs FF:LHU/PVAMU
    if team2.startswith("FF:") and "Florida" in [team1] and "Florida" in picks and "Florida" not in matched:
        row[MILES_COL] = team1
        matched.add("Florida")
        print(f"Row {i+1}: {team1} vs {team2} -> Miles picks {team1}")

    # Special handling for Tennessee vs FF:SMU/MiaOH
    if team2.startswith("FF:") and "Tennessee" in [team1] and "Tennessee" in picks and "Tennessee" not in matched:
        row[MILES_COL] = team1
        matched.add("Tennessee")
        print(f"Row {i+1}: {team1} vs {team2} -> Miles picks {team1}")

# Check all picks were matched
unmatched = set(picks) - matched
if unmatched:
    print(f"\nERROR: Unmatched picks: {unmatched}")
    sys.exit(1)

print(f"\nMatched all {len(matched)} picks.")

# Verify all rows have 22 columns
for i, row in enumerate(rows):
    if len(row) != 22:
        print(f"ERROR: Row {i+1} has {len(row)} columns, expected 22")
        sys.exit(1)

print("All rows have 22 columns. Writing CSV...")

with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Done! Miles's R64 picks have been entered.")
