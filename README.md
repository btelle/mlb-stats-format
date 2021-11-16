# mlb-stats-format

Parse game-level data from [Retrosheet](https://www.retrosheet.org/gamelogs/) and [Baseball Reference](https://www.baseball-reference.com) into a CSV format with the following columns:

* game_id
* game_date
* game_date_iso
* day_of_week
* home_team
* home_team_score
* away_team
* away_team_score
* innings
* is_extra_innings
* game_length
* game_length_minutes
* day_or_night
* attendance
* winning_pitcher
* losing_pitcher
* save_pitcher

## Getting data

For Retrosheet data, save the yearly gamelog TXT file to the `mlb-data-game-level` directory. For Baseball Reference, the game-level data is only available by team. Navigate to each team's page on Baseball Reference (list [here](https://www.baseball-reference.com/leagues/majors/2021.shtml)), click on **Schedule & Results**, and scroll to the *Team Game-by-Game Schedule* table. Under **Share & Export**, click on *Get table as CSV*. Copy the resulting CSV data into a CSV file named `ari-2021-results.csv` in the `mlb-data-game-level` directory, where `ari` is the team's abbreviation and `2021` is the season. Note, the names of these files are used in the script, so they must match this pattern.

## Usage

In a terminal, run:

```
python parse_results.py
```

The results are written to `mlb-data-game-level.csv` in the same directory as the script. The file is overwritten each time it is run.
