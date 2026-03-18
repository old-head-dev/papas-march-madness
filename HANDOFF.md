# Papa's March Madness 2026 — Claude Code Handoff

## Project Overview

Build a live, public-facing March Madness bracket pool dashboard hosted on GitHub Pages. Jon manages a family bracket pool (~15 participants) and needs a flashy dashboard that auto-updates as he fills in game results throughout the tournament.

---

## Architecture

### Data Source
- **`bracket.csv`** — single source of truth, lives in the GitHub repo root
- Jon edits this file directly (fills in picks as they come in, fills in `Actual_Winner` as games are played)
- Every `git push` automatically refreshes the live dashboard

### Dashboard
- **`index.html`** — single-file static HTML/CSS/JS app hosted on GitHub Pages
- Fetches `bracket.csv` from the GitHub raw URL on page load
- Calculates all scores client-side — no backend, no build step

### No Google Sheets dependency
- Jon keeps his Google Sheet separately for personal reference / his existing Results tab formulas
- The Google Sheet is NOT the live data source — the CSV in the repo is

---

## GitHub Setup (TO DO — Claude Code)

1. Create a new public GitHub repo (or use Jon's existing one — confirm with Jon)
2. Enable GitHub Pages on `main` branch, root directory
3. Add `bracket.csv` and `index.html` to repo root
4. Live URL will be: `https://[username].github.io/[repo-name]/`
5. Raw CSV URL (for dashboard to fetch): `https://raw.githubusercontent.com/[username]/[repo-name]/main/bracket.csv`
6. Update the `CSV_URL` constant in `index.html` with the real raw URL

---

## bracket.csv Structure

The file is exported from the "2026 Picks" tab of Jon's Google Sheet (`Papa's March Madness.xlsx`). It has already been shared with Claude and reviewed. Structure is as follows:

### Column layout (left to right)
| Col | Name | Description |
|-----|------|-------------|
| A | `Matchup` / Round label | Team name (row 1 of matchup) OR round header (e.g. `1st Round`, `2nd Round`) |
| B | Point value / Team 2 | Point multiplier on round header rows; Team 2 name on game rows |
| C | `Actual_Winner` | **Jon fills this in** as games are decided |
| D | Papa | Papa's pick for this game |
| E | Jon | Jon's pick |
| F | Drew | |
| G | Aubrey | |
| H | Miles | |
| I | Mariah | |
| J | Jada | |
| K | Katy | |
| L | Lisa | |
| M | Aaron | |
| N | Mason | |
| O | Journey | |
| P | Sara | |
| Q | Paige* | (asterisk in original, treat same as others) |
| R | Korbin | New participant for 2026, column was blank in 2025 |
| S | Doug | |
| T+ | Scoring columns | Calculated 0/1/2 etc. values — **IGNORE**, these feed Jon's Google Sheet formulas |

### Round header rows
Round headers appear as rows with the round name in column A and point value in column B:
- `1st Round` → 1 point per correct pick
- `2nd Round` → 2 points
- `Sweet 16` → 4 points
- `Elite 8` → 8 points
- `Final 4` → 16 points
- `Champ` → 32 points

### Parsing logic
When reading the CSV:
1. Detect round header rows: column A contains a round name AND column B contains a number
2. Track current point value from the most recent header row
3. All subsequent rows until the next header are game rows for that round
4. On game rows: col A = Team1, col B = Team2, col C = Actual_Winner, cols D–S = picks

---

## Participants (in column order)
Papa, Jon, Drew, Aubrey, Miles, Mariah, Jada, Katy, Lisa, Aaron, Mason, Journey, Sara, Paige, Korbin, Doug

- **16 participants total**
- Korbin is new for 2026 (was a blank column in the 2025 data)

---

## Scoring Rules
- A pick earns points if it **exactly matches** `Actual_Winner` (case-insensitive)
- Points per correct pick = value of the current round's point multiplier (1 / 2 / 4 / 8 / 16 / 32)
- `Actual_Winner` blank = game not yet played, no points awarded yet
- Picks that are blank = participant didn't submit a pick (score 0 for that game)

---

## Dashboard Requirements

### Visual Aesthetic
- **Dark, flashy, sports-broadcast feel** — think ESPN/NBA scoreboard energy
- Black/dark navy background
- High-contrast accent colors (orange, electric blue, gold for 1st place)
- Typography: `Barlow Condensed` (headers, numbers, names) + `DM Sans` or `Outfit` (body)
- Animated elements: live pulse dot, entrance animations on load, hover states
- Background: subtle grid or court-line texture
- NOT generic — avoid purple gradients, Inter/Roboto fonts, plain white backgrounds

### Views / Tabs

#### 1. Leaderboard (default view)
- **Podium cards** for top 3 (gold/silver/bronze styling), rank 1 spans full width
- **Full standings table**: rank, name, total points, round-by-round breakdown (R64, R32, S16, E8, F4, NCG)
- **Tournament progress bar**: shows how many games complete per round
- **Champion banner** at top if NCG winner is set

#### 2. Picks (per-person view)
- Round filter buttons (All / R64 / R32 / S16 / E8 / F4 / NCG)
- Grid of person cards, each showing their picks for the selected round
- Each pick row: team name + ✓ (correct) / ✗ (wrong) / pending status + points earned
- Person's total score in card header

#### 3. Bracket (matchup view)
- Grouped by region: East, West, South, Midwest
- Each matchup shows Team1 vs Team2, who won (highlighted), and a mini pick count (e.g. "11 picked Duke")
- Later rounds TBD as teams advance

---

## Jon's Ongoing Workflow (once built)

### When picks come in (each round)
Participants send picks via text, email, or handwritten photo — format is inconsistent. Jon will paste/upload raw picks to **Claude Code**, which should:
1. Parse the picks (fuzzy match team names to official bracket names)
2. Output exactly which cells to fill in `bracket.csv`
3. Optionally write directly to the CSV and commit/push

### When games finish each day
1. Jon opens `bracket.csv` in Excel or any text editor
2. Fills in `Actual_Winner` for completed games (must match one of the two team names in that row)
3. `git add bracket.csv && git commit -m "Update results" && git push`
4. Dashboard refreshes automatically for all viewers

---

## Files in This Handoff

| File | Description |
|------|-------------|
| `HANDOFF.md` | This document |
| `bracket.csv` | Template CSV with 2026 matchups, all picks blank |
| `index.html` | Dashboard shell (partially started — needs completion per specs above) |
| `data.json` | Early draft data structure — can be discarded, CSV is the source of truth |
| `Papa_s_March_Madness.xlsx` | Jon's original Google Sheet export (2025 data, used for reference) |

---

## Key Decisions Already Made
- CSV in GitHub repo = single source of truth (not Google Sheets)
- Jon keeps Google Sheet for personal use / his Results tab formulas
- Dashboard is pure static HTML — no backend, no Node, no build pipeline
- Claude Code handles parsing raw picks and updating CSV when Jon sends them in
- GitHub Pages hosts the dashboard at a shareable public URL
- `bracket.csv` column structure mirrors Jon's existing Google Sheet layout exactly

---

## Context About Jon
- Works on **Windows PC + iPhone 17 Pro** — no Mac tools
- Has surface-level coding knowledge (can read code, follow instructions, not a developer)
- Has GitHub access — Claude Code has direct access to his repos
- Prefers direct, no-fluff communication
- Tournament started **March 17, 2026** — first round games begin **March 19**
- The pool runs through **April 6, 2026** (National Championship)
