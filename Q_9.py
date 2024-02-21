import database

database.to_csv(
    'Q_9',
    'SELECT Players.player_id, Names.player_name, SUM(Players.successful_dribbles) as successful_dribbles '
    'FROM Players '
    'JOIN Names ON Players.player_id = Names.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name in (%s, %s, %s) '
    'GROUP BY Players.player_id, Names.player_name '
    'ORDER BY successful_dribbles DESC ',
    ('La Liga', '2018/2019', '2019/2020', '2020/2021')
)
