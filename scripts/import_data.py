import pandas as pd
import psycopg
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "epl_player_metrics.csv"

# Load processed football data
df = pd.read_csv(DATA_PATH)

# Connect to PostgreSQL
conn = psycopg.connect(
    dbname="football_analytics",
    user="roti",
    host="localhost",
    port=5432
)

cursor = conn.cursor()

# STEP 1: Clean team assignments

# Explicit assignments for players with multiple clubs
team_overrides = {
    7546: "Aston Villa",  # Harvey Elliott
    8706: "Arsenal"       # Eberechi Eze
}

df["clean_team"] = df.apply(
    lambda row: team_overrides.get(
        int(row["id"]),
        row["team_title"]
    ),
    axis=1
)

# Identify unique teams after cleaning
teams = df["clean_team"].dropna().unique()

for team in teams:
    cursor.execute(
        """
        INSERT INTO teams (team_name)
        VALUES (%s)
        ON CONFLICT (team_name) DO NOTHING
        """,
        (team,)
    )

print(f"\nProcessed {len(teams)} teams.")

# STEP 2: Import players
for _, row in df.iterrows():

    cursor.execute(
        """
        SELECT team_id
        FROM teams
        WHERE team_name = %s
        """,
        (row["clean_team"],)
    )

    team_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO players (
            player_id,
            player_name,
            position,
            team_id
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (player_id)
        DO UPDATE SET
            player_name = EXCLUDED.player_name,
            position = EXCLUDED.position,
            team_id = EXCLUDED.team_id
        """,
        (
            int(row["id"]),
            row["player_name"],
            row["primary_position"],
            team_id
        )
    )

print(f"Processed {len(df)} players.")

# STEP 3: Import player statistics
# Remove existing statistics for this season so rerunning
# the script doesn't create duplicate season records.
seasons = df["season"].dropna().unique().tolist()

cursor.execute(
    """
    DELETE FROM player_stats
    WHERE season = ANY(%s)
    """,
    (seasons,)
)

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO player_stats (
            player_id,
            season,
            games,
            minutes_played,
            goals,
            assists,
            xg,
            xa,
            shots,
            key_passes,
            goals_per90,
            assists_per90,
            xg_per90,
            xa_per90
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
        """,
        (
            int(row["id"]),
            row["season"],
            int(row["games"]),
            int(row["time"]),
            int(row["goals"]),
            int(row["assists"]),
            float(row["xG"]),
            float(row["xA"]),
            int(row["shots"]),
            int(row["key_passes"]),
            float(row["goals_per90"]),
            float(row["assists_per90"]),
            float(row["xG_per90"]),
            float(row["xA_per90"])
        )
    )

# STEP 4: Remove team records that no players reference
cursor.execute("""
    DELETE FROM teams
    WHERE NOT EXISTS (
        SELECT 1
        FROM players
        WHERE players.team_id = teams.team_id
    );
""")

print(f"Removed {cursor.rowcount} unused team records.")
conn.commit()

print(f"Imported {len(df)} player statistics records.")
print("\nFootball data imported successfully!")

cursor.close()
conn.close()