
from src.pipeline.fetch_matches import fetch_all_matches
from src.pipeline.api_client import SoccerDataClient

client = SoccerDataClient()

matches = fetch_all_matches()

# Start with only 3 matches
test_matches = matches[:3]

print("\nTEST BATCH")
print("-" * 50)

for match in test_matches:
    match_id = match["id"]

    home = match["home_team"]["name"]
    away = match["away_team"]["name"]

    print(f"\nMatch: {home} vs {away}")
    print("Match ID:", match_id)

    try:
        players = client.get_player_stats(match_id)

        if not isinstance(players, list):
            raise ValueError("Unexpected player stats format")

        team_ids = {
            match["home_team"]["id"],
            match["away_team"]["id"]
        }

        invalid_players = [
            p for p in players
            if p.get("team_id") not in team_ids
        ]

        print("Player records:", len(players))
        print("Invalid team assignments:", len(invalid_players))

        if invalid_players:
            print("WARNING: Player team IDs do not match fixture teams")

    except Exception as error:
        print("ERROR:", error)

print("\nBatch validation finished.")
