
-- Football Analytics v2.0
-- Statistical Completeness Tests

WITH quality_issues AS (

    -- Normalized xG must never be NULL.
    SELECT
        'missing_normalized_xg' AS issue,
        match_id || ':' || player_id AS record_id
    FROM live.vw_normalized_player_match_stats
    WHERE normalized_xg IS NULL

    UNION ALL

    -- Zero shots + missing raw xG must normalize to zero.
    SELECT
        'incorrect_zero_shot_xg' AS issue,
        match_id || ':' || player_id AS record_id
    FROM live.vw_normalized_player_match_stats
    WHERE shots = 0
      AND expected_goals IS NULL
      AND normalized_xg IS DISTINCT FROM 0

    UNION ALL

    -- Players with missing xA must not receive
    -- an artificially complete xA aggregate.
    SELECT
        'incorrect_xa_aggregation' AS issue,
        p.player_id AS record_id
    FROM live.vw_player_performance p
    WHERE p.xa IS NOT NULL
      AND EXISTS (
          SELECT 1
          FROM live.player_match_stats s
          JOIN live.matches m
              ON s.match_id = m.match_id
          WHERE s.player_id = p.player_id
            AND s.team_id = p.team_id
            AND m.season_id = p.season
            AND s.minutes_played > 0
            AND s.expected_assists IS NULL
      )
)

SELECT *
FROM quality_issues;

-- Fail automatically if any statistical rule is violated.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM live.vw_normalized_player_match_stats
        WHERE normalized_xg IS NULL
           OR (
               shots = 0
               AND expected_goals IS NULL
               AND normalized_xg IS DISTINCT FROM 0
           )
    )
    OR EXISTS (
        SELECT 1
        FROM live.vw_player_performance p
        WHERE p.xa IS NOT NULL
          AND EXISTS (
              SELECT 1
              FROM live.player_match_stats s
              JOIN live.matches m
                  ON s.match_id = m.match_id
              WHERE s.player_id = p.player_id
                AND s.team_id = p.team_id
                AND m.season_id = p.season
                AND s.minutes_played > 0
                AND s.expected_assists IS NULL
          )
    )
    THEN
        RAISE EXCEPTION 'Statistical completeness checks failed';
    END IF;
END
$$;
