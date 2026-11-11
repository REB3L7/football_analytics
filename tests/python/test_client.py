
from src.pipeline.api_client import SoccerDataClient

client = SoccerDataClient()

matches = client.get_matches(
    team_id="team_f0ibhxdw7hs5",
    status="finished"
)

print(f"Matches retrieved: {len(matches)}")

if matches:
    match = matches[0]

    print("Match ID:", match["id"])
    print("Competition:", match["competition_id"])
    print("Season:", match["season_id"])

    players = client.get_player_stats(match["id"])

    print("Player records:", len(players))
