from .api_client import SoccerDataClient

COMPETITION_ID = "competition_705uv6jm8myn"
SEASON_ID = "season_hr1ie7yrsdmt"

PAGE_SIZE = 20
MAX_PAGES = 30


def fetch_all_matches(client=None):
    if client is None:
        client = SoccerDataClient()

    all_matches = []
    seen_ids = set()

    for page in range(1, MAX_PAGES + 1):
        payload = client.get_matches(
            include_meta=True,
            competition_id=COMPETITION_ID,
            season_id=SEASON_ID,
            status="finished",
            page=page
        )

        matches = payload["data"]
        meta = payload["meta"]
        total_pages = int(meta["total_pages"])

        if total_pages < 1 or total_pages > MAX_PAGES:
            raise ValueError(
                f"Invalid total_pages: {total_pages}"
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
            f"Page {page}/{total_pages}: "
            f"{len(matches)} returned, "
            f"{new_count} new"
        )

        if page >= total_pages:
            break

        if new_count == 0:
            raise RuntimeError(
                f"Pagination made no progress on page {page}"
            )

    return all_matches


if __name__ == "__main__":
    matches = fetch_all_matches()
    print(f"\nTotal matches fetched: {len(matches)}")
