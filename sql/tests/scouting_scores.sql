
-- Football Analytics v2.0
-- Synthetic scouting score regression test
-- Requires seed_scouting.sql in an isolated test database.

DO $$
DECLARE
    incorrect_scores INTEGER;
    actual_players INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO actual_players
    FROM live.vw_scouting_leaderboard
    WHERE season = 'test_season';

    IF actual_players <> 3 THEN
        RAISE EXCEPTION
            'Expected 3 synthetic forwards, found %',
            actual_players;
    END IF;

    WITH expected AS (
        SELECT *
        FROM (VALUES
            ('test_forward_1', 50.00::numeric,
             90.00::numeric, 15.00::numeric),
            ('test_forward_2', 50.00::numeric,
             50.00::numeric, 50.00::numeric),
            ('test_forward_3', 50.00::numeric,
             10.00::numeric, 85.00::numeric)
        ) AS v(
            player_id,
            all_round_score,
            goalscorer_score,
            creator_score
        )
    )
    SELECT COUNT(*)
    INTO incorrect_scores
    FROM expected e
    LEFT JOIN live.vw_scouting_leaderboard a
        ON a.player_id = e.player_id
        AND a.season = 'test_season'
    WHERE a.player_id IS NULL
       OR a.all_round_score IS DISTINCT FROM e.all_round_score
       OR a.goalscorer_score IS DISTINCT FROM e.goalscorer_score
       OR a.creator_score IS DISTINCT FROM e.creator_score;

    IF incorrect_scores > 0 THEN
        RAISE EXCEPTION
            'Scouting score regression: % incorrect players',
            incorrect_scores;
    END IF;

    RAISE NOTICE
        'PASS: All 3 synthetic players have correct scouting scores.';
END $$;
