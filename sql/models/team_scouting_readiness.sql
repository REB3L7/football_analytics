
-- Football Analytics v2.0
-- Team-Specific Scouting Readiness

CREATE OR REPLACE VIEW live.vw_team_scouting_readiness AS

SELECT
    s.player_id,
    s.team_id,
    m.season_id,

    COUNT(*) FILTER (
        WHERE s.minutes_played > 0
    ) AS appearances,

    COALESCE(SUM(s.minutes_played), 0)
        AS total_minutes,

    COUNT(*) FILTER (
        WHERE s.minutes_played > 0
          AND s.expected_assists IS NULL
    ) AS missing_xa_appearances,

    BOOL_AND(
        s.minutes_played IS NOT NULL
        AND (
            s.minutes_played = 0
            OR s.expected_assists IS NOT NULL
        )
    ) AS xa_complete,

    (
        COALESCE(SUM(s.minutes_played), 0) >= 270
        AND BOOL_AND(
            s.minutes_played IS NOT NULL
            AND (
                s.minutes_played = 0
                OR s.expected_assists IS NOT NULL
            )
        )
    ) AS ready_for_scouting

FROM live.player_match_stats s

JOIN live.matches m
    ON s.match_id = m.match_id

GROUP BY
    s.player_id,
    s.team_id,
    m.season_id;
