
from src.pipeline.api_client import SoccerDataClient

client = SoccerDataClient()

competition_id = "competition_705uv6jm8myn"
season_id = "season_hr1ie7yrsdmt"

matches = client.get_matches(
    competition_id=competition_id,
    season_id=season_id,
    status="finished"
)

print("Matches returned:", len(matches))

for match in matches[:10]:
    home = match["home_team"]["name"]
    away = match["away_team"]["name"]

    print(
        f"Matchday {match.get('matchday')}: "
        f"{home} vs {away}"
    )
