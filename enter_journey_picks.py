import csv

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
JOURNEY_COL = 17  # 0-based

# Journey's picks: pick_team -> (team1_hint, team2_hint) for matching context
picks = {
    "Ohio St": ("Ohio St", "TCU"),
    "Nebraska": ("Nebraska", "Troy"),
    "South Florida": ("Louisville", "South Florida"),
    "Wisconsin": ("Wisconsin", "High Point"),
    "Duke": ("Duke", "Siena"),
    "Vanderbilt": ("Vanderbilt", "McNeese"),
    "Michigan St": ("Michigan St", "N. Dakota St"),
    "Arkansas": ("Arkansas", "Hawaii"),
    "VCU": ("N. Carolina", "VCU"),
    "Michigan": ("Michigan", "Howard"),
    "BYU": ("BYU", "Texas"),
    "Saint Mary's": ("Saint Mary's", "Texas A&M"),
    "Illinois": ("Illinois", "Penn"),
    "Saint Louis": ("Georgia", "Saint Louis"),
    "Gonzaga": ("Gonzaga", "Kennesaw St"),
    "Houston": ("Houston", "Idaho"),
    "Kentucky": ("Kentucky", "Santa Clara"),
    "Texas Tech": ("Texas Tech", "Akron"),
    "Arizona": ("Arizona", "Long Island"),
    "Virginia": ("Virginia", "Wright St"),
    "Iowa St": ("Iowa St", "Tennessee St"),
    "Alabama": ("Alabama", "Hofstra"),
    "Villanova": ("Villanova", "Utah St"),
    "Tennessee": ("Tennessee", "Miami (Ohio)"),
    "Iowa": ("Clemson", "Iowa"),
    "St. John's": ("St. John's", "N. Iowa"),
    "UCLA": ("UCLA", "UCF"),
    "Purdue": ("Purdue", "Queens"),
    "Florida": ("Florida", "Prairie View"),
    "Kansas": ("Kansas", "Cal Baptist"),
    "UConn": ("UConn", "Furman"),
    "Miami FL": ("Miami FL", "Missouri"),
}

# Read CSV
with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

matched = set()

for i, row in enumerate(rows):
    if len(row) < 6 or row[0] != "R64":
        continue
    team1 = row[3]
    team2 = row[4]

    for pick_name, (hint1, hint2) in picks.items():
        if pick_name in matched:
            continue
        # Match by checking if Team1 or Team2 matches the pick (case-insensitive)
        t1_lower = team1.lower()
        t2_lower = team2.lower()
        pick_lower = pick_name.lower()

        if t1_lower == pick_lower or t2_lower == pick_lower:
            # Found the row - set Journey's column to exact CSV value
            if t1_lower == pick_lower:
                exact_value = team1
            else:
                exact_value = team2

            # Ensure row has 22 columns
            while len(row) < 22:
                row.append("")

            row[JOURNEY_COL] = exact_value
            matched.add(pick_name)
            print(f"Row {i+1}: {team1} vs {team2} -> Journey picks: {exact_value}")
            break

# Check all picks matched
if len(matched) != 32:
    unmatched = set(picks.keys()) - matched
    print(f"\nERROR: {len(matched)}/32 picks matched. Unmatched: {unmatched}")
else:
    print(f"\nAll 32 picks matched successfully.")

# Verify all rows have exactly 22 fields
bad_rows = []
for i, row in enumerate(rows):
    if len(row) != 22:
        bad_rows.append((i+1, len(row)))

if bad_rows:
    print(f"ERROR: Rows with wrong column count: {bad_rows}")
else:
    print("All rows have exactly 22 columns. Writing...")
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print("Done. bracket.csv updated.")
