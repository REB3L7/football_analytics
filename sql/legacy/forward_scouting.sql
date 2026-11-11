CREATE OR REPLACE VIEW vw_forward_scouting AS

WITH qualified_forwards AS (
    SELECT
        p.player_id,
        p.player_name,
        t.team_name,
        s.season,
        s.minutes_played,

        s.goals_per90,
        s.assists_per90,
        s.xg_per90,
        s.xa_per90,

        s.shots * 90.0 / NULLIF(s.minutes_played, 0)
            AS shots_per90,

        s.key_passes * 90.0 / NULLIF(s.minutes_played, 0)
            AS key_passes_per90

    FROM players p

    JOIN teams t
        ON p.team_id = t.team_id

    JOIN player_stats s
        ON p.player_id = s.player_id

    WHERE p.position = 'F'
      AND s.minutes_played >= 270
),

percentile_scores AS (
    SELECT
        *,

        PERCENT_RANK() OVER (
            PARTITION BY season
            ORDER BY goals_per90
        ) * 100 AS goals_percentile,

        PERCENT_RANK() OVER (
            PARTITION BY season
            ORDER BY assists_per90
        ) * 100 AS assists_percentile,

        PERCENT_RANK() OVER (
            PARTITION BY season
            ORDER BY xg_per90
        ) * 100 AS xg_percentile,

        PERCENT_RANK() OVER (
            PARTITION BY season
            ORDER BY xa_per90
        ) * 100 AS xa_percentile,

        PERCENT_RANK() OVER (
            PARTITION BY season
            ORDER BY shots_per90
        ) * 100 AS shots_percentile,

        PERCENT_RANK() OVER (
            PARTITION BY season
            ORDER BY key_passes_per90
        ) * 100 AS key_passes_percentile

    FROM qualified_forwards
)

SELECT
    player_id,
    player_name,
    team_name,
    season,
    minutes_played,

    ROUND(goals_percentile::numeric, 1)
        AS goals_percentile,

    ROUND(assists_percentile::numeric, 1)
        AS assists_percentile,

    ROUND(xg_percentile::numeric, 1)
        AS xg_percentile,

    ROUND(xa_percentile::numeric, 1)
        AS xa_percentile,

    ROUND(shots_percentile::numeric, 1)
        AS shots_percentile,

    ROUND(key_passes_percentile::numeric, 1)
        AS key_passes_percentile,

    ROUND((
        goals_percentile +
        assists_percentile +
        xg_percentile +
        xa_percentile +
        shots_percentile +
        key_passes_percentile
    )::numeric / 6, 2) AS scouting_score

FROM percentile_scores;