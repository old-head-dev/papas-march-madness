import csv

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"

# Games to clear (Team1, Team2, expected current winner)
games_to_clear = [
    ("Duke", "Siena", "Duke"),
    ("Ohio St", "TCU", "TCU"),
    ("Louisville", "South Florida", "Louisville"),
]

# Read
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

# Snapshot original Actual_Winner values for verification
original_winners = {}
for i, row in enumerate(rows):
    if len(row) >= 6 and row[0] == 'R64':
        key = (row[3], row[4])
        original_winners[(i, key)] = row[5]

# Clear the 3 target games
cleared = []
for i, row in enumerate(rows):
    if len(row) < 6 or row[0] != 'R64':
        continue
    for team1, team2, expected in games_to_clear:
        if row[3] == team1 and row[4] == team2:
            assert row[5] == expected, f"Row {i}: expected '{expected}' but found '{row[5]}'"
            row[5] = ''
            cleared.append((i, team1, team2, expected))
            break

assert len(cleared) == 3, f"Expected to clear 3 games, cleared {len(cleared)}"

# Write
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    original_rows = list(csv.reader(f))

with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(rows)

# Verify
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    verify_rows = list(csv.reader(f))

# Check 1: All rows have 22 fields
for i, row in enumerate(verify_rows):
    assert len(row) == 22, f"Row {i} has {len(row)} fields, expected 22"
print("PASS: All rows have exactly 22 fields")

# Check 2: The 3 games have blank Actual_Winner
for i, team1, team2, old_winner in cleared:
    assert verify_rows[i][5] == '', f"Row {i} ({team1} vs {team2}) still has Actual_Winner='{verify_rows[i][5]}'"
    print(f"PASS: {team1} vs {team2} (row {i}) — Actual_Winner cleared (was '{old_winner}')")

# Check 3: No other Actual_Winner values changed
cleared_indices = {c[0] for c in cleared}
for i, row in enumerate(verify_rows):
    if i in cleared_indices:
        continue
    if len(row) >= 6 and original_rows[i][5] != row[5]:
        print(f"FAIL: Row {i} Actual_Winner changed from '{original_rows[i][5]}' to '{row[5]}'")
        raise AssertionError("Unexpected change")
print("PASS: No other Actual_Winner values were changed")

print("\nAll verifications passed.")
