import pandas as pd
import os

def update_team_csv(input_csv, team_name):
    """
    Extracts data for a specific team from the input CSV and merges it with an existing team CSV.
    If the CSV exists, it averages out all numerical values while skipping the first two columns.
    """
    # Read the input CSV
    df = pd.read_csv(input_csv, delimiter=";", encoding="utf-8")

    # Filter the data for the specified team
    team_df = df[df["team name"] == team_name]

    # Check if a CSV already exists for this team
    team_csv = f"{team_name}.csv"
    
    if os.path.exists(team_csv):
        # Load existing data
        existing_df = pd.read_csv(team_csv, delimiter=";", encoding="utf-8")

        # Identify numeric columns (skip first two: color and team name)
        numeric_cols = team_df.columns[2:]  

        # Convert to numeric for averaging
        existing_numeric = existing_df[numeric_cols].astype(float)
        new_numeric = team_df[numeric_cols].astype(float)

        # Concatenate and average
        combined_numeric = pd.concat([existing_numeric, new_numeric])
        averaged_numeric = combined_numeric.mean().to_frame().T  # Ensure it's a DataFrame

        # Preserve the first two columns (team name and color)
        result_df = team_df.iloc[:1, :2].copy()  # Take first row for non-numeric data
        for col in numeric_cols:
            result_df[col] = averaged_numeric[col].values[0]  # Assign values properly

        # Save the averaged data back to the CSV
        result_df.to_csv(team_csv, sep=";", index=False)
        print(f"Updated and averaged data saved to {team_csv}")
    
    else:
        # Save new data as a fresh CSV
        team_df.to_csv(team_csv, sep=";", index=False)
        print(f"New file created: {team_csv}")

# Example Usage:

def update_player_csv(input_csv, team_name):
    """
    Extracts data for a specific team from the input CSV and merges it with an existing team CSV.
    If the CSV exists, it averages out all numerical values while preserving non-numeric columns.
    """
    # Read the input CSV
    df = pd.read_csv(input_csv, delimiter=";", encoding="utf-8")

    # Filter the data for the specified team
    team_df = df[df["player name"] == team_name]

    # Automatically identify non-numeric columns
    non_numeric_cols = team_df.select_dtypes(exclude=["number"]).columns.tolist()

    # Identify numeric columns by excluding descriptive columns
    numeric_cols = [col for col in team_df.columns if col not in non_numeric_cols]

    # Check if a CSV already exists for this team
    team_csv = f"{team_name}.csv"
    
    if os.path.exists(team_csv):
        # Load existing data
        existing_df = pd.read_csv(team_csv, delimiter=";", encoding="utf-8")

        # Ensure existing CSV has the same numeric columns
        missing_cols = set(numeric_cols) - set(existing_df.columns)
        for col in missing_cols:
            existing_df[col] = 0  # Fill missing columns with 0

        # Convert to numeric safely
        existing_numeric = existing_df[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        new_numeric = team_df[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

        # Concatenate and average
        combined_numeric = pd.concat([existing_numeric, new_numeric])
        averaged_numeric = combined_numeric.mean().to_frame().T  # Ensure it's a DataFrame

        # Preserve non-numeric columns (team info, player names, etc.)
        result_df = team_df.iloc[:1, :].copy()  # Copy the first row for non-numeric data
        for col in numeric_cols:
            result_df[col] = averaged_numeric[col].values[0]  # Assign averaged values

        # Save the updated data back to the CSV
        result_df.to_csv(team_csv, sep=";", index=False, encoding="utf-8", header=True)
        print(f"Updated and averaged data saved to {team_csv}")

players = ["WestyzWorld","Finny. a&", "im super bad gr"]
input_csv = ["playergame3.csv", "playergame4.csv", "playergame5.csv", "playergame6.csv"]
for i in range(len(players)):
    for x in input_csv:
        update_player_csv("players/"+x, players[i])