import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

if not API_KEY:
    raise ValueError("API_FOOTBALL_KEY is missing")

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "league": 39,
    "season": 2024,
    "date": "2025-05-25"
}

response = requests.get(
    f"{BASE_URL}/fixtures",
    headers=headers,
    params=params,
    timeout=20
)

response.raise_for_status()
data = response.json()

if data.get("errors"):
    raise RuntimeError(f"API error: {data['errors']}")

fixtures = data.get("response", [])

print(f"\nFound {len(fixtures)} completed matches:\n")

for match in fixtures:
    fixture = match["fixture"]
    teams = match["teams"]
    goals = match["goals"]

    print(
        f"Fixture ID: {fixture['id']} | "
        f"{teams['home']['name']} {goals['home']} - "
        f"{goals['away']} {teams['away']['name']} | "
        f"{fixture['date']}"
    )
