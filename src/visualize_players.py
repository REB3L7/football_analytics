import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "epl_player_metrics.csv"

df = pd.read_csv(DATA_PATH)

# Minimum playing time
df = df[df["time"] >= 270].copy()

# Focus on players with at least one goal
df = df[df["goals"] >= 1].copy()

# Create chart
plt.figure(figsize=(12, 8))

plt.scatter(
    df["xG"],
    df["goals"],
    alpha=0.7,
    s=80
)

# Perfect expected-goals line
max_value = max(df["xG"].max(), df["goals"].max())

plt.plot(
    [0, max_value],
    [0, max_value],
    linestyle="--",
    label="Goals = xG"
)

# Label selected players
top_players = df.sort_values(
    by="goals",
    ascending=False
).head(10)

for _, player in top_players.iterrows():
    plt.annotate(
        player["player_name"],
        (player["xG"], player["goals"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=9
    )

plt.title(
    "Premier League Player Goals vs Expected Goals (2025/26 Snapshot)",
    fontsize=16
)

plt.xlabel("Expected Goals (xG)")
plt.ylabel("Actual Goals")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

# Save visualization
OUTPUT_PATH = BASE_DIR / "dashboards" / "goals_vs_xg.png"

plt.savefig(OUTPUT_PATH, dpi=300)

plt.show()

print("\nVisualization saved successfully!")