-- Football Analytics v2.0
-- Synthetic scouting test fixtures
-- Run ONLY against an isolated test database.

BEGIN;

INSERT INTO live.matches (
    match_id, competition_id, season_id, matchday,
    match_date, status,
    home_team_id, home_team_name,
    away_team_id, away_team_name,
    home_score, away_score
)
SELECT
    'test_match_' || n,
    'test_competition',
    'test_season',
    n,
    TIMESTAMPTZ '2026-01-01 12:00:00+00'
        + (n * INTERVAL '7 days'),
    'finished',
    'test_team_home',
    'Test United',
    'test_team_away',
    'Test City',
    3, 2
FROM generate_series(1, 3) AS n;

INSERT INTO live.players (
    player_id, player_name, position
)
VALUES
    ('test_forward_1', 'Test Goalscorer', 'F'),
    ('test_forward_2', 'Test Balanced', 'F'),
    ('test_forward_3', 'Test Creator', 'F');

INSERT INTO live.player_match_stats (
    match_id, player_id, team_id,
    minutes_played, goals, assists,
    expected_goals, expected_assists,
    shots, shots_on_target, key_passes,
    tackles, interceptions, rating
)
SELECT
    'test_match_' || n,
    p.player_id,
    'test_team_home',
    90,
    p.goals,
    p.assists,
    p.xg,
    p.xa,
    p.shots,
    p.shots_on_target,
    p.key_passes,
    0,
    0,
    7.50
FROM generate_series(1, 3) AS n
CROSS JOIN (
    VALUES
        ('test_forward_1', 2, 0, 1.5::numeric, 0.1::numeric, 5, 3, 1),
        ('test_forward_2', 1, 1, 1.0::numeric, 0.5::numeric, 3, 2, 3),
        ('test_forward_3', 0, 2, 0.5::numeric, 1.0::numeric, 1, 1, 5)
) AS p(
    player_id, goals, assists, xg, xa,
    shots, shots_on_target, key_passes
);

COMMIT;
