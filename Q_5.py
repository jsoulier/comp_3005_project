import database

database.to_csv(
    'Q_5',
    'SELECT Players.player_id, Humans.human_name, COALESCE(COUNT(BallReceipts.player_id), 0) AS ball_receipts '
    'FROM Players '
    'LEFT JOIN BallReceipts ON Players.player_id = BallReceipts.player_id '
    'JOIN Seasons ON Players.season_id = Seasons.season_id '
    'JOIN Humans ON Players.human_id = Humans.human_id '
    'WHERE Seasons.competition_name = %s AND Seasons.season_name = %s '
    'GROUP BY Players.player_id, Humans.human_name '
    'ORDER BY ball_receipts DESC; ',
    ('Premier League', '2003/2004')
)
