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
input_csv = "game4.csv"  # Replace with actual input file
team_name = "INFINITE BLUE"  # Replace with the team you want to process
update_team_csv(input_csv, team_name)
