import psycopg
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Connect to PostgreSQL
conn = psycopg.connect(
    dbname="football_analytics",
    user="roti",
    host="localhost",
    port=5432
)

cursor = conn.cursor()

# Create teams table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) UNIQUE NOT NULL
);
""")

# Create players table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    player_name VARCHAR(150) NOT NULL,
    position VARCHAR(50),
    team_id INTEGER REFERENCES teams(team_id)
);
""")

# Create player statistics table
cursor.execute("""
CREATE TABLE IF NOT EXISTS player_stats (
    stat_id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(player_id),
    season VARCHAR(20),
    games INTEGER,
    minutes_played INTEGER,
    goals INTEGER,
    assists INTEGER,
    xg FLOAT,
    xa FLOAT,
    shots INTEGER,
    key_passes INTEGER,
    goals_per90 FLOAT,
    assists_per90 FLOAT,
    xg_per90 FLOAT,
    xa_per90 FLOAT
);
""")

conn.commit()

print("\nDatabase tables created successfully!")

cursor.close()
conn.close()