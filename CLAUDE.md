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

## Participants (16)

Papa, Jon, Drew, Aubrey, Miles, Mariah, Jada, Katy, Lisa, Aaron, Mason, Journey, Sara, Paige, Korbin, Doug

## Pick Entry Workflow

Participants send picks via text, email, or handwritten photos. Formats vary wildly.

1. Jon pastes/uploads raw picks into Claude Code
2. Claude parses picks, fuzzy-matching team names to official bracket.csv names
3. Claude updates the correct participant column(s) in bracket.csv
4. Commit and push: `git add bracket.csv && git commit -m "Add [name] R64 picks" && git push`
5. Dashboard auto-refreshes for all viewers

**Critical**: team names in picks must match bracket.csv exactly (case-insensitive). Common issues:
- Abbreviations: "Mich St" → "Michigan St", "UNC" → "N. Carolina"
- Misspellings: always verify against the Team1/Team2 values in bracket.csv
- First Four teams: replace FF: entries with actual team name once play-in game is decided

## Game Result Update Workflow

1. Jon tells Claude which games finished and who won
2. Claude updates `Actual_Winner` column for those games in bracket.csv
3. Winner must exactly match one of Team1 or Team2 in that row
4. Commit and push

## Picks Per Round (Round-by-Round Format)

Participants do NOT fill out the full bracket upfront. They pick one round at a time:
- R64 picks due before first R64 games
- R32 picks due before first R32 games
- And so on through NCG

## Play-In / First Four Games

Some bracket slots start as "FF:XXX/YYY" format. Once the play-in game is decided:
1. Replace the FF entry in Team2 with the winning team name
2. Update any participant picks that referenced the FF entry
3. The seed is inherited from the bracket position (e.g., always 16-seed or 11-seed)

## Jon's Google Sheet

Jon maintains a separate Google Sheet for personal tracking with Excel formulas. Claude does NOT update the Google Sheet — only bracket.csv.
