
from src.pipeline.database import get_connection, match_exists

with get_connection() as conn:
    with conn.cursor() as cursor:

        existing = match_exists(
            cursor,
            "match_23fe4epspue0"
        )

        missing = match_exists(
            cursor,
            "match_nonexistent_test"
        )

        print("Arsenal match exists:", existing)
        print("Fake match exists:", missing)
