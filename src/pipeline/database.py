
import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="football_analytics"
    )


def match_exists(cursor, match_id):
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM live.matches
            WHERE match_id = %s
        )
        """,
        (match_id,)
    )

    return cursor.fetchone()[0]
