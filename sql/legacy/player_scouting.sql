CREATE OR REPLACE VIEW live.player_scouting AS

SELECT
    p.player_id,
    p.player_name,
    p.position,

    COUNT(DISTINCT s.match_id) AS appearances,

    SUM(COALESCE(s.minutes_played, 0)) AS minutes_played,

    SUM(COALESCE(s.goals, 0)) AS goals,
    SUM(COALESCE(s.assists, 0)) AS assists,

    ROUND(SUM(s.expected_goals), 2) AS expected_goals,
    ROUND(SUM(s.expected_assists), 2) AS expected_assists,

    SUM(COALESCE(s.shots, 0)) AS shots,
    SUM(COALESCE(s.shots_on_target, 0)) AS shots_on_target,

    SUM(COALESCE(s.key_passes, 0)) AS key_passes,
    SUM(COALESCE(s.tackles, 0)) AS tackles,
    SUM(COALESCE(s.interceptions, 0)) AS interceptions,

    ROUND(AVG(s.rating), 2) AS average_rating,

    ROUND(
        SUM(COALESCE(s.goals, 0)) * 90.0 /
        NULLIF(SUM(COALESCE(s.minutes_played, 0)), 0),
        2
    ) AS goals_per_90,

    ROUND(
        SUM(COALESCE(s.assists, 0)) * 90.0 /
        NULLIF(SUM(COALESCE(s.minutes_played, 0)), 0),
        2
    ) AS assists_per_90

FROM live.player_match_stats s

JOIN live.players p
    ON s.player_id = p.player_id

GROUP BY
    p.player_id,
    p.player_name,
    p.position;
