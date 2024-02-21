import database

database.to_csv(
    'Q_9',
    'SELECT Players.human_id, Humans.human_name, COALESCE(COUNT(Dribbles.player_id), 0) AS completed_dribbles '
    'FROM Players '
    'LEFT JOIN Dribbles ON Players.player_id = Dribbles.player_id AND Dribbles.completed = TRUE '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'JOIN Humans ON Players.human_id = Humans.human_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name IN (%s, %s, %s) '
    'GROUP BY Players.human_id, Humans.human_name '
    'ORDER BY completed_dribbles DESC; ',
    ('La Liga', '2018/2019', '2019/2020', '2020/2021')
)
