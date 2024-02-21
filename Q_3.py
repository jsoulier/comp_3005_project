import database

database.to_csv(
    'Q_3',
    'SELECT Players.player_id, Humans.human_name, COUNT(*) AS first_time_shots '
    'FROM Players '
    'JOIN Shots ON Players.player_id = Shots.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'JOIN Humans ON Players.human_id = Humans.human_id '
    'WHERE '
    '    Shots.first_time = TRUE AND '
    '    Seasons.competition_name = %s AND Seasons.season_name IN (%s, %s, %s) '
    'GROUP BY Players.player_id, Humans.human_name '
    'ORDER BY first_time_shots DESC; ',
    ('La Liga', '2018/2019', '2019/2020', '2020/2021')
)
