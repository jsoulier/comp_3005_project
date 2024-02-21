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

# The seasons and competitions required by the queries
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

    # Clone the repository metadata
    subprocess.run([
        'git',
        'clone',
        '-n',
        '--filter=tree:0',
        UPSTREAM,
        'json'
    ])

    with cd('json'):
        # Clone the competitions
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

        # Clone the required matches
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

        # Clone the required lineups and events
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
        'DROP TABLE IF EXISTS BallReceipts; '
        'DROP TABLE IF EXISTS BallRecoveries; '
        'DROP TABLE IF EXISTS Dispossessions; '
        'DROP TABLE IF EXISTS Duels; '
        'DROP TABLE IF EXISTS CameraOns; '
        'DROP TABLE IF EXISTS Blocks; '
        'DROP TABLE IF EXISTS Offsides; '
        'DROP TABLE IF EXISTS Clearances; '
        'DROP TABLE IF EXISTS Interceptions; '
        'DROP TABLE IF EXISTS Dribbles; '
        'DROP TABLE IF EXISTS Shots; '
        'DROP TABLE IF EXISTS Pressures; '
        'DROP TABLE IF EXISTS HalfStarts; '
        'DROP TABLE IF EXISTS Substitutions; '
        'DROP TABLE IF EXISTS OwnGoalsAgainst; '
        'DROP TABLE IF EXISTS FoulsWon; '
        'DROP TABLE IF EXISTS FoulsCommitted; '
        'DROP TABLE IF EXISTS GoalKeepers; '
        'DROP TABLE IF EXISTS BadBehaviours; '
        'DROP TABLE IF EXISTS OwnGoalsFor; '
        'DROP TABLE IF EXISTS PlayerOns; '
        'DROP TABLE IF EXISTS PlayerOffs; '
        'DROP TABLE IF EXISTS Shields; '
        'DROP TABLE IF EXISTS Passes; '
        'DROP TABLE IF EXISTS FiftyFifties; '
        'DROP TABLE IF EXISTS HalfEnds; '
        'DROP TABLE IF EXISTS StartingXIs; '
        'DROP TABLE IF EXISTS TacticalShifts; '
        'DROP TABLE IF EXISTS Errors; '
        'DROP TABLE IF EXISTS Miscontrols; '
        'DROP TABLE IF EXISTS DribbledPasts; '
        'DROP TABLE IF EXISTS InjuryStoppages; '
        'DROP TABLE IF EXISTS RefereeBallDrops; '
        'DROP TABLE IF EXISTS Carries; '
        'DROP TABLE IF EXISTS Players; '
        'DROP TABLE IF EXISTS Humans; '
        'DROP TABLE IF EXISTS Teams; '
        'DROP TABLE IF EXISTS Seasons; '
        'CREATE TABLE Seasons ( '
        '    season_id SERIAL PRIMARY KEY, '
        '    competition_name VARCHAR(15), '
        '    season_name VARCHAR(10), '
        '    CONSTRAINT season_unique UNIQUE (competition_name, season_name) '
        '); '
        'CREATE TABLE Humans ( '
        '    human_id INT PRIMARY KEY, '
        '    human_name VARCHAR(128) '
        '); '
        'CREATE TABLE Teams ( '
        '    team_id INT PRIMARY KEY, '
        '    team_name VARCHAR(128) '
        '); '
        'CREATE TABLE Players ('
        '    player_id SERIAL PRIMARY KEY, '
        '    human_id INT, '
        '    team_id INT, '
        '    season_id INT, '
        '    FOREIGN KEY (human_id) REFERENCES Humans (human_id), '
        '    FOREIGN KEY (season_id) REFERENCES Seasons (season_id), '
        '    FOREIGN KEY (team_id) REFERENCES Teams (team_id), '
        '    CONSTRAINT player_unique UNIQUE (human_id, season_id, team_id) '
        '); '
        'CREATE TABLE BallReceipts ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE BallRecoveries ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Dispossessions ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Duels ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE CameraOns ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Blocks ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Offsides ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Clearances ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Interceptions ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Dribbles ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Shots ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Pressures ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE HalfStarts ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Substitutions ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE OwnGoalsAgainst ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE FoulsWon ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE FoulsCommitted ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE GoalKeepers ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE BadBehaviours ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE OwnGoalsFor ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE PlayerOns ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE PlayerOffs ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Shields ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Passes ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE FiftyFifties ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE HalfEnds ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE StartingXIs ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE TacticalShifts ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Errors ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Miscontrols ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE DribbledPasts ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE InjuryStoppages ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE RefereeBallDrops ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
        'CREATE TABLE Carries ( '
        '    player_id INT, '
        '    FOREIGN KEY (player_id) REFERENCES Players (player_id) '
        '); '
    )

@set_cwd
def populate_tables():
    humans = []
    players = []
    teams = []
    ball_receipts = []
    ball_recoveries = []
    dispossessions = []
    duels = []
    camera_ons = []
    blocks = []
    offsides = []
    clearances = []
    interceptions = []
    dribbles = []
    shots = []
    pressures = []
    half_starts = []
    substitutions = []
    own_goal_sagainst = []
    fouls_won = []
    fouls_committed = []
    goalkeepers = []
    bad_behaviours = []
    own_goals_for = []
    player_ons = []
    player_offs = []
    shields = []
    passes = []
    fifty_fifties = []
    half_ends = []
    starting_xis = []
    tactical_shifts = []
    errors = []
    miscontrols = []
    dribbled_pasts = []
    injury_stoppages = []
    referee_ball_drops = []
    carries = []

    # Parse the matches
    with cd('json'):
        matches = glob.glob(os.path.join('data', 'matches', '**', '*.json'))
        for path in matches:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                match_id = str(item['match_id'])
                competition_name = item['competition']['competition_name']
                season_name = item['season']['season_name']

                # Get unique id for the season and competition pair
                cursor.execute(
                    'INSERT INTO Seasons (competition_name, season_name) '
                    'VALUES (%s, %s) '
                    'ON CONFLICT ON CONSTRAINT season_unique DO UPDATE '
                    'SET season_name = Seasons.season_name '
                    'RETURNING *; ',
                    (competition_name, season_name)
                )
                season_id = cursor.fetchone()[0]

                # Parse the lineups
                path = 'data/lineups/' + match_id + '.json'
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for item in data:
                    team_id = item['team_id']
                    team_name = item['team_name']
                    teams.append((team_id, team_name))
                    for player in item['lineup']:
                        human_name = player['player_name']
                        human_id = player['player_id']
                        players.append((human_id, team_id, season_id))
                        humans.append((human_id, human_name))

                # Parse the events
                path = 'data/events/' + match_id + '.json'
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for item in data:
                    type_id = item['type']['id']
                    if type_id == 16:
                        human_id = item['player']['id']
                        team_id = item['team']['id']
                        shots.append((human_id, team_id, season_id))
                        continue
                    if type_id == 30:
                        human_id = item['player']['id']
                        team_id = item['team']['id']
                        passes.append((human_id, team_id, season_id))
                        continue
                    if type_id == 14:
                        human_id = item['player']['id']
                        team_id = item['team']['id']
                        dribbles.append((human_id, team_id, season_id))
                        continue

    cursor.executemany(
        'INSERT INTO Teams (team_id, team_name) '
        'VALUES (%s, %s) '
        'ON CONFLICT DO NOTHING; ',
        teams
    )
    cursor.executemany(
        'INSERT INTO Humans (human_id, human_name) '
        'VALUES (%s, %s) '
        'ON CONFLICT DO NOTHING; ',
        humans
    )
    cursor.executemany(
        'INSERT INTO Players (human_id, team_id, season_id) '
        'VALUES (%s, %s, %s) '
        'ON CONFLICT ON CONSTRAINT player_unique DO NOTHING; ',
        players
    )
    cursor.executemany(
        'INSERT INTO Shots (player_id) '
        'VALUES (('
        '    SELECT player_id '
        '    FROM Players '
        '    WHERE human_id = %s AND team_id = %s AND season_id = %s '
        '))',
        shots
    )

@set_cwd
def to_csv(name, text, args):
    open_database()
    cursor.execute(text, args)
    cols = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    if not os.path.exists('csv'):
        os.mkdir('csv')
    path = os.path.join('csv', name + '.csv')
    with open(path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(cols)
        writer.writerows(rows)
    quit_database()
