import database

# database.to_csv(
#     'Q_5',
#     'SELECT Players.player_id, Names.player_name, Players.recipient_passes '
#     'FROM Players '
#     'JOIN Names ON Players.player_id = Names.player_id '
#     'JOIN Seasons ON Players.season_id = Seasons.season_id '
#     'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
#     'ORDER BY recipient_passes DESC ',
#     ('Premier League', '2003/2004')
# )
