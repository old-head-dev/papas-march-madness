import csv

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
MASON_COL = 16  # 0-based

rows = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

# For every R64 row, set Mason's column to Team1
count = 0
for row in rows:
    if len(row) >= 22 and row[0] == 'R64':
        team1 = row[3]
        row[MASON_COL] = team1
        count += 1
        print(f"  Mason picks: {team1} (from {team1} vs {row[4]})")

print(f"\nTotal R64 picks entered: {count}")

# Verify all rows have exactly 22 columns
errors = []
for i, row in enumerate(rows):
    if len(row) != 22:
        errors.append(f"  Row {i+1}: {len(row)} columns")

if errors:
    print("COLUMN COUNT ERRORS:")
    for e in errors:
        print(e)
else:
    print("All rows have exactly 22 columns. Writing file.")
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print("Done.")
