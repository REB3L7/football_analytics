
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SQL_FILES = [
    "sql/schema/live_schema.sql",
    "sql/schema/pipeline_runs.sql",
    "sql/models/normalized_player_match_stats.sql",
    "sql/models/player_data_completeness.sql",
    "sql/models/scouting_readiness.sql",
    "sql/models/team_scouting_readiness.sql",
    "sql/models/live_player_performance.sql",
    "sql/models/live_forward_scouting.sql",
    "sql/models/live_specialized_scouting.sql",
    "sql/models/live_scouting_leaderboard.sql",
]


def initialize_database():
    database = os.getenv("PGDATABASE", "football_analytics")

    print(f"Initializing database: {database}", flush=True)
    print("=" * 50, flush=True)

    for index, relative_path in enumerate(SQL_FILES, start=1):
        sql_path = PROJECT_ROOT / relative_path

        if not sql_path.is_file():
            print(f"Missing SQL file: {sql_path}", file=sys.stderr)
            return 1

        print(
            f"[{index}/{len(SQL_FILES)}] {relative_path}",
            flush=True,
        )

        result = subprocess.run(
            [
                "psql",
                "-X",
                "-v",
                "ON_ERROR_STOP=1",
                "-d",
                database,
                "-f",
                str(sql_path),
            ],
            check=False,
        )

        if result.returncode != 0:
            print(
                f"FAILED: {relative_path}",
                file=sys.stderr,
            )
            return result.returncode

    print("=" * 50)
    print("Database initialization completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(initialize_database())
