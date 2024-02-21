import database

# database.to_csv(
#     'Q_8',
#     'SELECT Teams.team_id, Teams.team_name, SUM(Players.through_passes) AS through_passes '
#     'FROM Players '
#     'JOIN Teams ON Players.team_id = Teams.team_id '
#     'JOIN Seasons ON Players.season_id = Seasons.season_id '
#     'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
#     'GROUP BY Teams.team_id, Teams.team_name '
#     'ORDER BY through_passes DESC ',
#     ('La Liga', '2020/2021')
# )
