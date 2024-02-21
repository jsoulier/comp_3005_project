import database

database.to_csv(
    'Q_8',
    'SELECT Teams.team_id, Teams.team_name, COALESCE(COUNT(Passes.player_id), 0) AS through_balls '
    'FROM Players '
    'LEFT JOIN Passes ON Players.player_id = Passes.player_id AND Passes.through_ball = TRUE '
    'JOIN Teams ON Players.team_id = Teams.team_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'GROUP BY Teams.team_id, Teams.team_name '
    'ORDER BY through_balls DESC; ',
    ('La Liga', '2020/2021')
)
