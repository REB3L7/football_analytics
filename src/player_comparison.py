import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "forward_scouting_rankings.csv"

df = pd.read_csv(DATA_PATH)

metrics = [
    "goals_per90",
    "assists_per90",
    "xG_per90",
    "xA_per90",
    "shots_per90",
    "key_passes_per90"
]

labels = [
    "Goals/90",
    "Assists/90",
    "xG/90",
    "xA/90",
    "Shots/90",
    "Key Passes/90"
]

# Ask user which players to compare
print("\nAVAILABLE PLAYERS:")
print(", ".join(sorted(df["player_name"].tolist())))

player1_name = input("\nEnter first player: ").strip()
player2_name = input("Enter second player: ").strip()

# Find selected players
player1 = df[
    df["player_name"].str.casefold() == player1_name.casefold()
]

player2 = df[
    df["player_name"].str.casefold() == player2_name.casefold()
]

if player1.empty or player2.empty:
    print("\nOne or both players were not found.")
    raise SystemExit(1)

player1 = player1.iloc[0]
player2 = player2.iloc[0]

# Retrieve percentile scores
values1 = [
    player1[f"{metric}_percentile"] for metric in metrics
]

values2 = [
    player2[f"{metric}_percentile"] for metric in metrics
]

# Close radar chart
values1 += values1[:1]
values2 += values2[:1]

angles = np.linspace(
    0, 2 * np.pi, len(metrics),
    endpoint=False
).tolist()

angles += angles[:1]

# Create radar chart
fig, ax = plt.subplots(
    figsize=(9, 9),
    subplot_kw={"polar": True}
)

ax.plot(
    angles,
    values1,
    linewidth=2,
    label=player1["player_name"]
)

ax.fill(angles, values1, alpha=0.15)

ax.plot(
    angles,
    values2,
    linewidth=2,
    label=player2["player_name"]
)

ax.fill(angles, values2, alpha=0.15)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

ax.set_ylim(0, 100)

ax.set_title(
    f"{player1['player_name']} vs {player2['player_name']}\n"
    "Premier League Forward Comparison",
    fontsize=15,
    pad=25
)

ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()

OUTPUT_PATH = BASE_DIR / "dashboards" / "player_comparison.png"

plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")

plt.show()

print("\nPlayer comparison chart saved successfully!")