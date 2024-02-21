import database

database.to_csv(
    'Q_10',
    'SELECT Players.player_id, Names.player_name, Players.dribbled_passed '
    'FROM Players '
    'JOIN Names ON Players.player_id = Names.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'ORDER BY dribbled_passed DESC ',
    ('La Liga', '2020/2021')
)
