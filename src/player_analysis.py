import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "epl_2025_26.csv"

df = pd.read_csv(DATA_PATH)

# Convert statistics to numeric values
numeric_columns = [
    "goals", "assists", "xG", "xA",
    "shots", "key_passes", "time"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove players without recorded minutes
df = df[df["time"] > 0].copy()

# Calculate per-90-minute statistics
df["goals_per90"] = df["goals"] / df["time"] * 90
df["assists_per90"] = df["assists"] / df["time"] * 90
df["xG_per90"] = df["xG"] / df["time"] * 90
df["xA_per90"] = df["xA"] / df["time"] * 90
df["shots_per90"] = df["shots"] / df["time"] * 90
df["key_passes_per90"] = df["key_passes"] / df["time"] * 90

# Finishing performance
df["goals_minus_xG"] = df["goals"] - df["xG"]

# Filter players with at least 270 minutes
qualified = df[df["time"] >= 270].copy()

# Sort by goals per 90
top_scorers = qualified.sort_values(
    by="goals_per90",
    ascending=False
)

print("\nTOP PREMIER LEAGUE SCORERS (PER 90 MINUTES)")
print("-" * 75)

print(
    top_scorers[
        [
            "player_name",
            "team_title",
            "time",
            "goals",
            "goals_per90",
            "xG_per90",
            "goals_minus_xG"
        ]
    ].head(15).to_string(index=False)
)

# Save enriched dataset
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "epl_player_metrics.csv"

df.to_csv(OUTPUT_PATH, index=False)

print("\nPlayer metrics saved successfully!")