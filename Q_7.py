import database

database.to_csv(
    'Q_7',
    'SELECT Players.player_id, Names.player_name, Players.through_passes '
    'FROM Players '
    'JOIN Names ON Players.player_id = Names.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'ORDER BY through_passes DESC ',
    ('La Liga', '2020/2021')
)
