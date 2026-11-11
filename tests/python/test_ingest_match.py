
from src.pipeline.api_client import SoccerDataClient
from src.pipeline.fetch_matches import fetch_all_matches
from src.pipeline.ingest_match import ingest_match

client = SoccerDataClient()

matches = fetch_all_matches()

# Test one match we haven't ingested yet
match = next(
    m for m in matches
    if m["id"] == "match_finivel2w2bm"
)

players = client.get_player_stats(match["id"])

count = ingest_match(match, players)

print("\nSuccessfully ingested:")
print(match["home_team"]["name"],
      "vs", match["away_team"]["name"])
print("Player records:", count)
