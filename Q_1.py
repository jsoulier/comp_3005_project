import database

database.to_csv(
    'Q_1',
    'SELECT Players.human_id, Humans.human_name, COALESCE(AVG(Shots.xg), 0) as xg '
    'FROM Players '
    'LEFT JOIN Shots ON Players.player_id = Shots.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'JOIN Humans ON Players.human_id = Humans.human_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'GROUP BY Players.player_id, Humans.human_name '
    'ORDER BY xg DESC; ',
    ('La Liga', '2020/2021')
)
