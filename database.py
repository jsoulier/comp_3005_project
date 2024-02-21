import psycopg

import contextlib
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
    '2003/2004',
    '2018/2019',
    '2019/2020',
    '2020/2021',
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
            'data/competitions.json'
        ])
        subprocess.run([
            'git',
            'checkout',
            COMMIT
        ])

        events = []
        lineups = []
        matches = []

        path = os.path.join('data', 'competitions.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data:
            if item['season_name'] not in SEASONS:
                continue
            competition = str(item['competition_id'])
            season = str(item['season_id'])
            matches.append('data/matches/' + competition + '/' + season + '.json')
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone',
        ] + matches)

        for path in matches:
            path = os.path.normpath(path)
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                events.append('data/events/' + str(item['match_id']) + '.json')
                lineups.append('data/lineups/' + str(item['match_id']) + '.json')
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone',
        ] + events + lineups)

def open_database():
    global connection
    global cursor
    connection = psycopg.connect(
        'dbname=' + DATABASE + ' '
        'user=' + USERNAME + ' '
        'password=' + PASSWORD + ' '
    )
    cursor = connection.cursor()

def create_database_tables():
    cursor.execute('DROP TABLE IF EXISTS Players')
    cursor.execute('DROP TABLE IF EXISTS Seasons')
    cursor.execute('DROP TABLE IF EXISTS Teams')
    cursor.execute(
        'CREATE TABLE Seasons ( '
        '    id SERIAL PRIMARY KEY, '
        '    name VARCHAR(10) UNIQUE '
        '); '
    )
    cursor.execute(
        'CREATE TABLE Teams ( '
        '    id INT PRIMARY KEY, '
        '    name VARCHAR(64) '
        '); '
    )
    cursor.execute(
        'CREATE TABLE Players ( '
        '    name VARCHAR(128), '
        '    id INT, '
        '    season INT, '
        '    team INT, '
        '    games_played INT DEFAULT 1, '
        '    goals_scored INT DEFAULT 0, '
        '    FOREIGN KEY (season) REFERENCES Seasons (id), '
        '    FOREIGN KEY (team) REFERENCES Teams (id), '
        '    CONSTRAINT uniqueness UNIQUE (id, season, team) '
        '); '
    )

def parse_lineups(path, season):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        team = item['team_id']
        cursor.execute(
            'INSERT INTO Teams (id, name) '
            'VALUES (%s, %s) '
            'ON CONFLICT DO NOTHING; ',
            (team, item['team_name'])
        )
        for player in item['lineup']:
            cursor.execute(
                'INSERT INTO Players (name, id, season, team) '
                'VALUES (%s, %s, %s, %s) '
                'ON CONFLICT ON CONSTRAINT uniqueness DO UPDATE '
                'SET games_played = Players.games_played + 1; ',
                (player['player_name'], player['player_id'], season, team)
            )

def parse_events(path, season):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        if 'shot' not in item:
            continue
        if item['shot']['outcome']['name'] == 'Goal':
            cursor.execute(
                'UPDATE Players '
                'SET goals_scored = goals_scored + 1 '
                'WHERE id = %s AND season = %s AND team = %s; ',
                (item['player']['id'], season, item['team']['id'])
            )

@set_cwd
def populate_tables():
    with cd('json'):
        matches = glob.glob(os.path.join('data', 'matches', '**', '*.json'))
        for path in matches:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                cursor.execute(
                    'INSERT INTO Seasons (name) '
                    'VALUES (%s) '
                    'ON CONFLICT (name) DO UPDATE '
                    'SET name = Seasons.name '
                    'RETURNING *; ',
                    (item['season']['season_name'],)
                )
                season = cursor.fetchone()[0]
                lineups = 'data/lineups/' + str(item['match_id']) + '.json'
                events = 'data/events/' + str(item['match_id']) + '.json'
                parse_lineups(lineups, season)
                parse_events(events, season)

if __name__ == '__main__':
    # sparse_download()
    open_database()
    create_database_tables()
    populate_tables()

    cursor.execute('SELECT * FROM Players')
    rows = cursor.fetchall()
    for col_desc in cursor.description:
        print(col_desc[0])
    for row in rows:
        for value in row:
            try:
                print(value, end=' ')
            except:
                pass
        print()
