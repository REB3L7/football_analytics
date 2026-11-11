-- Football Analytics v2.0
-- Live Specialized Scouting which preserves original v1.0 scoring weights

CREATE OR REPLACE VIEW live.vw_specialized_scouting AS

SELECT
    player_id,
    player_name,
    team_name,
    season,
    minutes_played,

    scouting_score AS all_round_score,

    ROUND((
        goals_percentile * 0.35 +
        xg_percentile * 0.35 +
        shots_percentile * 0.20 +
        assists_percentile * 0.05 +
        xa_percentile * 0.05
    ), 2) AS goalscorer_score,

    ROUND((
        assists_percentile * 0.30 +
        xa_percentile * 0.30 +
        key_passes_percentile * 0.25 +
        goals_percentile * 0.10 +
        xg_percentile * 0.05
    ), 2) AS creator_score

FROM live.vw_forward_scouting;
