CREATE OR REPLACE VIEW vw_scouting_leaderboard AS
SELECT
    player_id,
    player_name,
    team_name,
    season,
    minutes_played,

    all_round_score,
    goalscorer_score,
    creator_score,

    RANK() OVER (
        PARTITION BY season
        ORDER BY all_round_score DESC
    ) AS all_round_rank,

    RANK() OVER (
        PARTITION BY season
        ORDER BY goalscorer_score DESC
    ) AS goalscorer_rank,

    RANK() OVER (
        PARTITION BY season
        ORDER BY creator_score DESC
    ) AS creator_rank

FROM vw_specialized_scouting;