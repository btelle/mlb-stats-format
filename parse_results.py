import csv
import glob
import math
import datetime

FIELDNAMES = [
    "game_id",
    "game_date",
    "game_date_iso",
    "season",
    "day_of_week",
    "home_team",
    "home_team_score",
    "away_team",
    "away_team_score",
    "innings",
    "is_extra_innings",
    "game_length",
    "game_length_minutes",
    "day_or_night",
    "attendance",
    "winning_pitcher",
    "losing_pitcher",
    "save_pitcher",
    "after_rule_change",
    "past_10th_inning",
    "run_differential",
]

# Map retrosheet's unusual abbreviations to common ones
ABBR_MAP = {
    "LAN": "LAD",
    "ANA": "LAA",
    "CHN": "CHC",
    "CHA": "CHW",
    "NYN": "NYM",
    "NYA": "NYY",
    "SFN": "SFG",
    "WAS": "WSN",
    "KCA": "KCR",
    "SDN": "SDP",
    "SLN": "STL",
    "TBA": "TBR",
}


def read_file(path):
    with open(path, "r") as fh:
        reader = csv.reader(fh)
        next(reader)
        for row in reader:
            if "txt" in path.lower():
                yield format_retrosheet_row(row)
            else:
                # only home games to dedupe
                try:
                    if len(row) > 1 and row[4] == "":
                        yield format_row(path, row)
                except:
                    print(row)
                    raise


def abbreviation_match(abbr):
    return ABBR_MAP[abbr.upper()] if abbr in ABBR_MAP else abbr


def format_row(path, row):
    season_year = path.rsplit("/", 1)[1].split("-")[1]
    game_date = datetime.datetime.strptime("{}, {}".format((row[1].split("(")[0]).strip(), season_year), "%A %b %d, %Y")
    game_number = "0"
    if "(" in row[1]:
        game_number = row[1].split("(")[1][0]

    tmp_row = {}
    tmp_row["game_id"] = row[3] + game_date.strftime("%Y%m%d") + game_number
    tmp_row["game_date"] = row[1]
    tmp_row["game_date_iso"] = game_date.strftime("%Y-%m-%d")
    tmp_row["season"] = season_year
    tmp_row["day_of_week"] = game_date.strftime("%a")

    if row[4] == "@":
        tmp_row["home_team"] = row[5]
        tmp_row["home_team_score"] = row[8]
        tmp_row["away_team"] = row[3]
        tmp_row["away_team_score"] = row[7]
    else:
        tmp_row["home_team"] = row[3]
        tmp_row["home_team_score"] = row[7]
        tmp_row["away_team"] = row[5]
        tmp_row["away_team_score"] = row[8]

    tmp_row["innings"] = (9 if row[9] == "" else int(row[9]))
    tmp_row["is_extra_innings"] = ("Y" if (tmp_row["innings"] > 9 or (int(season_year) >= 2020 and tmp_row["game_id"][-1] != "0" and tmp_row["innings"] > 7)) else "N")
    tmp_row["game_length"] = row[16]
    tmp_row["game_length_minutes"] = int(row[16].split(":")[0])*60 + int(row[16].split(":")[1])
    tmp_row["day_or_night"] = row[17]
    tmp_row["attendance"] = int(0 if row[18] == "" else row[18].replace(",", ""))
    tmp_row["winning_pitcher"] = row[13]
    tmp_row["losing_pitcher"] = row[14]
    tmp_row["save_pitcher"] = row[15]
    tmp_row["after_rule_change"] = "Y" if int(tmp_row["season"]) >= 2020 else "N"
    tmp_row["past_10th_inning"] = 1 if tmp_row["innings"] > 10 else 0
    tmp_row["run_differential"] = abs(int(tmp_row["home_team_score"]) - int(tmp_row["away_team_score"]))

    return tmp_row


def format_retrosheet_row(row):
    tmp_row = {}
    tmp_row["game_id"] = abbreviation_match(row[6]) + row[0] + row[1]   # Home team + date + game number (if double-header)
    tmp_row["game_date"] = row[0]
    tmp_row["game_date_iso"] = datetime.datetime.strptime(row[0], "%Y%m%d").strftime("%Y-%m-%d")
    tmp_row["season"] = tmp_row["game_id"][3:7]
    tmp_row["day_of_week"] = row[2]
    tmp_row["home_team"] = abbreviation_match(row[6])
    tmp_row["home_team_score"] = row[10]
    tmp_row["away_team"] = abbreviation_match(row[3])
    tmp_row["away_team_score"] = row[9]
    tmp_row["innings"] = math.ceil(int(row[11])/2.0/3.0)
    tmp_row["is_extra_innings"] = ("Y" if (tmp_row["innings"] > 9 or (int(tmp_row["season"]) >= 2020 and tmp_row["game_id"][-1] != "0" and tmp_row["innings"] > 7)) else "N")
    tmp_row["game_length"] = str(math.floor(int(row[18])/60)) + ":" + str(int(row[18])%60).zfill(2)
    tmp_row["game_length_minutes"] = int(row[18])
    tmp_row["day_or_night"] = row[12]
    tmp_row["attendance"] = int(0 if row[17] == "" else row[17].replace(",", ""))
    tmp_row["winning_pitcher"] = row[94].split(" ")[-1].replace("(none)", "")
    tmp_row["losing_pitcher"] = row[96].split(" ")[-1].replace("(none)", "")
    tmp_row["save_pitcher"] = row[98].split(" ")[-1].replace("(none)", "")
    tmp_row["after_rule_change"] = "Y" if int(tmp_row["season"]) >= 2020 else "N"
    tmp_row["past_10th_inning"] = 1 if tmp_row["innings"] > 10 else 0
    tmp_row["run_differential"] = abs(int(tmp_row["home_team_score"]) - int(tmp_row["away_team_score"]))

    return tmp_row

def main():
    data_dir = "mlb-data-game-level"

    with open("{}.csv".format(data_dir), "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()

        for file in glob.glob("{}/*".format(data_dir)):
            for row in read_file(file):
                writer.writerow(row)


if __name__ == "__main__":
    main()
