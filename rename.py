import os
import pandas as pd
def rename_csv_files_in_folder(folder_path):
    file_count = {}\
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, delimiter=';')
            
            if df.shape[1] < 3:
                print(f"Error: {file_name} does not have enough columns.")
                continue
            
            teams = df.iloc[:, 1].unique()
            
            if len(teams) < 2:
                print(f"Error: Could not find two distinct team names in {file_name}.")
                continue
            
            base_name = f"{teams[0]} vs {teams[1]}"
            new_file_name = base_name + ".csv"
            new_file_path = os.path.join(folder_path, new_file_name)
            
            count = 1
            while os.path.exists(new_file_path):
                new_file_name = f"{base_name} {count}.csv"
                new_file_path = os.path.join(folder_path, new_file_name)
                count += 1
            
            os.rename(file_path, new_file_path)
            print(f"Renamed {file_name} to: {new_file_name}")

# Example usage
folder_path = "unknown/"  # Update with the actual folder path
rename_csv_files_in_folder(folder_path)
