import database

database.open_database()
database.cursor.execute(
    'SELECT Names.player_name, Players.first_time_shots '
    'FROM Players '
    'JOIN Names ON Players.player_id = Names.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'ORDER BY first_time_shots DESC ',
    ('La Liga', '2020/2021',)
)
database.to_csv('Q_3')
database.quit_database()
