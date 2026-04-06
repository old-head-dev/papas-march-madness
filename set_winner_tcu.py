import csv

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"

rows = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

# Find the R64 row with Ohio St vs TCU and blank Actual_Winner
found = False
for i, row in enumerate(rows):
    if len(row) < 6:
        continue
    if row[0] == 'R64' and row[5].strip() == '':
        teams = {row[3].strip(), row[4].strip()}
        if 'Ohio St' in teams and 'TCU' in teams:
            # Use exact value from Team1 or Team2
            if row[3].strip() == 'TCU':
                row[5] = 'TCU'
            elif row[4].strip() == 'TCU':
                row[5] = 'TCU'
            print(f"Row {i}: Set Actual_Winner to 'TCU' for {row[3]} vs {row[4]}")
            found = True
            break

if not found:
    print("ERROR: Could not find the Ohio St vs TCU game with blank Actual_Winner")
    exit(1)

# Write back
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# Verify all rows have 22 fields
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if len(row) != 22:
            print(f"ERROR: Row {i} has {len(row)} fields instead of 22: {row[:5]}...")
            exit(1)

print("Verification passed: all rows have exactly 22 fields.")
