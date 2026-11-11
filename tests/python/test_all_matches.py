
from src.pipeline.api_client import SoccerDataClient

client = SoccerDataClient()

all_matches = []
seen_ids = set()

page = 1
MAX_PAGES = 30

while page <= MAX_PAGES:
    matches = client.get_matches(
        competition_id="competition_705uv6jm8myn",
        season_id="season_hr1ie7yrsdmt",
        status="finished",
        page=page
    )

    if not matches:
        print(f"Page {page}: No more matches.")
        break

    new_matches = [
        match for match in matches
        if match["id"] not in seen_ids
    ]

    print(
        f"Page {page}: "
        f"{len(matches)} returned, "
        f"{len(new_matches)} new"
    )

    if not new_matches:
        print("No new match IDs. Stopping.")
        break

    for match in new_matches:
        seen_ids.add(match["id"])
        all_matches.append(match)

    if len(matches) < 20:
        print("Final partial page reached.")
        break

    page += 1

print("\nTotal unique matches:", len(all_matches))

if all_matches:
    dates = [
        match["utc_date"]
        for match in all_matches
        if match.get("utc_date")
    ]

    if dates:
        print("Earliest match:", min(dates))
        print("Latest match:", max(dates))

    print(
        "Matchdays:",
        sorted({
            match["matchday"]
            for match in all_matches
            if match.get("matchday") is not None
        })
    )
