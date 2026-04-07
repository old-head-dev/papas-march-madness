# Papa's March Madness — Next Year Setup Guide

## What This Project Is

A single-page dashboard (`index.html`) + CSV data file (`bracket.csv`) hosted on GitHub Pages. No build step — just push to `main` and it auto-deploys.

**Live site**: https://old-head-dev.github.io/papas-march-madness/
**Repo**: https://github.com/old-head-dev/papas-march-madness

---

## Steps to Update for a New Year

### 1. Create a New `bracket.csv`

The CSV has 22 columns:

```
Round,Points,Region,Team1,Team2,Actual_Winner,Papa,Jon,Drew,Aubrey,Miles,Mariah,Jada,Katy,Lisa,Aaron,Mason,Journey,Sara,Paige,Korbin,Doug
```

**If participants change**, update the header row (columns 6-21) and also update:
- `CLAUDE.md` — the participant list, column indices, and count references
- `index.html` — the JS `PARTICIPANTS` array (search for it near the top of the `<script>` block)

**Bracket structure — 70 rows total:**

| Row | Content |
|-----|---------|
| 1 | Header row |
| 2 | "1st Round" section label (decorative) |
| 3-34 | R64 games (32 games: 8 per region × 4 regions) |
| 35 | "2nd Round" section label |
| 36-51 | R32 games (16 games: 4 per region) |
| 52 | "Sweet 16" section label |
| 53-60 | S16 games (8 games: 2 per region) |
| 61 | "Elite 8" section label |
| 62-65 | E8 games (4 games: 1 per region) |
| 66 | "Final 4" section label |
| 67-68 | F4 games (2 games) |
| 69 | "Championship" section label |
| 70 | NCG game (1 game) |

**Region order matters** — within each round, games are grouped by region in this order: East, West, South, Midwest. Within each region, games follow bracket position (1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15).

**Points per round**: R64=1, R32=2, S16=4, E8=8, F4=16, NCG=32.

**For each game row, fill in:**
- `Round`: R64, R32, S16, E8, F4, or NCG
- `Points`: per the scoring above
- `Region`: East/West/South/Midwest (or "Final Four"/"Championship" for F4/NCG)
- `Team1`: Higher-seeded team (by bracket position)
- `Team2`: Lower-seeded team
- `Actual_Winner`: Leave blank — filled in as games are played
- Participant columns: Leave blank — filled in as picks come in

**Play-in games**: If the bracket has First Four play-in games, put placeholder text like `FF:TeamA/TeamB` in the Team2 field. Once the play-in game is decided, replace with the winning team name.

**Later round matchups** (R32 onward): You can leave Team1/Team2 blank initially — they get auto-populated when feeder games have winners. But the rows themselves must exist in the CSV.

### 2. Update F4 → NCG Region Pairing

The F4 matchups are cross-region and change every year based on the NCAA bracket. In `CLAUDE.md`, update:

```
### E8 → F4 (cross-region, 20XX bracket)
- F4 Game 1: [Region] champion vs [Region] champion
- F4 Game 2: [Region] champion vs [Region] champion
```

Check the official NCAA bracket to see which regions are paired.

### 3. Update `index.html` History Tab

Add the new year's results to the History section (search for `<!-- HISTORY -->`). Add the new year as the first card, bump existing years' stagger classes up by one.

### 4. Update `CLAUDE.md` Current Status

Reset the "Current Status" section to reflect the new tournament state:
- Clear round completion status
- Update dates for the new year's tournament schedule

### 5. Clean Up Old Scripts

The repo accumulates one-off Python scripts (`enter_*_picks.py`, `set_winner_*.py`, etc.) from the previous year. These can be deleted — they were used for initial data entry and aren't needed going forward.

---

## How the Dashboard Works During the Tournament

### Entering Picks

Jon pastes pick data (any format — text, screenshots, handwritten notes) into a Claude Code CLI session. Claude:
1. Fuzzy-matches team names to official bracket values
2. Shows a confirmation table
3. Writes to `bracket.csv` using Python's `csv` module (NEVER hand-edit the CSV)
4. Commits and pushes to deploy

### Entering Game Results

Jon types `Winner: Duke` or `Winners: Duke, Florida`. Claude:
1. Finds the matching game row where that team plays and Actual_Winner is blank
2. Sets Actual_Winner
3. Auto-populates next-round matchups if both feeder games are decided
4. Commits and pushes

### Dashboard Auto-Refresh

The dashboard re-fetches `bracket.csv` on visibility change, pageshow, and focus events — so it updates automatically when users switch back to the tab/app.

---

## Key Files

| File | Purpose |
|------|---------|
| `index.html` | The entire dashboard — HTML, CSS, JS in one file |
| `bracket.csv` | All bracket data — teams, results, picks |
| `CLAUDE.md` | Instructions for Claude Code sessions |
| `manifest.json` | Web app manifest for Add to Home Screen |
| `icon.jpg` | App icon |

---

## Starter Prompt for New Year

Copy-paste this to kick off a new year's setup:

```
I need to set up Papa's March Madness bracket pool for [YEAR]. Here's the bracket:

[paste bracket or link]

Participants: [list names, or "same as last year"]

Please:
1. Create a new bracket.csv with the correct teams and matchups
2. Update CLAUDE.md with new dates, F4 region pairings, and current status
3. Clean up old one-off scripts from last year
4. Push everything to deploy
```
