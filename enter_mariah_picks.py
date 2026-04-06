import csv

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
MARIAH_COL = 11  # 0-based index

# Mariah's R64 picks: map pick (lowercase) to the team she picked
picks = [
    "Duke", "Ohio St", "St. John's", "Kansas", "South Florida",
    "Michigan St", "UCLA", "UConn", "Florida", "Iowa",
    "Vanderbilt", "Nebraska", "N. Carolina", "Illinois", "Saint Mary's",
    "Houston", "Arizona", "Utah St", "Wisconsin", "Arkansas",
    "BYU", "Gonzaga", "Missouri", "Purdue", "Michigan",
    "Saint Louis", "Texas Tech", "Alabama", "Tennessee", "Virginia",
    "Kentucky", "Iowa St"
]

# Read CSV
with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

# Verify header
assert len(rows[0]) == 22, f"Header has {len(rows[0])} columns, expected 22"
assert rows[0][MARIAH_COL] == "Mariah", f"Column 11 is '{rows[0][MARIAH_COL]}', expected 'Mariah'"

matched = 0
for pick in picks:
    pick_lower = pick.lower()
    found = False
    for i, row in enumerate(rows):
        if len(row) < 22:
            continue
        if row[0] != "R64":
            continue
        team1 = row[3]
        team2 = row[4]
        # Match pick to team1 or team2
        if team1.lower() == pick_lower:
            rows[i][MARIAH_COL] = team1  # exact value from CSV
            matched += 1
            found = True
            break
        elif team2.lower() == pick_lower:
            rows[i][MARIAH_COL] = team2
            matched += 1
            found = True
            break
    if not found:
        # Try partial match for Florida (FF: entry) and Tennessee (FF: entry)
        for i, row in enumerate(rows):
            if len(row) < 22 or row[0] != "R64":
                continue
            team1 = row[3]
            team2 = row[4]
            if pick_lower in team1.lower() or pick_lower in team2.lower():
                # Determine which team is the pick
                if pick_lower in team1.lower():
                    rows[i][MARIAH_COL] = team1
                else:
                    rows[i][MARIAH_COL] = team1 if pick_lower == team1.lower() else team2 if pick_lower == team2.lower() else team1
                    # Actually for Florida and Tennessee, we want the non-FF team
                    if pick_lower in team1.lower():
                        rows[i][MARIAH_COL] = team1
                    else:
                        # pick is e.g. "florida" and team1 is "Florida", team2 is "FF:..."
                        # We want the actual team name
                        rows[i][MARIAH_COL] = team1 if pick_lower in team1.lower() else pick
                print(f"  Partial match: '{pick}' -> row {i} ({team1} vs {team2}), set to '{rows[i][MARIAH_COL]}'")
                matched += 1
                found = True
                break
        if not found:
            print(f"  WARNING: No match found for '{pick}'")

print(f"Matched {matched} of {len(picks)} picks")

# Verify all rows have 22 columns
for i, row in enumerate(rows):
    assert len(row) == 22, f"Row {i} has {len(row)} columns, expected 22: {row}"

# Write back
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# Final verification: re-read and check Mariah's picks
with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
    verify_rows = list(csv.reader(f))

print("\nMariah's R64 picks in CSV:")
for row in verify_rows:
    if row[0] == "R64":
        print(f"  {row[3]:20s} vs {row[4]:20s} -> Mariah: {row[MARIAH_COL]}")

# Verify column count
for i, row in enumerate(verify_rows):
    assert len(row) == 22, f"Verification failed: Row {i} has {len(row)} columns"
print(f"\nAll {len(verify_rows)} rows have exactly 22 columns. Done!")
