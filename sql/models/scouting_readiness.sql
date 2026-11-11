-- Football Analytics v2.0
-- Scouting Readiness

CREATE OR REPLACE VIEW live.vw_scouting_readiness AS

SELECT
    player_id,
    player_name,
    position,
    season_id,
    appearances,
    total_minutes,
    missing_xa_appearances,
    normalized_xg_appearances,
    xa_complete,
    meets_minutes_threshold,

    (
        position = 'F'
        AND xa_complete
        AND meets_minutes_threshold
    ) AS ready_for_scouting

FROM live.vw_player_data_completeness;
