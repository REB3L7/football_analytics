-- Football Analytics v2.0
-- Normalized Player Match Statistics
--
-- Preserve raw API data in live.player_match_stats.
-- Normalize missing xG only when shots = 0.

CREATE OR REPLACE VIEW live.vw_normalized_player_match_stats AS
SELECT
    s.*,

    CASE
        WHEN s.shots = 0
             AND s.expected_goals IS NULL
        THEN 0::NUMERIC(8,3)
        ELSE s.expected_goals
    END AS normalized_xg,

    CASE
        WHEN s.shots = 0
             AND s.expected_goals IS NULL
        THEN TRUE
        ELSE FALSE
    END AS xg_imputed

FROM live.player_match_stats s;
