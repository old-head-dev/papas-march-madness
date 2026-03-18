# Papa's March Madness 2026

Family bracket pool dashboard for 16 participants, hosted on GitHub Pages.

## Architecture

- **Single-file dashboard**: `index.html` — static HTML/CSS/JS, no build step
- **Data source**: `bracket.csv` — fetched client-side from GitHub raw URL
- **Hosting**: GitHub Pages (legacy mode) at https://old-head-dev.github.io/papas-march-madness/
- **Repo**: https://github.com/old-head-dev/papas-march-madness (public)
- Every `git push` to `main` auto-deploys the dashboard

## bracket.csv Structure

```
Round,Points,Region,Team1,Team2,Actual_Winner,Papa,Jon,...,Doug
```

- **Round header rows**: "1st Round", "2nd Round", etc. — decorative, skip when parsing
- **Game rows**: Round code (R64/R32/S16/E8/F4/NCG), points, region, team1, team2, actual_winner, then 16 participant pick columns
- **Scoring**: R64=1pt, R32=2pt, S16=4pt, E8=8pt, F4=16pt, NCG=32pt
- **Seeds**: derived from bracket position within each region (1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15)
- **Team name matching**: case-insensitive, must exactly match one of the two teams in that row

**CRITICAL: NEVER hand-edit bracket.csv by manually counting commas.** The file has 22 columns and off-by-one comma errors silently shift picks to wrong participants. ALWAYS use a Python script with the `csv` module: read with `csv.reader`, modify rows as 22-element arrays, write with `csv.writer`, and verify column alignment programmatically before saving.

## Participants (16)

Papa, Jon, Drew, Aubrey, Miles, Mariah, Jada, Katy, Lisa, Aaron, Mason, Journey, Sara, Paige, Korbin, Doug

## Remote Workflow (Phone Commands)

Jon manages the pool from his phone via Claude Code CLI remote sessions. Every command ends with an automatic `git add bracket.csv && git commit && git push` to update the live dashboard.

### Game Results

When Jon types:
```
Winner: Duke
```
or for multiple games:
```
Winners: Duke, Florida, Arizona
```

Claude should:
1. Read bracket.csv and find the game row where Duke is Team1 or Team2 AND Actual_Winner is blank
2. Set Actual_Winner to the exact Team1/Team2 value from that row (preserving original casing/spelling)
3. If the team name is ambiguous (appears in multiple unfinished games), ask Jon to clarify
4. Commit with message like "Results: Duke, Florida, Arizona win" and push

### Play-In Updates

When Jon types:
```
Play-in winner: Lehigh
```

Claude should:
1. Find the FF: entry in bracket.csv containing that team name
2. Replace the entire FF:XXX/YYY value in Team2 with the winning team name
3. Check if any participant picks reference the FF: string and note if updates are needed
4. Commit and push

### Entering Picks

Jon will paste whatever he receives — raw text, screenshots, photos of handwritten notes, email forwards. No fixed format or order.

Claude should:
1. Extract team names from the input (any format, any order, possibly abbreviated or misspelled)
2. Fuzzy-match each team name to the official Team1/Team2 values in bracket.csv for the current round
3. Determine which game each pick belongs to based on team name matching (NOT position/order in the list)
4. Fill the correct participant's column for each matching game row
5. Show Jon the parsed picks in a clear format for confirmation BEFORE committing
6. After Jon confirms, commit with message like "Add Papa R64 picks" and push

**Common abbreviations to handle**: "Mich St" → "Michigan St", "UNC" → "N. Carolina", "SJU" → "St. John's", "Nova" → "Villanova", "UVA" → "Virginia", "UK" → "Kentucky", "Bama" → "Alabama", "OSU" → "Ohio St", etc.

**Confirmation protocol**: After parsing picks, ALWAYS show Jon the full parsed table for confirmation before writing to CSV. If any team name is too fuzzy to be 100% certain, explicitly call it out and ask Jon to clarify. Zero tolerance for mistakes — every pick must be verified correct.

### Strip Dummy Data

When Jon types:
```
Strip dummy data
```

Claude should:
1. Clear ALL Actual_Winner values and ALL participant pick values from bracket.csv
2. Keep the bracket structure intact (Round, Points, Region, Team1, Team2 columns preserved)
3. Commit with message "Strip dummy data for go-live" and push

## Picks Per Round (Round-by-Round Format)

Participants do NOT fill out the full bracket upfront. They pick one round at a time:
- R64 picks → before Thursday R64 games
- R32 picks → Saturday morning before R32 games
- S16 picks → before Sweet 16 games
- E8 picks → before Elite 8 games
- F4 picks → before Final Four games
- NCG pick → before Championship game

Each round's picks go into that round's rows in the CSV. They NEVER overwrite previous round picks — each round has separate rows.

## Bracket Progression (Auto-Populate Next Round Matchups)

When entering game results, Claude must automatically populate the next round's Team1/Team2 when both feeder games have winners. This ensures matchups are ready before the next round's picks come in.

### R64 → R32 (within each region, games paired by bracket position)

Each region has 8 R64 games in this order. The winners feed into R32 as follows:
- **R32 Slot 1**: Winner of R64 Game 1 (1v16) vs Winner of R64 Game 2 (8v9)
- **R32 Slot 2**: Winner of R64 Game 3 (5v12) vs Winner of R64 Game 4 (4v13)
- **R32 Slot 3**: Winner of R64 Game 5 (6v11) vs Winner of R64 Game 6 (3v14)
- **R32 Slot 4**: Winner of R64 Game 7 (7v10) vs Winner of R64 Game 8 (2v15)

### R32 → S16 (within each region)
- **S16 Slot 1**: Winner of R32 Slot 1 vs Winner of R32 Slot 2
- **S16 Slot 2**: Winner of R32 Slot 3 vs Winner of R32 Slot 4

### S16 → E8 (within each region)
- **E8**: Winner of S16 Slot 1 vs Winner of S16 Slot 2

### E8 → F4 (cross-region, 2026 bracket)
- **F4 Game 1**: East champion vs South champion
- **F4 Game 2**: West champion vs Midwest champion

### F4 → NCG
- **NCG**: Winner of F4 Game 1 vs Winner of F4 Game 2

### How to apply
When Claude enters a game result (Actual_Winner):
1. Set Actual_Winner for the completed game
2. Identify the feeder pair for the next round (e.g., R64 games 1 and 2 in East → R32 slot 1 in East)
3. If BOTH games in the pair now have winners, populate Team1 and Team2 in the next round's corresponding slot
4. Team1 = winner from the higher-seeded game (earlier in the bracket), Team2 = winner from the lower-seeded game
5. Use Python csv module for all writes
6. Commit and push

## Play-In / First Four Games

Some bracket slots start as "FF:XXX/YYY" format. Once the play-in game is decided:
1. Replace the FF entry in Team2 with the winning team name
2. Update any participant picks that referenced the FF entry
3. The seed is inherited from the bracket position (e.g., always 16-seed or 11-seed)

### Remaining First Four (as of March 18, 2026)
- **South 16-seed**: Prairie View A&M vs Lehigh → winner plays (1) Florida
- **Midwest 11-seed**: Miami (Ohio) vs SMU → winner plays (6) Tennessee

### Resolved First Four
- **West 11-seed**: Texas (replaced FF:TX/NCSt) → plays (6) BYU
- **Midwest 16-seed**: Howard (replaced FF:HOW/UMBC) → plays (1) Michigan

## Jon's Google Sheet

Jon maintains a separate Google Sheet for personal tracking with Excel formulas. Claude does NOT update the Google Sheet — only bracket.csv.
