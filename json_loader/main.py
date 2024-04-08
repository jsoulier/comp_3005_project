import contextlib
import glob
import json
import os
import psycopg
import sql 
import subprocess

repository = 'https://github.com/statsbomb/open-data'
commit = '0067cae166a56aa80b2ef18f61e16158d6a7359a'
name = 'dump_database'
username = 'postgres'
password = '1234'
host = 'localhost'
port = '5432'
seasons = [('La Liga', '2020/2021'), ('La Liga', '2019/2020'),
    ('La Liga','2018/2019'), ('Premier League', '2003/2004')]

@contextlib.contextmanager
def cd(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)

def download():
    if os.path.exists('json'):
        return
    subprocess.run(['git', 'clone', '-n', '--filter=tree:0', repository, 'json'])
    with cd('json'):
        subprocess.run(['git', 'sparse-checkout', 'set', '--no-cone', '/data/competitions.json'])
        subprocess.run(['git', 'checkout', commit])
        matches = []
        events = []
        lineups = []
        path = os.path.join('data', 'competitions.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data:
            competition_name = item['competition_name']
            season_name = item['season_name']
            season = (competition_name, season_name)
            if season not in seasons:
                continue
            competition_id = str(item['competition_id'])
            season_id = str(item['season_id'])
            matches.append('data/matches/' + competition_id + '/' + season_id + '.json')
        subprocess.run(['git', 'sparse-checkout', 'add', '--no-cone'] + ['/' + path for path in matches])
        for path in matches:
            path = os.path.normpath(path)
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                match_id = str(item['match_id'])
                events.append('/data/events/' + match_id + '.json')
                lineups.append('/data/lineups/' + match_id + '.json')
        subprocess.run(['git', 'sparse-checkout', 'add', '--no-cone'] + events + lineups)

def populate(cursor):
    person = []
    team = []
    player = []
    ball_recovery = []
    dispossessed = []
    duel = []
    camera_on = []
    block = []
    offside = []
    clearance = []
    interception = []
    dribble = []
    shot = []
    pressure = []
    half_start = []
    substitution = []
    own_goal_against = []
    foul_won = []
    foul_committed = []
    goal_keeper = []
    bad_behaviour = []
    own_goal_for = []
    player_on = []
    player_off = []
    shield = []
    pass_ = []
    fifty_fifty = []
    half_end = []
    starting_xi = []
    tactical_shift = []
    error = []
    miscontrol = []
    dribbled_past = []
    injury_stoppage = []
    referee_ball_drop = []
    ball_receipt = []
    carry = []
    with cd('json'):
        matches = glob.glob(os.path.join('data', 'matches', '**', '*.json'))
        for path in matches:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                match_id = str(item['match_id'])
                competition_name = item['competition']['competition_name']
                season_name = item['season']['season_name']
                cursor.execute(sql.season, (competition_name, season_name))
                season_id = cursor.fetchone()[0]
                path = 'data/lineups/' + match_id + '.json'
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for item in data:
                    team_id = item['team_id']
                    team_name = item['team_name']
                    team.append((team_id, team_name))
                    for player_ in item['lineup']:
                        person_name = player_['player_name']
                        person_id = player_['player_id']
                        player.append((person_id, team_id, season_id))
                        person.append((person_id, person_name))
                path = 'data/events/' + match_id + '.json'
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for item in data:
                    type_id = item['type']['id']
                    person_id = item.get('player', {}).get('id')
                    team_id = item.get('team', {}).get('id')
                    play_id = item.get('play_pattern', {}).get('id')
                    position_id = item.get('position', {}).get('id')
                    period = item.get('period', 0)
                    minute = item.get('minute', 0)
                    second = item.get('second', 0)
                    possession = item.get('possession', 0)
                    possession_id = item.get('possession_team', {}).get('id')
                    x, y = item.get('location', [0, 0])
                    duration = item.get('duration', 0)
                    under_pressure = 'under_pressure' in item
                    counter_pressure = 'counterpress' in item
                    common = (person_id, team_id, season_id, play_id, position_id,
                        period, minute, second, possession, possession_id, x, y,
                        duration, under_pressure)
                    match type_id:
                        case 2:
                            ball_recovery_ = item.get('ball_recovery', {})
                            offensive = 'offensive' in ball_recovery_
                            recovery_failure = 'recovery_failure' in ball_recovery_
                            ball_recovery.append(common + (offensive, recovery_failure))
                        case 3:
                            dispossessed.append(common)
                        case 4:
                            duel_ = item['duel']
                            duel_type_id = duel_['type']['id']
                            duel_outcome_id = duel_.get('outcome', {}).get('id')
                            duel.append(common + (counter_pressure, duel_type_id, duel_outcome_id))
                        case 5:
                            camera_on.append(common)
                        case 6:
                            block_ = item.get('block', {})
                            deflection = 'deflection' in block_
                            offensive = 'offensive' in block_
                            save_block = 'save_block' in block_
                            block.append(common + (counter_pressure, deflection, offensive, save_block))
                        case 8:
                            offside.append(common)
                        case 9:
                            clearance_ = item.get('clearance')
                            aerial_won = 'aerial_won' in clearance_
                            body_part_id = clearance_['body_part']['id']
                            clearance.append(common + (aerial_won, body_part_id))
                        case 10:
                            interception.append(common)
                        case 14:
                            dribble_ = item['dribble']
                            overrun = 'overrun' in dribble_
                            nutmeg = 'nutmeg' in dribble_
                            no_touch = 'no_touch' in dribble_
                            outcome_id = dribble_['outcome']['id']
                            dribble.append(common + (overrun, nutmeg, no_touch, outcome_id))
                        case 16:
                            shot_ = item['shot']
                            xg = shot_['statsbomb_xg']
                            first_time = 'first_time' in shot_
                            shot.append(common + (xg, first_time))
                        case 17:
                            pressure.append(common)
                        case 18:
                            half_start.append(common)
                        case 19:
                            substitution.append(common)
                        case 20:
                            own_goal_against.append(common)
                        case 21:
                            foul_won.append(common)
                        case 22:
                            foul_committed.append(common)
                        case 23:
                            goal_keeper.append(common)
                        case 24:
                            bad_behaviour.append(common)
                        case 25:
                            own_goal_for.append(common + (team_id, ))
                        case 26:
                            player_on.append(common)
                        case 27:
                            player_off.append(common)
                        case 28:
                            shield.append(common)
                        case 30:
                            pass__ = item['pass']
                            through_ball = 'through_ball' in pass__
                            pass_.append(common + (through_ball, ))
                        case 33:
                            fifty_fifty.append(common)
                        case 34:
                            half_end.append(common)
                        case 35:
                            starting_xi.append(common)
                        case 36:
                            tactical_shift.append(common)
                        case 37:
                            error.append(common)
                        case 38:
                            miscontrol.append(common)
                        case 39:
                            dribbled_past.append(common)
                        case 40:
                            injury_stoppage.append(common)
                        case 41:
                            referee_ball_drop.append(common)
                        case 42:
                            ball_receipt.append(common)
                        case 43:
                            carry.append(common)
    cursor.executemany(sql.person, person)
    cursor.executemany(sql.team, team)
    cursor.executemany(sql.player, player)
    cursor.executemany(sql.ball_recovery, ball_recovery)
    cursor.executemany(sql.dispossessed, dispossessed)
    cursor.executemany(sql.duel, duel)
    cursor.executemany(sql.camera_on, camera_on)
    cursor.executemany(sql.block, block)
    cursor.executemany(sql.offside, offside)
    cursor.executemany(sql.clearance, clearance)
    cursor.executemany(sql.interception, interception)
    cursor.executemany(sql.dribble, dribble)
    cursor.executemany(sql.shot, shot)
    cursor.executemany(sql.pressure, pressure)
    cursor.executemany(sql.half_start, half_start)
    cursor.executemany(sql.substitution, substitution)
    cursor.executemany(sql.own_goal_against, own_goal_against)
    cursor.executemany(sql.foul_won, foul_won)
    cursor.executemany(sql.foul_committed, foul_committed)
    cursor.executemany(sql.goal_keeper, goal_keeper)
    cursor.executemany(sql.bad_behaviour, bad_behaviour)
    cursor.executemany(sql.own_goal_for, own_goal_for)
    cursor.executemany(sql.player_on, player_on)
    cursor.executemany(sql.player_off, player_off)
    cursor.executemany(sql.shield, shield)
    cursor.executemany(sql.pass_, pass_)
    cursor.executemany(sql.fifty_fifty, fifty_fifty)
    cursor.executemany(sql.half_end, half_end)
    cursor.executemany(sql.starting_xi, starting_xi)
    cursor.executemany(sql.tactical_shift, tactical_shift)
    cursor.executemany(sql.error, error)
    cursor.executemany(sql.miscontrol, miscontrol)
    cursor.executemany(sql.dribbled_past, dribbled_past)
    cursor.executemany(sql.injury_stoppage, injury_stoppage)
    cursor.executemany(sql.referee_ball_drop, referee_ball_drop)
    cursor.executemany(sql.ball_receipt, ball_receipt)
    cursor.executemany(sql.carry, carry)

def export():
    os.environ['PGPASSWORD'] = password
    subprocess.run([
        'pg_dump.exe',
        '--file', '..\\dbexport.sql',
        '--host', host,
        '--port', port,
        '--username', username,
        '--encoding', 'utf-8',
        '--verbose',
        '--format=p',
        name
    ]);

def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    connection = psycopg.connect(dbname=name, user=username, password=password, host=host, port=port)
    cursor = connection.cursor()
    download()
    cursor.execute(sql.drop)
    cursor.execute(sql.create)
    populate(cursor)
    connection.commit()
    cursor.close()
    connection.close()
    export()

if __name__ == '__main__':
    main()
