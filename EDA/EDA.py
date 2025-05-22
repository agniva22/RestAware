import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime, timedelta

file_path = "./decoded_radar_sleep_data.csv"
df = pd.read_csv(file_path)

start_time = datetime.now()
df['Time'] = df['millis'].apply(lambda x: start_time + timedelta(milliseconds=x))

image_dir = Path("./Image")
image_dir.mkdir(exist_ok=True)
summary_path = Path("./data_summary.txt")

def plot_sleep_status(person_df, name):
    plt.figure(figsize=(12, 3))
    sns.scatterplot(data=person_df, x="Time", y="Status", hue="Status", palette="Set2", legend=False)
    plt.title(f"Status Over Time - {name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(image_dir / f"{name}_Status.eps", format='eps')
    plt.close()

def plot_posture(person_df, name):
    plt.figure(figsize=(12, 3))
    sns.scatterplot(data=person_df, x="Time", y="Posture", hue="Posture", palette="coolwarm", legend=False)
    plt.title(f"Posture Over Time - {name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(image_dir / f"{name}_Posture.eps", format='eps')
    plt.close()

def plot_movement(person_df, name):
    plt.figure(figsize=(12, 3))
    sns.lineplot(data=person_df, x="Time", y="Movement_Value", marker="o")
    plt.title(f"Movement Value Over Time - {name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(image_dir / f"{name}_Movement_Value.eps", format='eps')
    plt.close()

def generate_summary(person_df, name):
    summary = []
    summary.append(f"Summary for {name}:\n")
    summary.append(f"Total Entries: {len(person_df)}\n")
    summary.append(f"Unique Postures: {person_df['Posture'].unique().tolist()}\n")
    summary.append("Posture Counts:\n")
    summary.append(f"{person_df['Posture'].value_counts().to_string()}\n")
    summary.append("Status Counts:\n")
    summary.append(f"{person_df['Status'].value_counts().to_string()}\n")
    summary.append("Movement Value Stats:\n")
    summary.append(f"{person_df['Movement_Value'].describe().to_string()}\n")
    summary.append("-" * 50 + "\n")
    return summary

summary_lines = []

for person in df["Name"].unique():
    person_df = df[df["Name"] == person].copy()
    plot_sleep_status(person_df, person)
    plot_posture(person_df, person)
    plot_movement(person_df, person)
    summary_lines.extend(generate_summary(person_df, person))

with open(summary_path, "w") as f:
    f.writelines(summary_lines)

print(f"Summary saved at: {summary_path}")
print(f"Images saved in: {image_dir}")
