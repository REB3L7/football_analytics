-- Football Analytics v2.0
-- Automated Scouting Leaderboard Quality Test
-- Returns zero rows when all checks pass.

WITH quality_issues AS (

    SELECT
        'invalid_score' AS issue,
        player_id
    FROM live.vw_scouting_leaderboard
    WHERE all_round_score NOT BETWEEN 0 AND 100
       OR goalscorer_score NOT BETWEEN 0 AND 100
       OR creator_score NOT BETWEEN 0 AND 100
       OR all_round_score IS NULL
       OR goalscorer_score IS NULL
       OR creator_score IS NULL

    UNION ALL

    SELECT
        'invalid_rank' AS issue,
        player_id
    FROM live.vw_scouting_leaderboard
    WHERE all_round_rank < 1
       OR goalscorer_rank < 1
       OR creator_rank < 1
       OR all_round_rank IS NULL
       OR goalscorer_rank IS NULL
       OR creator_rank IS NULL

    UNION ALL

    SELECT
        'duplicate_player_team_season' AS issue,
        player_id
    FROM live.vw_scouting_leaderboard
    GROUP BY player_id, team_name, season
    HAVING COUNT(*) > 1
)

SELECT *
FROM quality_issues;

-- Fail the test if any quality issues were found.
SELECT 1 / CASE
    WHEN EXISTS (
        SELECT 1
        FROM live.vw_scouting_leaderboard
        WHERE all_round_score IS NULL
           OR goalscorer_score IS NULL
           OR creator_score IS NULL
           OR all_round_score NOT BETWEEN 0 AND 100
           OR goalscorer_score NOT BETWEEN 0 AND 100
           OR creator_score NOT BETWEEN 0 AND 100
           OR all_round_rank IS NULL
           OR goalscorer_rank IS NULL
           OR creator_rank IS NULL
           OR all_round_rank < 1
           OR goalscorer_rank < 1
           OR creator_rank < 1
    )
    OR EXISTS (
        SELECT 1
        FROM live.vw_scouting_leaderboard
        GROUP BY player_id, team_name, season
        HAVING COUNT(*) > 1
    )
    THEN 0
    ELSE 1
END AS quality_test_passed;