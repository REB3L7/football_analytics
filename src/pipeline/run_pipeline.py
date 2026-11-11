import argparse

from .api_client import SoccerDataClient
from .fetch_matches import fetch_all_matches
from .database import get_connection, match_exists
from .ingest_match import ingest_match
from .pipeline_logger import start_run, finish_run

def determine_run_status(successful, failed, rate_limited):
    if rate_limited:
        return "partial_success" if successful > 0 else "rate_limited"
    if failed:
        return "failed"
    return "success"

def run_pipeline(batch_size=5):
    run_id = start_run()

    discovered = 0
    successful = 0
    failed = 0
    total_players = 0
    error_message = None
    rate_limited = False

    print(f"Pipeline run ID: {run_id}")

    try:
        client = SoccerDataClient()

        print("Fetching finished matches...")
        matches = fetch_all_matches(client=client)
        discovered = len(matches)

        print(f"\nFound {discovered} finished matches.")

        with get_connection() as conn:
            with conn.cursor() as cursor:
                new_matches = [
                    match for match in matches
                    if not match_exists(cursor, match["id"])
                ]

        print(f"New matches available: {len(new_matches)}")

        batch = new_matches[:batch_size]

        for index, match in enumerate(batch, start=1):
            match_id = match["id"]
            home = match["home_team"]["name"]
            away = match["away_team"]["name"]

            print(
                f"\n[{index}/{len(batch)}] "
                f"{home} vs {away}"
            )

            try:
                players = client.get_player_stats(match_id)
                count = ingest_match(match, players)

                successful += 1
                total_players += count

                print(f"SUCCESS: {count} player records")

            except Exception as error:
                failed += 1
                error_message = f"{match_id}: {error}"
                print(f"FAILED: {error_message}")

                response = getattr(error, "response", None)

                if (
                    response is not None
                    and response.status_code == 429
                ):
                    rate_limited = True
                    retry_after = response.headers.get(
                        "Retry-After", "Unknown"
                    )

                    print("\nAPI RATE LIMIT REACHED")
                    print(f"Retry after: {retry_after} seconds")
                    print("Stopping pipeline.")
                    break

    except Exception as error:
        failed += 1
        error_message = str(error)

        response = getattr(error, "response", None)

        if response is not None and response.status_code == 429:
            rate_limited = True

            retry_after = response.headers.get(
                "Retry-After", "Unknown"
            )

            print("\nAPI RATE LIMIT REACHED DURING MATCH DISCOVERY")
            print(f"Retry after: {retry_after} seconds")
        else:
            print(f"\nPIPELINE ERROR: {error_message}")

    finally:
        status = determine_run_status(successful, failed, rate_limited)

        finish_run(
            run_id=run_id,
            status=status,
            matches_discovered=discovered,
            matches_processed=successful,
            matches_failed=failed,
            player_records_processed=total_players,
            error_message=error_message,
        )

        print("\n" + "=" * 45)
        print("PIPELINE SUMMARY")
        print("=" * 45)
        print("Run ID:", run_id)
        print("Status:", status)
        print("Matches discovered:", discovered)
        print("Successful matches:", successful)
        print("Failed matches:", failed)
        print("Player records processed:", total_players)

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Maximum number of new matches to ingest"
    )

    args = parser.parse_args()

    if args.batch_size < 1:
        parser.error("--batch-size must be at least 1")

    run_pipeline(batch_size=args.batch_size)
