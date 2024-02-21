import database

database.to_csv(
    'Q_3',
    'SELECT Players.human_id, Humans.human_name, COALESCE(COUNT(Shots.player_id), 0) AS first_time_shots '
    'FROM Players '
    'LEFT JOIN Shots ON Players.player_id = Shots.player_id AND Shots.first_time = TRUE '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'JOIN Humans ON Players.human_id = Humans.human_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name IN (%s, %s, %s) '
    'GROUP BY Players.human_id, Humans.human_name '
    'ORDER BY first_time_shots DESC; ',
    ('La Liga', '2018/2019', '2019/2020', '2020/2021')
)
