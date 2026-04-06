# Papa's March Madness 2026

Family bracket pool dashboard for 16 participants, hosted on GitHub Pages.

## Architecture

- **Single-file dashboard**: `index.html` — static HTML/CSS/JS, no build step
- **Data source**: `bracket.csv` — fetched client-side via relative path (same GitHub Pages origin)
- **Hosting**: GitHub Pages at https://old-head-dev.github.io/papas-march-madness/
- **Repo**: https://github.com/old-head-dev/papas-march-madness (public)
- Every `git push` to `main` auto-deploys (CDN propagation takes 1-5 minutes)
- **Web app manifest**: `manifest.json` — supports Add to Home Screen on iOS
- **Auto-refresh**: visibility change, pageshow, and focus listeners re-fetch data when app returns to foreground

## bracket.csv Structure

```
Round,Points,Region,Team1,Team2,Actual_Winner,Papa,Jon,Drew,Aubrey,Miles,Mariah,Jada,Katy,Lisa,Aaron,Mason,Journey,Sara,Paige,Korbin,Doug
```

- **22 columns total** — column indices: Round(0), Points(1), Region(2), Team1(3), Team2(4), Actual_Winner(5), Papa(6), Jon(7), Drew(8), Aubrey(9), Miles(10), Mariah(11), Jada(12), Katy(13), Lisa(14), Aaron(15), Mason(16), Journey(17), Sara(18), Paige(19), Korbin(20), Doug(21)
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

**Permissions setup for remote sessions** — paste at start of session:
```
/allowed-tools Bash(python *) Bash(git add *) Bash(git commit *) Bash(git push *) Bash(git push) Bash(git status *) Bash(git log *) Bash(git diff *)
```

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
4. After setting winner(s), check bracket progression rules below — auto-populate next round matchups if both feeder games are decided
5. Commit with message like "Results: Duke, Florida, Arizona win" and push

### Play-In Updates

When Jon types:
```
Play-in winner: Lehigh
```

Claude should:
1. Find the FF: entry in bracket.csv containing that team name
2. Replace the entire FF:XXX/YYY value in Team2 with the winning team name
3. Check if any participant picks reference the FF: string and update if needed
4. Commit and push

### Entering Picks

Jon will paste whatever he receives — raw text, screenshots, photos of handwritten notes, email forwards. No fixed format or order. Picks may arrive in bracket order, by region, or completely random.

Claude should:
1. Extract team names from the input (any format, any order, possibly abbreviated or misspelled)
2. Fuzzy-match each team name to the official Team1/Team2 values in bracket.csv for the current round
3. Determine which game each pick belongs to based on team name matching (NOT position/order in the list)
4. Fill the correct participant's column for each matching game row
5. Show Jon the parsed picks in a clear table format for confirmation BEFORE committing
6. If ALL picks are confident matches with no questions, confirm and proceed
7. If any team name is too fuzzy to be 100% certain, explicitly call it out and ask Jon to clarify
8. After Jon confirms, commit with message like "Add Papa R64 picks" and push

**Common abbreviations to handle**: "Mich St"/"MSU" → "Michigan St", "UNC" → "N. Carolina", "SJU"/"St Johns" → "St. John's", "Nova"/"Villa" → "Villanova", "UVA"/"VA" → "Virginia", "UK"/"KY" → "Kentucky", "Bama"/"AL" → "Alabama", "OSU"/"OHST"/"Ohio State" → "Ohio St", "USF" → "South Florida", "Zags"/"Gonz" → "Gonzaga", "Vandy" → "Vanderbilt", "KU" → "Kansas", "FL" → "Florida", "IL" → "Illinois", "AZ" → "Arizona", "TN" → "Tennessee", "PU" → "Purdue", "MI" → "Michigan", "St Marys" → "Saint Mary's", "Texas AM" → "Texas A&M", "SLU" → "Saint Louis", "Zona" → "Arizona", "Gonz" → "Gonzaga", "TTU" → "Texas Tech", "IA" → "Iowa St", "St John"/"Saint John" → "St. John's"

**Confirmation protocol**: Zero tolerance for mistakes. Every pick must be verified correct. Flag upset picks (lower seed over higher seed) in the confirmation table. Note all fuzzy matches made.

## Picks Per Round (Round-by-Round Format)

Participants do NOT fill out the full bracket upfront. They pick one round at a time:
- R64 picks → before Thursday R64 games (March 19-20)
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

## First Four / Play-In Games (All Resolved)

- **West 11-seed**: Texas → plays (6) BYU
- **Midwest 16-seed**: Howard → plays (1) Michigan
- **South 16-seed**: Prairie View A&M → Prairie View → plays (1) Florida
- **Midwest 11-seed**: Miami (Ohio) → plays (6) Tennessee

## Current Status (as of March 21, 2026)

- R64 complete — all 32 games decided, all R32 matchups populated
- R32 picks being entered (12 of 16 participants done)
- Dashboard live at https://old-head-dev.github.io/papas-march-madness/
- R32 games start Saturday March 22

## Dashboard Features

- **Leaderboard**: Sortable standings table with podium, round-by-round scores, MVP/cold badges (require 3+ distinct scores), rank movement arrows
- **Picks**: Pick consensus heatmap showing who picked each team
- **Upsets**: Called It (green), Missed It (red), No One Saw It Coming (yellow)
- **Lone Wolf**: Unique picks no one else made — HIT (green), MISS (red), TBD (gray)
- **Head-to-Head**: Compare any two participants pick-by-pick
- **Awards**: Most upsets called, most upsets missed, highest/lowest round score, chalkiest picker, boldest picker, consensus crusher, playing it safe
- **History**: Past tournament results (2024, 2025 winners)

## Jon's Google Sheet

Jon maintains a separate Google Sheet for personal tracking with Excel formulas. Claude does NOT update the Google Sheet — only bracket.csv.

## Verify Before Done

- Data: open `bracket.csv` and confirm all picks/winners are correct — read back any manual entries to the user
- Local test: open `index.html` in a browser, verify scores render correctly and no console errors
- Deploy: `git push` to main, then verify the live GitHub Pages URL loads with updated data
