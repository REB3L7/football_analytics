CREATE OR REPLACE VIEW vw_player_performance AS
SELECT
    p.player_id,
    p.player_name,
    p.position,
    t.team_name,
    s.season,
    s.games,
    s.minutes_played,
    s.goals,
    s.assists,
    ROUND(s.xg::numeric, 2) AS xg,
    ROUND(s.xa::numeric, 2) AS xa,
    s.shots,
    s.key_passes,
    ROUND(s.goals_per90::numeric, 3) AS goals_per90,
    ROUND(s.assists_per90::numeric, 3) AS assists_per90,
    ROUND(s.xg_per90::numeric, 3) AS xg_per90,
    ROUND(s.xa_per90::numeric, 3) AS xa_per90,
    ROUND((s.goals - s.xg)::numeric, 2) AS goals_minus_xg
FROM players p
JOIN teams t ON p.team_id = t.team_id
JOIN player_stats s ON p.player_id = s.player_id;
