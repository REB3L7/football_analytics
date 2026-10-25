import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset location
DATA_PATH = BASE_DIR / "data" / "raw" / "premier_league_players.csv"

# Check dataset exists
if not DATA_PATH.exists():
    print("Dataset not found.")
    raise SystemExit(1)

# Load football data
df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")

print("\nOriginal dataset shape:")
print(df.shape)

print("\nAvailable columns:")
print(df.columns.tolist())

# Filter for Premier League
epl_df = df[df["league"] == "EPL"].copy()

# Filter for 2025/26 season
epl_df = epl_df[epl_df["year"] == 2025]

print("\nPremier League 2025/26 dataset:")
print(epl_df.shape)

print("\nFirst five players:")
print(epl_df.head())

print("\nMissing values:")
print(epl_df.isnull().sum())

# Save filtered dataset
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "epl_2025_26.csv"

epl_df.to_csv(OUTPUT_PATH, index=False)

print("\nFiltered dataset saved successfully!")