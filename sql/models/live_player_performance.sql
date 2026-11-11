CREATE OR REPLACE VIEW live.vw_player_performance AS

WITH player_team_stats AS (
    SELECT
        s.player_id,
        s.team_id,
        m.season_id,

        COUNT(DISTINCT s.match_id) AS games,

        SUM(COALESCE(s.minutes_played, 0)) AS minutes_played,
        SUM(COALESCE(s.goals, 0)) AS goals,
        SUM(COALESCE(s.assists, 0)) AS assists,

        SUM(s.normalized_xg) AS xg,
        CASE
            WHEN COUNT(*) FILTER (
                WHERE s.minutes_played > 0
                AND s.expected_assists IS NULL
            ) > 0
            THEN NULL
            ELSE SUM(s.expected_assists)
        END AS xa,

        SUM(COALESCE(s.shots, 0)) AS shots,
        SUM(COALESCE(s.key_passes, 0)) AS key_passes

    FROM live.vw_normalized_player_match_stats s

    JOIN live.matches m
        ON s.match_id = m.match_id

    GROUP BY
        s.player_id,
        s.team_id,
        m.season_id
)

SELECT
    p.player_id,
    p.player_name,
    p.position,

    COALESCE(
        CASE
            WHEN pts.team_id = m.home_team_id
            THEN m.home_team_name
            ELSE m.away_team_name
        END,
        pts.team_id
    ) AS team_name,

    pts.season_id AS season,
    pts.games,
    pts.minutes_played,
    pts.goals,
    pts.assists,

    ROUND(pts.xg, 2) AS xg,
    ROUND(pts.xa, 2) AS xa,

    pts.shots,
    pts.key_passes,

    ROUND(
        pts.goals * 90.0 /
        NULLIF(pts.minutes_played, 0),
        3
    ) AS goals_per90,

    ROUND(
        pts.assists * 90.0 /
        NULLIF(pts.minutes_played, 0),
        3
    ) AS assists_per90,

    ROUND(
        pts.xg * 90.0 /
        NULLIF(pts.minutes_played, 0),
        3
    ) AS xg_per90,

    ROUND(
        pts.xa * 90.0 /
        NULLIF(pts.minutes_played, 0),
        3
    ) AS xa_per90,

    ROUND(pts.goals - pts.xg, 2) AS goals_minus_xg,
    pts.team_id AS team_id

FROM player_team_stats pts

JOIN live.players p
    ON pts.player_id = p.player_id

LEFT JOIN LATERAL (
    SELECT
        m.home_team_id,
        m.home_team_name,
        m.away_team_name
    FROM live.player_match_stats s
    JOIN live.matches m
        ON s.match_id = m.match_id
    WHERE s.player_id = pts.player_id
      AND s.team_id = pts.team_id
      AND m.season_id = pts.season_id
    ORDER BY m.match_date DESC NULLS LAST, m.match_id DESC
    LIMIT 1
) m ON TRUE;
