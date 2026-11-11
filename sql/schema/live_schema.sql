CREATE SCHEMA IF NOT EXISTS live;
SET search_path TO live, public;

CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    competition_id TEXT NOT NULL,
    season_id TEXT NOT NULL,
    matchday INTEGER,
    match_date TIMESTAMPTZ,
    status TEXT NOT NULL,
    home_team_id TEXT NOT NULL,
    home_team_name TEXT,
    away_team_id TEXT NOT NULL,
    away_team_name TEXT,
    home_score INTEGER,
    away_score INTEGER,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    player_name TEXT NOT NULL,
    position TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS player_match_stats (
    match_id TEXT NOT NULL
        REFERENCES matches(match_id),
    player_id TEXT NOT NULL
        REFERENCES players(player_id),
    team_id TEXT NOT NULL,
    minutes_played INTEGER,
    goals INTEGER,
    assists INTEGER,
    expected_goals NUMERIC(8,3),
    expected_assists NUMERIC(8,3),
    shots INTEGER,
    shots_on_target INTEGER,
    key_passes INTEGER,
    tackles INTEGER,
    interceptions INTEGER,
    rating NUMERIC(5,2),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (match_id, player_id)
);

CREATE INDEX IF NOT EXISTS idx_matches_season
    ON matches(season_id, match_date);

CREATE INDEX IF NOT EXISTS idx_player_stats_team
    ON player_match_stats(team_id);
