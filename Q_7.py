import database

database.to_csv(
    'Q_7',
    'SELECT Players.player_id, Humans.human_name, COALESCE(COUNT(Passes.player_id), 0) AS through_balls '
    'FROM Players '
    'LEFT JOIN Passes ON Players.player_id = Passes.player_id AND Passes.through_ball = TRUE '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'JOIN Humans ON Players.human_id = Humans.human_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'GROUP BY Players.player_id, Humans.human_name '
    'ORDER BY through_balls DESC; ',
    ('La Liga', '2020/2021')
)
