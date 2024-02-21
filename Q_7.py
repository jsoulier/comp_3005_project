import database

database.to_csv(
    'Q_7',
    'SELECT Players.player_id, Humans.human_name, COUNT(*) AS through_balls '
    'FROM Players '
    'JOIN Passes ON Players.player_id = Passes.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'JOIN Humans ON Players.human_id = Humans.human_id '
    'WHERE '
    '    Passes.through_ball = TRUE AND '
    '    Seasons.competition_name = %s AND Seasons.season_name = %s '
    'GROUP BY Players.player_id, Humans.human_name '
    'ORDER BY through_balls DESC; ',
    ('La Liga', '2020/2021')
)
