-- Football Analytics v2.0
-- Data Quality Checks

SELECT
    'duplicate_matches' AS check_name,
    COUNT(*) AS issues
FROM (
    SELECT match_id
    FROM live.matches
    GROUP BY match_id
    HAVING COUNT(*) > 1
) duplicates

UNION ALL

SELECT
    'duplicate_player_match_stats',
    COUNT(*)
FROM (
    SELECT match_id, player_id
    FROM live.player_match_stats
    GROUP BY match_id, player_id
    HAVING COUNT(*) > 1
) duplicates

UNION ALL

SELECT
    'invalid_minutes',
    COUNT(*)
FROM live.player_match_stats
WHERE minutes_played < 0
   OR minutes_played > 130

UNION ALL

SELECT
    'missing_player_references',
    COUNT(*)
FROM live.player_match_stats s
LEFT JOIN live.players p
    ON s.player_id = p.player_id
WHERE p.player_id IS NULL

UNION ALL

SELECT
    'missing_match_references',
    COUNT(*)
FROM live.player_match_stats s
LEFT JOIN live.matches m
    ON s.match_id = m.match_id
WHERE m.match_id IS NULL

ORDER BY check_name;
