
-- Football Analytics v2.0
-- Ingestion Integrity Tests
-- Detect duplicate records, broken references,
-- and invalid playing time.

WITH quality_issues AS (

    -- Duplicate matches
    SELECT
        'duplicate_match' AS issue,
        match_id AS record_id
    FROM live.matches
    GROUP BY match_id
    HAVING COUNT(*) > 1

    UNION ALL

    -- Duplicate player-match records
    SELECT
        'duplicate_player_match' AS issue,
        match_id || ':' || player_id AS record_id
    FROM live.player_match_stats
    GROUP BY match_id, player_id
    HAVING COUNT(*) > 1

    UNION ALL

    -- Missing player references
    SELECT
        'missing_player' AS issue,
        s.player_id AS record_id
    FROM live.player_match_stats s
    LEFT JOIN live.players p
        ON s.player_id = p.player_id
    WHERE p.player_id IS NULL

    UNION ALL

    -- Missing match references
    SELECT
        'missing_match' AS issue,
        s.match_id AS record_id
    FROM live.player_match_stats s
    LEFT JOIN live.matches m
        ON s.match_id = m.match_id
    WHERE m.match_id IS NULL

    UNION ALL

    -- Invalid playing time
    SELECT
        'invalid_minutes' AS issue,
        match_id || ':' || player_id AS record_id
    FROM live.player_match_stats
    WHERE minutes_played < 0
       OR minutes_played > 130
)

SELECT *
FROM quality_issues;

-- Return a nonzero exit status when any issue exists.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM live.player_match_stats
        WHERE minutes_played < 0
           OR minutes_played > 130
    )
    OR EXISTS (
        SELECT 1
        FROM live.player_match_stats s
        LEFT JOIN live.players p
            ON s.player_id = p.player_id
        LEFT JOIN live.matches m
            ON s.match_id = m.match_id
        WHERE p.player_id IS NULL
           OR m.match_id IS NULL
    )
    OR EXISTS (
        SELECT 1 FROM (
            SELECT match_id
            FROM live.matches
            GROUP BY match_id
            HAVING COUNT(*) > 1
        ) duplicates
    )
    OR EXISTS (
        SELECT 1 FROM (
            SELECT match_id, player_id
            FROM live.player_match_stats
            GROUP BY match_id, player_id
            HAVING COUNT(*) > 1
        ) duplicates
    )
    THEN
        RAISE EXCEPTION 'Ingestion integrity checks failed';
    END IF;
END
$$;
