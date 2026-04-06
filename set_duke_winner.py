import csv

filepath = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"

with open(filepath, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

found = False
for i, row in enumerate(rows):
    if len(row) >= 6 and row[0] == 'R64' and row[3] == 'Duke' and row[4] == 'Siena' and row[5] == '':
        row[5] = 'Duke'
        found = True
        print(f"Row {i}: Set Actual_Winner to 'Duke' for Duke vs Siena")
        break

if not found:
    print("ERROR: Could not find the Duke vs Siena R64 game with blank Actual_Winner")
    exit(1)

# Verify all rows have 22 fields
for i, row in enumerate(rows):
    if len(row) != 22:
        print(f"ERROR: Row {i} has {len(row)} fields instead of 22: {row[:5]}...")
        exit(1)

print("Verification passed: all rows have exactly 22 fields.")

with open(filepath, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("bracket.csv updated successfully.")
