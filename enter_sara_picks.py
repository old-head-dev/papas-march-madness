import csv
import sys

CSV_PATH = r"C:\Users\jkher\Documents\Claude\Papas March Madness\bracket.csv"
SARA_COL = 18  # 0-based index

# Sara's R64 picks: map pick team name -> exact value to find in Team1/Team2
picks = [
    "Duke", "TCU", "St. John's", "Kansas", "Louisville", "Michigan St", "UCLA", "UConn",
    "Florida", "Iowa", "Vanderbilt", "Nebraska", "VCU", "Illinois", "Texas A&M", "Houston",
    "Arizona", "Villanova", "Wisconsin", "Arkansas", "BYU", "Gonzaga", "Miami FL", "Purdue",
    "Michigan", "Saint Louis", "Texas Tech", "Alabama", "Tennessee", "Virginia", "Santa Clara", "Iowa St"
]

# Read CSV
with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

# Verify header
assert len(rows[0]) == 22, f"Expected 22 columns in header, got {len(rows[0])}"
assert rows[0][SARA_COL] == "Sara", f"Column 18 is '{rows[0][SARA_COL]}', expected 'Sara'"

# Find R64 rows and enter picks
matched = 0
for pick in picks:
    found = False
    for i, row in enumerate(rows):
        if row[0] != "R64":
            continue
        team1 = row[3]
        team2 = row[4]
        # Match pick to team1 or team2 (case-insensitive)
        if pick.lower() == team1.lower():
            rows[i][SARA_COL] = team1  # use exact CSV value
            print(f"  Row {i+1}: {team1} vs {team2} -> Sara picks: {team1}")
            matched += 1
            found = True
            break
        elif pick.lower() == team2.lower():
            rows[i][SARA_COL] = team2  # use exact CSV value
            print(f"  Row {i+1}: {team1} vs {team2} -> Sara picks: {team2}")
            matched += 1
            found = True
            break
        # Handle FF: entries (e.g., Florida vs FF:LHU/PVAMU)
        elif "FF:" in team2 and pick.lower() == team1.lower():
            rows[i][SARA_COL] = team1
            print(f"  Row {i+1}: {team1} vs {team2} -> Sara picks: {team1}")
            matched += 1
            found = True
            break
        elif "FF:" in team2:
            # Check if pick matches part of FF entry
            pass

    if not found:
        # Try partial match for Tennessee vs FF:SMU/MiaOH
        if pick.lower() == "tennessee":
            for i, row in enumerate(rows):
                if row[0] == "R64" and row[3].lower() == "tennessee":
                    rows[i][SARA_COL] = row[3]
                    print(f"  Row {i+1}: {row[3]} vs {row[4]} -> Sara picks: {row[3]}")
                    matched += 1
                    found = True
                    break
        if not found:
            print(f"  WARNING: Could not match pick '{pick}' to any R64 game!")

print(f"\nMatched {matched} of {len(picks)} picks.")

if matched != 32:
    print("ERROR: Not all 32 picks matched. Aborting.")
    sys.exit(1)

# Verify all rows have 22 columns
for i, row in enumerate(rows):
    if len(row) != 22:
        print(f"ERROR: Row {i+1} has {len(row)} columns, expected 22. Aborting.")
        sys.exit(1)

# Write CSV
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Successfully wrote Sara's R64 picks to bracket.csv")
print("Column alignment verified: all rows have 22 fields.")
