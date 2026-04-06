"""Replace the South 16-seed play-in entry FF:LHU/PVAMU with Prairie View (winner)."""
import csv, sys

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
EXPECTED_COLS = 22

# Read
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

updated = False
ff_refs_in_picks = []

for i, row in enumerate(rows):
    # Find the FF:LHU/PVAMU entry in Team2 (column index 4)
    if len(row) >= 5 and "FF:" in row[4] and ("LHU" in row[4] or "PVAMU" in row[4]):
        print(f"Row {i+1}: Found Team2 = '{row[4]}' (Team1 = '{row[3]}', Region = '{row[2]}')")
        row[4] = "Prairie View"
        print(f"  -> Updated Team2 to 'Prairie View'")
        updated = True

    # Check all participant pick columns (indices 6-21) for FF:LHU/PVAMU references
    for j in range(6, min(len(row), 22)):
        if "FF:" in row[j] and ("LHU" in row[j] or "PVAMU" in row[j]):
            header = rows[0][j] if j < len(rows[0]) else f"col{j}"
            ff_refs_in_picks.append((i+1, header, row[j]))

if not updated:
    print("ERROR: Could not find FF:LHU/PVAMU entry in bracket.csv")
    sys.exit(1)

if ff_refs_in_picks:
    print(f"\nWARNING: Found {len(ff_refs_in_picks)} participant pick(s) referencing the FF: string:")
    for row_num, participant, val in ff_refs_in_picks:
        print(f"  Row {row_num}, {participant}: '{val}'")
else:
    print("\nNo participant picks reference the FF:LHU/PVAMU string (all picked Florida).")

# Verify column counts
errors = []
for i, row in enumerate(rows):
    if len(row) != EXPECTED_COLS:
        errors.append((i+1, len(row)))

if errors:
    print(f"\nERROR: Column count mismatches found:")
    for row_num, count in errors:
        print(f"  Row {row_num}: {count} columns (expected {EXPECTED_COLS})")
    sys.exit(1)
else:
    print(f"\nAll {len(rows)} rows have exactly {EXPECTED_COLS} columns. OK")

# Write
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    original = f.read()

with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("bracket.csv updated successfully.")
