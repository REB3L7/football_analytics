
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SOCCER_DATA_KEY")

if not api_key:
    raise ValueError("SOCCER_DATA_KEY is missing from .env")

url = "https://api.soccer-data.co/v1/matches"

params = {
    "team_id": "team_f0ibhxdw7hs5",
    "status": "finished"
}

response = requests.get(
    url,
    headers={"X-Api-Key": api_key},
    params=params,
    timeout=20
)

print("HTTP status:", response.status_code)
response.raise_for_status()

payload = response.json()
matches = payload.get("data", [])

print("Matches returned:", len(matches))


import json

if matches:
    match = matches[0]

    print("\nMATCH KEYS:")
    print(list(match.keys()))

    print("\nMATCH DETAILS:")
    print(json.dumps(match, indent=2))

else:
    print("No matches returned.")


print("\nCOMPETITION AND SEASON:")

if matches:
    match = matches[0]

    print("Competition ID:", match.get("competition_id"))
    print("Season ID:", match.get("season_id"))
    print("Matchday:", match.get("matchday"))
    print("Match date:", match.get("utc_date"))
    print("Match status:", match.get("status"))
