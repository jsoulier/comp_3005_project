import database

database.to_csv(
    'Q_10',
    'SELECT Players.human_id, Humans.human_name, COALESCE(COUNT(DribbledPasts.player_id), 0) AS dribbled_pasts '
    'FROM Players '
    'LEFT JOIN DribbledPasts ON Players.player_id = DribbledPasts.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'JOIN Humans ON Players.human_id = Humans.human_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'GROUP BY Players.human_id, Humans.human_name '
    'ORDER BY dribbled_pasts; ',
    ('La Liga', '2020/2021')
)

