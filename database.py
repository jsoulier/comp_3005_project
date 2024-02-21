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

connection = ''
cursor = ''

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

        m1 = []
        m2 = []
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
            m1.append('/' + path)
            m2.append(path)
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone',
        ] + m1)

        e = []
        l = []
        for path in m2:
            path = os.path.normpath(path)
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                match_id = str(item['match_id'])
                e.append('/data/events/' + match_id + '.json')
                l.append('/data/lineups/' + match_id + '.json')
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone',
        ] + e + l)

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

def create_tables():
    cursor.execute('DROP TABLE IF EXISTS Players')
    cursor.execute('DROP TABLE IF EXISTS Names')
    cursor.execute('DROP TABLE IF EXISTS Seasons')
    cursor.execute('DROP TABLE IF EXISTS Teams')
    cursor.execute(
        'CREATE TABLE Seasons ( '
        '    season_id SERIAL PRIMARY KEY, '
        '    competition_name VARCHAR(15), '
        '    season_name VARCHAR(10), '
        '    CONSTRAINT season_unique UNIQUE (competition_name, season_name) '
        '); '
    )
    cursor.execute(
        'CREATE TABLE Teams ( '
        '    team_id INT PRIMARY KEY, '
        '    team_name VARCHAR(64) '
        '); '
    )
    cursor.execute(
        'CREATE TABLE Names ('
        '    player_id INT PRIMARY KEY, '
        '    player_name VARCHAR(128) '
        '); '
    )
    cursor.execute(
        'CREATE TABLE Players ( '
        '    player_id INT, '
        '    season_id INT, '
        '    team_id INT, '
        '    shots INT DEFAULT 0, '
        '    first_time_shots INT DEFAULT 0, '
        '    passes INT DEFAULT 0, '
        '    FOREIGN KEY (player_id) REFERENCES Names (player_id), '
        '    FOREIGN KEY (season_id) REFERENCES Seasons (season_id), '
        '    FOREIGN KEY (team_id) REFERENCES Teams (team_id), '
        '    CONSTRAINT player_unique UNIQUE (player_id, season_id) '
        '); '
    )

def parse_l(path, season_id):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        team_id = item['team_id']
        team_name = item['team_name']
        cursor.execute(
            'INSERT INTO Teams (team_id, team_name) '
            'VALUES (%s, %s) '
            'ON CONFLICT DO NOTHING; ',
            (team_id, team_name)
        )
        for player in item['lineup']:
            player_name = player['player_name']
            player_id = player['player_id']
            cursor.execute(
                'INSERT INTO Names (player_id, player_name) '
                'VALUES (%s, %s) '
                'ON CONFLICT DO NOTHING; ',
                (player_id, player_name)
            )
            cursor.execute(
                'INSERT INTO Players (player_id, season_id, team_id) '
                'VALUES (%s, %s, %s) '
                'ON CONFLICT DO NOTHING; ',
                (player_id, season_id, team_id)
            )

def parse_e(path, season_id):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        match item['type']['id']:
            case 16: # shot
                player_id = item['player']['id']
                cursor.execute(
                    'UPDATE Players '
                    'SET shots = shots + 1 '
                    'WHERE player_id = %s AND season_id = %s; ',
                    (player_id, season_id)
                )
                if 'first_time' in item['shot']:
                    cursor.execute(
                        'UPDATE Players '
                        'SET first_time_shots = first_time_shots + 1 '
                        'WHERE player_id = %s AND season_id = %s; ',
                        (player_id, season_id)
                    )
            case 30: # pass
                player_id = item['player']['id']
                cursor.execute(
                    'UPDATE Players '
                    'SET passes = passes + 1 '
                    'WHERE player_id = %s AND season_id = %s; ',
                    (player_id, season_id)
                )

@set_cwd
def populate_tables():
    with cd('json'):
        m = glob.glob(os.path.join('data', 'matches', '**', '*.json'))
        for path in m:
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
                l = 'data/lineups/' + match_id + '.json'
                e = 'data/events/' + match_id + '.json'
                parse_l(l, season_id)
                parse_e(e, season_id)

def to_csv(name):
    cols = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    with open(name + '.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(cols)
        writer.writerows(rows)

if __name__ == '__main__':
    sparse_download()
    open_database()
    create_tables()
    populate_tables()
    quit_database()
