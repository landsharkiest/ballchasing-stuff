import pandas as pd
import os


input_csv = "input.csv"

df = pd.read_csv(input_csv, delimiter=";", encoding="utf-8")

df.columns = df.columns.str.strip()
df = df.sort_values(by="team name")

# Group by "team name" and save each team’s data in a separate CSV file
for team_name, team_data in df.groupby("team name"):
    filename = f"{team_name}.csv"  # Create a unique file per team
    team_data.to_csv(filename, sep=";", index=False)