from .database import get_connection


def ingest_match(match, players):
    """
    Insert or update one match and its player statistics.

    Both inputs come from the Soccer Data API.
    """

    match_id = match["id"]

    team_ids = {
        match["home_team"]["id"],
        match["away_team"]["id"]
    }

    if not isinstance(players, list) or not players:
        raise ValueError(
            f"Missing player statistics for {match_id}"
        )

    if any(p.get("team_id") not in team_ids for p in players):
        raise ValueError(
            f"Invalid player team assignment in {match_id}"
        )

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Insert or update the match
            cur.execute("""
                INSERT INTO live.matches (
                    match_id, competition_id, season_id,
                    matchday, match_date, status,
                    home_team_id, home_team_name,
                    away_team_id, away_team_name,
                    home_score, away_score
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (match_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    home_score = EXCLUDED.home_score,
                    away_score = EXCLUDED.away_score,
                    updated_at = NOW()
            """, (
                match_id,
                match["competition_id"],
                match["season_id"],
                match.get("matchday"),
                match.get("utc_date"),
                match["status"],
                match["home_team"]["id"],
                match["home_team"]["name"],
                match["away_team"]["id"],
                match["away_team"]["name"],
                match["score"].get("home"),
                match["score"].get("away")
            ))

            for player in players:

                # Insert or update player details
                cur.execute("""
                    INSERT INTO live.players (
                        player_id, player_name, position
                    )
                    VALUES (%s, %s, %s)
                    ON CONFLICT (player_id) DO UPDATE SET
                        player_name = EXCLUDED.player_name,
                        position = EXCLUDED.position,
                        updated_at = NOW()
                """, (
                    player["player_id"],
                    player["player_name"],
                    player.get("position")
                ))

                shooting = player.get("shooting") or {}
                passing = player.get("passing") or {}
                defending = player.get("defending") or {}

                # Insert or update player match statistics
                cur.execute("""
                    INSERT INTO live.player_match_stats (
                        match_id, player_id, team_id,
                        minutes_played, goals, assists,
                        expected_goals, expected_assists,
                        shots, shots_on_target,
                        key_passes, tackles,
                        interceptions, rating
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (match_id, player_id)
                    DO UPDATE SET
                        team_id = EXCLUDED.team_id,
                        minutes_played = EXCLUDED.minutes_played,
                        goals = EXCLUDED.goals,
                        assists = EXCLUDED.assists,
                        expected_goals = EXCLUDED.expected_goals,
                        expected_assists = EXCLUDED.expected_assists,
                        shots = EXCLUDED.shots,
                        shots_on_target = EXCLUDED.shots_on_target,
                        key_passes = EXCLUDED.key_passes,
                        tackles = EXCLUDED.tackles,
                        interceptions = EXCLUDED.interceptions,
                        rating = EXCLUDED.rating,
                        updated_at = NOW()
                """, (
                    match_id,
                    player["player_id"],
                    player["team_id"],
                    player.get("minutes_played"),
                    shooting.get("goals"),
                    passing.get("assists"),
                    shooting.get("expected_goals"),
                    shooting.get("expected_assists"),
                    shooting.get("total_shots"),
                    shooting.get("shots_on_target"),
                    passing.get("key_passes"),
                    defending.get("tackles"),
                    defending.get("interceptions"),
                    player.get("rating")
                ))

    return len(players)
