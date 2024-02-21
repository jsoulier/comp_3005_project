import database

database.open_database()
database.cursor.execute(
    'SELECT Players.player_name, Players.shots '
    'FROM Players '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'WHERE Seasons.season_name = %s '
    'ORDER BY shots DESC ',
    ('2020/2021',)
)
database.csvify('Q_2')
database.quit_database()
