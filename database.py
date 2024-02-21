import psycopg

import contextlib
import functools
import json
import os
import subprocess

UPSTREAM = 'https://github.com/statsbomb/open-data' 
COMMIT = '0067cae166a56aa80b2ef18f61e16158d6a7359a'
DATABASE = 'football'
USERNAME = 'football'
PASSWORD = 'password'

# All of the seasons required to complete the queries
SEASONS = [
    '2003/2004',
    '2018/2019',
    '2019/2020',
    '2020/2021',
]

connection = ''

@contextlib.contextmanager
def cd(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)

def force_cwd(function):
    @functools.wraps(function)
    def _(*args, **kwargs):
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)
        return function(*args, **kwargs)
    return _

def open_database():
    global connection
    connection = psycopg.connect(
        'dbname=' + DATABASE + ' '
        'user=' + USERNAME + ' '
        'password=' + PASSWORD + ' '
    )

def create_database_tables():
    with connection.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS Seasons')
        cursor.execute('DROP TABLE IF EXISTS Teams')
        cursor.execute('DROP TABLE IF EXISTS Players')
        cursor.execute(
            'CREATE TABLE Seasons ('
            '    id INT PRIMARY KEY,'
            '    name VARCHAR(10)'
            ');'
        )
        cursor.execute(
            'CREATE TABLE Teams ('
            '    id INT PRIMARY KEY'
            ');'
        )
        cursor.execute(
            'CREATE TABLE Players ('
            '    season INT,'
            '    team INT,'
            '    FOREIGN KEY (season) REFERENCES Seasons(id),'
            '    FOREIGN KEY (team) REFERENCES Teams(id)'
            ');'
        )

@force_cwd
def populate_database():
    # if os.path.exists('json'):
    #     return

    # Start with basic metadata
    subprocess.run([
        'git',
        'clone',
        '-n',
        '--filter=tree:0',
        UPSTREAM,
        'json'
    ])

    with cd('json'):

        # Clone the root to determine what matches are required
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

        # Clone the required matches
        path = os.path.join('data', 'competitions.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data:
            if item['season_name'] not in SEASONS:
                continue
            matches.append('data/matches/' + str(item['competition_id']) + '/' +
                str(item['season_id']) + '.json')
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone',
        ] + matches)

        # Clone the required events and lineups
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

        # TODO: populate events and lineups

if __name__ == '__main__':
    open_database()
    create_database_tables()
    populate_database()
