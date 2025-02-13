import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import defaultdict

def plot_rocket_league_scatter_with_regression(folder_path, x_column, y_column):
    plt.figure(figsize=(10, 6))
    
    team_stats = defaultdict(lambda: {'x_values': [], 'y_values': []})
    
    for file_name in os.listdir(folder_path):
        match = re.match(r"^(.*?) vs (.*?) \d+\.csv$", file_name)
        if not match:
            print(f"Skipping {file_name}: Incorrect filename format.")
            continue
        
        team1, team2 = match.groups()
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, delimiter=';')
        
        if x_column in df.columns and y_column in df.columns:
            x_values = df[x_column].dropna()
            y_values = df[y_column].dropna()
            
            if len(x_values) == len(y_values):
                team_stats[team1]['x_values'].extend(x_values)
                team_stats[team1]['y_values'].extend(y_values)
                team_stats[team2]['x_values'].extend(x_values)
                team_stats[team2]['y_values'].extend(y_values)
            else:
                print(f"Skipping {file_name}: Column lengths do not match.")
        else:
            print(f"Skipping {file_name}: Columns '{x_column}' or '{y_column}' not found.")
    
    # Plot all data points with a regression line
    all_x = []
    all_y = []
    all_labels = []
    
    for team, values in team_stats.items():
        all_x.extend(values['x_values'])
        all_y.extend(values['y_values'])
        all_labels.extend([team] * len(values['x_values']))
    
    plt.figure(figsize=(10, 6))
    sns.regplot(x=all_x, y=all_y, scatter_kws={'alpha': 0.5})
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{x_column} vs {y_column} with Regression Line")
    plt.show()
    
    # Plot individual team data points with different colors
    plt.figure(figsize=(10, 6))
    
    for team, values in team_stats.items():
        sns.scatterplot(x=values['x_values'], y=values['y_values'], label=team)
    
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{x_column} vs {y_column} - Team-wise Distribution")
    plt.legend()
    plt.show()

# Example usage
folder_path = "unknown/"  # Update with actual folder path
x_column = "avg boost amount"  # Update with desired X-axis column
y_column = "time ball in own side"  # Update with desired Y-axis column
plot_rocket_league_scatter_with_regression(folder_path, x_column, y_column)