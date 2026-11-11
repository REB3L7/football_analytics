
from src.pipeline.api_client import SoccerDataClient

client = SoccerDataClient()

base_params = {
    "competition_id": "competition_705uv6jm8myn",
    "season_id": "season_hr1ie7yrsdmt",
    "status": "finished"
}

for page in [1, 2, 3]:
    matches = client.get_matches(
        **base_params,
        page=page
    )

    print(f"\nPage {page}")
    print("Matches returned:", len(matches))

    if matches:
        print("First match ID:", matches[0]["id"])
        print("Last match ID:", matches[-1]["id"])
