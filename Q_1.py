import database

# database.to_csv(
#     'Q_1',
#     'SELECT Players.player_id, Names.player_name, Players.average_xg '
#     'FROM Players '
#     'JOIN Names ON Players.player_id = Names.player_id '
#     'JOIN Seasons ON Players.season_id = Seasons.season_id '
#     'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
#     'ORDER BY average_xg DESC ',
#     ('La Liga', '2020/2021')
# )
