-- Football Analytics v2.0
-- Live Forward Scouting
-- Preserves the original v1.0 scoring methodology

CREATE OR REPLACE VIEW live.vw_forward_scouting AS

WITH qualified_forwards AS (
    SELECT
        p.player_id,
        p.player_name,
        p.team_name,
        p.season,
        p.minutes_played,

        p.goals_per90,
        p.assists_per90,
        p.xg_per90,
        p.xa_per90,

        p.shots * 90.0 / NULLIF(p.minutes_played, 0)
            AS shots_per90,

        p.key_passes * 90.0 / NULLIF(p.minutes_played, 0)
            AS key_passes_per90

    FROM live.vw_player_performance p

    JOIN live.vw_team_scouting_readiness r
        ON p.player_id = r.player_id
        AND p.team_id = r.team_id
        AND p.season = r.season_id

    WHERE p.position = 'F'
      AND p.minutes_played >= 270
      AND r.ready_for_scouting = TRUE
      AND p.xg_per90 IS NOT NULL
      AND p.xa_per90 IS NOT NULL
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
