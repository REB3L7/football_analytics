from .database import get_connection


def start_run():
    """Create a new pipeline run record."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO live.pipeline_runs (status)
                VALUES ('running')
                RETURNING run_id
                """
            )
            run_id = cursor.fetchone()[0]

    return run_id


def finish_run(
    run_id,
    status,
    matches_discovered=0,
    matches_processed=0,
    matches_failed=0,
    player_records_processed=0,
    error_message=None,
):
    """Update a pipeline run with its final results."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE live.pipeline_runs
                SET
                    finished_at = NOW(),
                    status = %s,
                    matches_discovered = %s,
                    matches_processed = %s,
                    matches_failed = %s,
                    player_records_processed = %s,
                    error_message = %s
                WHERE run_id = %s
                """,
                (
                    status,
                    matches_discovered,
                    matches_processed,
                    matches_failed,
                    player_records_processed,
                    error_message,
                    run_id,
                ),
            )
