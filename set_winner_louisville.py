import csv

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"

# Read all rows
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

# Find and update the Louisville vs South Florida game
found = False
for i, row in enumerate(rows):
    if len(row) >= 6 and row[0] == 'R64':
        teams = {row[3].strip(), row[4].strip()}
        if teams == {'Louisville', 'South Florida'} and row[5].strip() == '':
            # Set Actual_Winner to the exact Team1/Team2 value
            if row[3].strip() == 'Louisville':
                row[5] = 'Louisville'
            else:
                row[5] = row[4].strip()  # use exact value from cell
            found = True
            print(f"Row {i}: Set Actual_Winner to '{row[5]}' for {row[3]} vs {row[4]}")
            break

if not found:
    print("ERROR: Could not find Louisville vs South Florida game with blank Actual_Winner")
    exit(1)

# Write back
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# Verify all rows have 22 columns
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    verify_rows = list(csv.reader(f))

errors = []
for i, row in enumerate(verify_rows):
    if len(row) != 22 and len(row) > 0:  # skip empty trailing rows
        errors.append(f"Row {i}: {len(row)} columns")

if errors:
    print("COLUMN COUNT ERRORS:")
    for e in errors:
        print(f"  {e}")
    exit(1)
else:
    print(f"Verification passed: all {len([r for r in verify_rows if len(r) == 22])} non-empty rows have exactly 22 columns")
