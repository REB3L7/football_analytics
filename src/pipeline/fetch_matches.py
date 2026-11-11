from .api_client import SoccerDataClient

COMPETITION_ID = "competition_705uv6jm8myn"
SEASON_ID = "season_hr1ie7yrsdmt"

PAGE_SIZE = 20
MAX_PAGES = 30


def fetch_all_matches():
    client = SoccerDataClient()

    all_matches = []
    seen_ids = set()

    for page in range(1, MAX_PAGES + 1):
        matches = client.get_matches(
            competition_id=COMPETITION_ID,
            season_id=SEASON_ID,
            status="finished",
            page=page
        )

        if not matches:
            break

        new_count = 0

        for match in matches:
            match_id = match["id"]

            if match_id in seen_ids:
                continue

            seen_ids.add(match_id)
            all_matches.append(match)
            new_count += 1

        print(
            f"Page {page}: "
            f"{len(matches)} returned, "
            f"{new_count} new"
        )

        if new_count == 0 or len(matches) < PAGE_SIZE:
            break
    else:
        raise RuntimeError(
            "Maximum pagination limit reached. "
            "Check whether more pages are available."
        )

    return all_matches


if __name__ == "__main__":
    matches = fetch_all_matches()

    print(f"\nTotal matches fetched: {len(matches)}")
