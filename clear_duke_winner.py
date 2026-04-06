import csv

filepath = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"

with open(filepath, 'r', newline='') as f:
    rows = list(csv.reader(f))

found = False
for row in rows:
    if len(row) >= 6 and row[0] == 'R64' and row[3] == 'Duke' and row[4] == 'Siena' and row[5] == 'Duke':
        print(f"Found: {row[:6]}")
        row[5] = ''
        print(f"After:  {row[:6]}")
        found = True
        break

if not found:
    print("ERROR: Duke vs Siena R64 row not found!")
    exit(1)

# Verify all rows have 22 fields
for i, row in enumerate(rows):
    if len(row) != 22:
        print(f"ERROR: Row {i} has {len(row)} fields (expected 22): {row[:6]}")
        exit(1)

print("All rows have exactly 22 fields.")

with open(filepath, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Done. Actual_Winner cleared for Duke vs Siena.")
