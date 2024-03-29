import database

database.to_csv(
    'Q_6',
    'SELECT Teams.team_id, Teams.team_name, COALESCE(COUNT(Shots.player_id), 0) AS shots '
    'FROM Players '
    'LEFT JOIN Shots ON Players.player_id = Shots.player_id '
    'JOIN Teams ON Players.team_id = Teams.team_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'GROUP BY Teams.team_id, Teams.team_name '
    'ORDER BY shots DESC; ',
    ('Premier League', '2003/2004')
)
