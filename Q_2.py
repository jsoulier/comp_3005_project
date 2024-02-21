import database

database.open_database()
database.cursor.execute(
    'SELECT * '
    'FROM Players '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'WHERE Seasons.season_name = %s '
    'ORDER BY goals_scored DESC ',
    ('2020/2021',)
)

rows = database.cursor.fetchall()
for row in rows:
    print(row)

database.quit_database()
