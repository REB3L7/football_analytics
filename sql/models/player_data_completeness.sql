-- Football Analytics v2.0
-- Player Data Completeness

CREATE OR REPLACE VIEW live.vw_player_data_completeness AS

SELECT
    p.player_id,
    p.player_name,
    p.position,
    m.season_id,

    COUNT(*) FILTER (
        WHERE s.minutes_played > 0
    ) AS appearances,

    COALESCE(
        SUM(s.minutes_played),
        0
    ) AS total_minutes,

    COUNT(*) FILTER (
        WHERE s.minutes_played > 0
          AND s.expected_assists IS NULL
    ) AS missing_xa_appearances,

    COUNT(*) FILTER (
        WHERE s.minutes_played > 0
          AND s.xg_imputed
    ) AS normalized_xg_appearances,

    BOOL_AND(
        s.minutes_played IS NOT NULL
        AND (
            s.minutes_played = 0
            OR s.expected_assists IS NOT NULL
        )
    ) AS xa_complete,

    COALESCE(
        SUM(s.minutes_played),
        0
    ) >= 270 AS meets_minutes_threshold

FROM live.vw_normalized_player_match_stats s

JOIN live.players p
    ON s.player_id = p.player_id

JOIN live.matches m
    ON s.match_id = m.match_id

GROUP BY
    p.player_id,
    p.player_name,
    p.position,
    m.season_id;
