
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SOCCER_DATA_KEY")

if not API_KEY:
    raise ValueError("SOCCER_DATA_KEY is missing from .env")

BASE_URL = "https://api.soccer-data.co/v1"

match_id = "match_23fe4epspue0"

url = f"{BASE_URL}/matches/{match_id}/player-stats"

response = requests.get(
    url,
    headers={"X-Api-Key": API_KEY},
    timeout=20
)

print("HTTP status:", response.status_code)

response.raise_for_status()

data = response.json()


players = data.get("data", [])

print(f"\nTotal player records: {len(players)}")

xg_available = 0
xa_available = 0

for player in players:
    shooting = player.get("shooting") or {}

    if shooting.get("expected_goals") is not None:
        xg_available += 1

    if shooting.get("expected_assists") is not None:
        xa_available += 1

print(f"Players with xG: {xg_available}")
print(f"Players with xA: {xa_available}")

print("\nPLAYERS BY TEAM:")

teams = {}

for player in players:
    team_id = player.get("team_id", "Unknown")
    teams[team_id] = teams.get(team_id, 0) + 1

for team_id, count in teams.items():
    print(f"{team_id}: {count} players")

print("\nSAMPLE PLAYER STATISTICS:")

for player in players[:10]:
    shooting = player.get("shooting") or {}

    print(
        f"{player.get('player_name')} | "
        f"Minutes: {player.get('minutes_played')} | "
        f"xG: {shooting.get('expected_goals')} | "
        f"xA: {shooting.get('expected_assists')}"
    )