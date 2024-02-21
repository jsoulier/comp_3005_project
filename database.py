import psycopg

import contextlib
import csv
import functools
import glob
import json
import os
import subprocess

UPSTREAM = 'https://github.com/statsbomb/open-data' 
COMMIT = '0067cae166a56aa80b2ef18f61e16158d6a7359a'
DATABASE = 'football'
USERNAME = 'football'
PASSWORD = 'password'

SEASONS = [
    ('La Liga', '2020/2021'),
    ('La Liga', '2019/2020'),
    ('La Liga', '2018/2019'),
    ('Premier League', '2003/2004'),
]

connection = None
cursor = None

@contextlib.contextmanager
def cd(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)

def set_cwd(function):
    @functools.wraps(function)
    def _(*args, **kwargs):
        path = os.path.dirname(os.path.abspath(__file__))
        with cd(path):
            return function(*args, **kwargs)
    return _

def open_database():
    global connection
    global cursor
    connection = psycopg.connect(
        'dbname=' + DATABASE + ' '
        'user=' + USERNAME + ' '
        'password=' + PASSWORD + ' '
    )
    cursor = connection.cursor()

def quit_database():
    connection.commit()
    cursor.close()
    connection.close()

@set_cwd
def sparse_download():
    if os.path.exists('json'):
        return
    subprocess.run([
        'git',
        'clone',
        '-n',
        '--filter=tree:0',
        UPSTREAM,
        'json'
    ])

    with cd('json'):
        subprocess.run([
            'git',
            'sparse-checkout',
            'set',
            '--no-cone',
            '/data/competitions.json'
        ])
        subprocess.run([
            'git',
            'checkout',
            COMMIT
        ])

        matches1 = []
        matches2 = []
        path = os.path.join('data', 'competitions.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data:
            competition_name = item['competition_name']
            season_name = item['season_name']
            if (competition_name, season_name) not in SEASONS:
                continue
            competition_id = str(item['competition_id'])
            season_id = str(item['season_id'])
            path = 'data/matches/' + competition_id + '/' + season_id + '.json'
            matches1.append('/' + path)
            matches2.append(path)
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone',
        ] + matches1)

        events = []
        lineups = []
        for path in matches2:
            path = os.path.normpath(path)
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                match_id = str(item['match_id'])
                events.append('/data/events/' + match_id + '.json')
                lineups.append('/data/lineups/' + match_id + '.json')
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone',
        ] + events + lineups)

def create_tables():
    cursor.execute(
        'DROP TABLE IF EXISTS XG; '
        'DROP TABLE IF EXISTS Players; '
        'DROP TABLE IF EXISTS Names; '
        'DROP TABLE IF EXISTS Seasons; '
        'DROP TABLE IF EXISTS Teams; '
        'CREATE TABLE Teams ( '
        '    team_id INT PRIMARY KEY, '
        '    team_name VARCHAR(64) '
        '); '
        'CREATE TABLE Seasons ( '
        '    season_id SERIAL PRIMARY KEY, '
        '    competition_name VARCHAR(15), '
        '    season_name VARCHAR(10), '
        '    CONSTRAINT season_unique UNIQUE (competition_name, season_name) '
        '); '
        'CREATE TABLE Names ('
        '    player_id INT PRIMARY KEY, '
        '    player_name VARCHAR(128) '
        '); '
        'CREATE TABLE Players ( '
        '    player_id INT, '
        '    season_id INT, '
        '    team_id INT, '
        '    shots INT DEFAULT 0, '
        '    first_time_shots INT DEFAULT 0, '
        '    passes INT DEFAULT 0, '
        '    recipient_passes INT DEFAULT 0, '
        '    through_passes INT DEFAULT 0, '
        '    successful_dribbles INT DEFAULT 0, '
        '    dribbled_passed INT DEFAULT 0, '
        '    average_xg FLOAT DEFAULT 0, '
        '    FOREIGN KEY (player_id) REFERENCES Names (player_id), '
        '    FOREIGN KEY (season_id) REFERENCES Seasons (season_id), '
        '    FOREIGN KEY (team_id) REFERENCES Teams (team_id), '
        '    CONSTRAINT player_unique UNIQUE (player_id, season_id) '
        '); '
        'CREATE TABLE XG ( '
        '    player_id INT, '
        '    season_id INT, '
        '    xg FLOAT, '
        '    FOREIGN KEY (player_id, season_id) '
        '    REFERENCES Players (player_id, season_id) '
        '); '
    )

@set_cwd
def populate_tables():
    teams = []
    players = []
    names = []
    shots = []
    first_time_shots = []
    passes = []
    recipient_passes = []
    through_passes = []
    successful_dribbles = []
    dribbled_passed = []
    xgs = []

    with cd('json'):
        matches = glob.glob(os.path.join('data', 'matches', '**', '*.json'))
        for path in matches:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                match_id = str(item['match_id'])
                competition_name = item['competition']['competition_name']
                season_name = item['season']['season_name']
                cursor.execute(
                    'INSERT INTO Seasons (competition_name, season_name) '
                    'VALUES (%s, %s) '
                    'ON CONFLICT ON CONSTRAINT season_unique DO UPDATE '
                    'SET season_name = Seasons.season_name '
                    'RETURNING *; ',
                    (competition_name, season_name)
                )
                season_id = cursor.fetchone()[0]

                path = 'data/lineups/' + match_id + '.json'
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for item in data:
                    team_id = item['team_id']
                    team_name = item['team_name']
                    teams.append((team_id, team_name))
                    for player in item['lineup']:
                        player_name = player['player_name']
                        player_id = player['player_id']
                        players.append((player_id, season_id, team_id))
                        names.append((player_id, player_name))

                path = 'data/events/' + match_id + '.json'
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for item in data:
                    match item['type']['id']:
                        case 16:
                            player_id = item['player']['id']
                            statsbomb_xg = item['shot']['statsbomb_xg']
                            shots.append((player_id, season_id))
                            xgs.append((player_id, season_id, statsbomb_xg))
                            if 'first_time' in item['shot']:
                                first_time_shots.append((player_id, season_id))
                        case 30:
                            player_id = item['player']['id']
                            passes.append((player_id, season_id))
                            if 'recipient' in item['pass']:
                                recipient_id = item['pass']['recipient']['id']
                                recipient_passes.append((recipient_id, season_id))
                            if 'through_ball' in item['pass']:
                                through_passes.append((player_id, season_id))
                        case 14:
                            player_id = item['player']['id']
                            if item['dribble']['outcome']['id'] == 8:
                                successful_dribbles.append((player_id, season_id))
                        case 39:
                            player_id = item['player']['id']
                            dribbled_passed.append((player_id, season_id))

    cursor.executemany(
        'INSERT INTO Teams (team_id, team_name) '
        'VALUES (%s, %s) '
        'ON CONFLICT DO NOTHING; ',
        teams
    )
    cursor.executemany(
        'INSERT INTO Names (player_id, player_name) '
        'VALUES (%s, %s) '
        'ON CONFLICT DO NOTHING; ',
        names
    )
    cursor.executemany(
        'INSERT INTO Players (player_id, season_id, team_id) '
        'VALUES (%s, %s, %s) '
        'ON CONFLICT DO NOTHING; ',
        players
    )
    cursor.executemany(
        'UPDATE Players '
        'SET shots = shots + 1 '
        'WHERE player_id = %s AND season_id = %s; ',
        shots
    )
    cursor.executemany(
        'UPDATE Players '
        'SET first_time_shots = first_time_shots + 1 '
        'WHERE player_id = %s AND season_id = %s; ',
        first_time_shots
    )
    cursor.executemany(
        'UPDATE Players '
        'SET passes = passes + 1 '
        'WHERE player_id = %s AND season_id = %s; ',
        passes
    )
    cursor.executemany(
        'UPDATE Players '
        'SET recipient_passes = recipient_passes + 1 '
        'WHERE player_id = %s AND season_id = %s; ',
        recipient_passes
    )
    cursor.executemany(
        'UPDATE Players '
        'SET through_passes = through_passes + 1 '
        'WHERE player_id = %s AND season_id = %s; ',
        through_passes
    )
    cursor.executemany(
        'UPDATE Players '
        'SET successful_dribbles = successful_dribbles + 1 '
        'WHERE player_id = %s AND season_id = %s; ',
        successful_dribbles
    )
    cursor.executemany(
        'UPDATE Players '
        'SET dribbled_passed = dribbled_passed + 1 '
        'WHERE player_id = %s AND season_id = %s; ',
        dribbled_passed
    )
    cursor.executemany(
        'INSERT INTO XG (player_id, season_id, xg) '
        'VALUES (%s, %s, %s); ',
        xgs
    )
    cursor.execute(
        'UPDATE Players '
        'SET average_xg = AverageXG.average_xg '
        'FROM ( '
        '    SELECT player_id, season_id, AVG(xg) as average_xg '
        '    FROM XG '
        '    GROUP BY player_id, season_id '
        ') AS AverageXG '
        'WHERE '
        '    Players.player_id = AverageXG.player_id AND '
        '    Players.season_id = AverageXG.season_id; '
    )

@set_cwd
def to_csv(name, text, args):
    open_database()
    cursor.execute(text, args)
    cols = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    with open(name + '.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(cols)
        writer.writerows(rows)
    quit_database()
