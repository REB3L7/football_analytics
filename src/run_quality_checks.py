import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEST_FILES = [
    "sql/tests/scouting_leaderboard.sql",
    "sql/tests/ingestion_integrity.sql",
    "sql/tests/statistical_completeness.sql",
]

SCOUTING_TEST = "sql/tests/scouting_scores.sql"


def run_tests():
    database = os.getenv("PGDATABASE", "football_analytics")
    include_scouting = os.getenv("RUN_SCOUTING_TESTS") == "1"

    tests = TEST_FILES.copy()

    if include_scouting:
        tests.append(SCOUTING_TEST)

    print("\nFOOTBALL ANALYTICS - DATA QUALITY CHECKS")
    print("=" * 45)
    print(f"Database: {database}")
    print(f"Synthetic scoring test: {'enabled' if include_scouting else 'disabled'}")

    failed_tests = []

    for test_file in tests:
        test_path = PROJECT_ROOT / test_file
        print(f"\nRunning: {test_file}", flush=True)

        result = subprocess.run(
            [
                "psql",
                "-X",
                "-v",
                "ON_ERROR_STOP=1",
                "-d",
                database,
                "-P",
                "pager=off",
                "-f",
                str(test_path),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("PASS")
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
        else:
            print("FAIL")
            print(result.stderr)
            failed_tests.append(test_file)

    print("=" * 45)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {len(tests) - len(failed_tests)}")
    print(f"Failed: {len(failed_tests)}")

    return 1 if failed_tests else 0


if __name__ == "__main__":
    sys.exit(run_tests())
