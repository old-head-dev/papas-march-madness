import csv

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
JON_COL = 7  # 0-based index

# Jon's R64 picks: pick_team -> used to match against Team1/Team2
jon_picks = [
    "Duke", "Ohio St", "St. John's", "Kansas", "South Florida",
    "Michigan St", "UCLA", "UConn", "Florida", "Iowa",
    "Vanderbilt", "Nebraska", "VCU", "Illinois", "Saint Mary's",
    "Houston", "Arizona", "Utah St", "Wisconsin", "Arkansas",
    "BYU", "Gonzaga", "Miami FL", "Purdue", "Michigan",
    "Saint Louis", "Akron", "Hofstra", "Tennessee", "Virginia",
    "Santa Clara", "Iowa St",
]

# Read CSV
with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

# Track which picks were matched
matched = set()

for i, row in enumerate(rows):
    if len(row) < 22:
        continue
    if row[0] != "R64":
        continue
    team1 = row[3]
    team2 = row[4]
    for pick in jon_picks:
        if pick.lower() == team1.lower() or pick.lower() == team2.lower():
            # Use the exact value from the CSV
            exact = team1 if pick.lower() == team1.lower() else team2
            rows[i][JON_COL] = exact
            matched.add(pick)
            print(f"Row {i}: {team1} vs {team2} -> Jon picks {exact}")
            break

# Check all picks matched
unmatched = [p for p in jon_picks if p not in matched]
if unmatched:
    print(f"\nWARNING: Unmatched picks: {unmatched}")
else:
    print(f"\nAll {len(jon_picks)} picks matched successfully.")

# Verify column alignment
bad_rows = [(i, len(r)) for i, r in enumerate(rows) if len(r) != 22 and len(r) > 1]
if bad_rows:
    print(f"ERROR: Column misalignment in rows: {bad_rows}")
else:
    print("Column alignment verified: all rows have 22 fields.")

# Write CSV
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Done. bracket.csv updated.")
