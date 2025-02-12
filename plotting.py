

import pandas as pd
import matplotlib.pyplot as plt

def compare_teams(team1_csv, team2_csv, columns_to_plot):
    """
    Reads two team CSVs, extracts specific data columns, and plots them side by side.
    """
    # Load the CSVs
    team1_df = pd.read_csv(team1_csv, delimiter=";", encoding="utf-8")
    team2_df = pd.read_csv(team2_csv, delimiter=";", encoding="utf-8")

    # Extract team names (assuming they are the same in all rows)
    team1_name = team1_df.iloc[0]["team name"]
    team2_name = team2_df.iloc[0]["team name"]

    # Number of plots needed
    num_plots = len(columns_to_plot)

    # Create subplots
    fig, axes = plt.subplots(1, num_plots, figsize=(5 * num_plots, 5))  # Adjust size based on number of plots

    if num_plots == 1:
        axes = [axes]  # Ensure axes is iterable if only one plot

    # Plot each selected column
    for i, col in enumerate(columns_to_plot):
        # Get the values for both teams
        team1_value = float(team1_df[col].values[0])
        team2_value = float(team2_df[col].values[0])

        # Plot bar chart for this column
        axes[i].bar([team1_name, team2_name], [team1_value, team2_value], color=["blue", "orange"])
        axes[i].set_title(col)
        axes[i].set_ylabel("Amount")

    # Adjust layout
    plt.tight_layout()
    plt.show()

# Example usage:
team1_csv = "TEAM VIRTUE.csv"  # Replace with actual filename
team2_csv = "INFINITE BLUE.csv"  # Replace with actual filename

# Choose specific columns to compare, , "demos inflicted", "time ball possession","avg boost amount", "amount collected","time supersonic speed","amount overfill total", "time slow speed" 
columns_to_plot = ["count stolen big pads", "count stolen small pads", "amount stolen big pads", "amount stolen small pads"]

compare_teams("teams/INFINITE BLUE.csv", "teams/TEAM VIRTUE.csv", columns_to_plot)

#compare_teams(team1_csv, team2_csv, columns_to_plot)

import pandas as pd
import matplotlib.pyplot as plt

def compare_players(player1_csv, player2_csv, player3_csv, columns_to_plot):
    """
    Reads three player CSVs, extracts specific data columns, and plots them side by side.
    """
    # Load the CSVs
    player1_df = pd.read_csv(player1_csv, delimiter=";", encoding="utf-8")
    player2_df = pd.read_csv(player2_csv, delimiter=";", encoding="utf-8")
    player3_df = pd.read_csv(player3_csv, delimiter=";", encoding="utf-8")

    # Extract player names (assuming they are the same in all rows)
    player1_name = player1_df.iloc[0]["player name"]
    player2_name = player2_df.iloc[0]["player name"]
    player3_name = player3_df.iloc[0]["player name"]

    # Number of plots needed
    num_plots = len(columns_to_plot)

    # Create subplots
    fig, axes = plt.subplots(1, num_plots, figsize=(5 * num_plots, 5))  # Adjust size based on number of plots

    if num_plots == 1:
        axes = [axes]  # Ensure axes is iterable if only one plot

    # Plot each selected column
    for i, col in enumerate(columns_to_plot):
        try:
            # Convert values to float and handle missing data
            player1_value = float(player1_df[col].values[0]) if col in player1_df else 0
            player2_value = float(player2_df[col].values[0]) if col in player2_df else 0
            player3_value = float(player3_df[col].values[0]) if col in player3_df else 0

            # Plot bar chart for this column
            axes[i].bar([player1_name, player2_name, player3_name], 
                        [player1_value, player2_value, player3_value], 
                        color=["blue", "orange", "green"])
            axes[i].set_title(col)
            axes[i].set_ylabel("Amount")

        except Exception as e:
            print(f"Error processing column '{col}': {e}")

    # Adjust layout
    plt.tight_layout()
    plt.show()

# Example usage:
# compare_players("player1.csv", "player2.csv", "player3.csv", ["score", "goals", "assists"])

#compare_players("im super bad gr.csv", "WestyzWorld.csv", "Finny. a&.csv", columns_to_plot)
