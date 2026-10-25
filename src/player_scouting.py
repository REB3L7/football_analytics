import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "epl_player_metrics.csv"

df = pd.read_csv(DATA_PATH)

# Focus on forwards
forwards = df[df["primary_position"] == "F"].copy()

# Minimum playing time
forwards = forwards[forwards["time"] >= 270].copy()

# Metrics used for scouting
metrics = [
    "goals_per90",
    "assists_per90",
    "xG_per90",
    "xA_per90",
    "shots_per90",
    "key_passes_per90"
]

# Convert metrics to percentile rankings
for metric in metrics:
    forwards[f"{metric}_percentile"] = (
        forwards[metric].rank(pct=True) * 100
    )

# Calculate overall scouting score
percentile_columns = [
    f"{metric}_percentile" for metric in metrics
]

forwards["scouting_score"] = (
    forwards[percentile_columns].mean(axis=1)
)

# Rank players
ranked_forwards = forwards.sort_values(
    by="scouting_score",
    ascending=False
)

print("\nTOP PREMIER LEAGUE FORWARDS — SCOUTING RANKINGS")
print("-" * 85)

print(
    ranked_forwards[
        [
            "player_name",
            "team_title",
            "time",
            "goals_per90",
            "xG_per90",
            "assists_per90",
            "xA_per90",
            "scouting_score"
        ]
    ].head(15).round(2).to_string(index=False)
)

# Save scouting results
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "forward_scouting_rankings.csv"

ranked_forwards.to_csv(OUTPUT_PATH, index=False)

print("\nScouting rankings saved successfully!")