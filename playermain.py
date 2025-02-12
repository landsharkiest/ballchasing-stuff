import pandas as pd
import os


input_csv = "playergame1.csv"

df = pd.read_csv(input_csv, delimiter=";", encoding="utf-8")

df.columns = df.columns.str.strip()
df = df.sort_values(by="player name")

# Group by "team name" and save each team’s data in a separate CSV file
for team_name, team_data in df.groupby("player name"):
    filename = f"{team_name}.csv"  # Create a unique file per team
    team_data.to_csv(filename, sep=";", index=False)