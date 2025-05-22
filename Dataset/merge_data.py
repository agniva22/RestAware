import pandas as pd
import glob
import os

csv_files = glob.glob("./radar_*.csv")
print(f"Found {len(csv_files)} CSV files.")

df_list = []

for file in csv_files:
    filename = os.path.basename(file)
    name = filename.split("_")[1]

    try:
        df = pd.read_csv(file)
        if df.empty:
            print(f"Warning: {file} is empty.")
            continue
        df["Name"] = name
        df_list.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")

if not df_list:
    raise ValueError("No valid CSV.")

merged_df = pd.concat(df_list, ignore_index=True)
merged_df.to_csv("./collected_data.csv", index=False)
