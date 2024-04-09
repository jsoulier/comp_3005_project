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
seasons = [
    ('La Liga', '2020/2021'),
    ('La Liga', '2019/2020'),
    ('La Liga', '2018/2019'),
    ('Premier League', '2003/2004')
]

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
    
    # clone competitions
    subprocess.run([
        'git',
        'clone',
        '-n',
        '--filter=tree:0',
        repository,
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
            commit
        ])
        matches = []
        events = []
        lineups = []

        # clone matches
        path = os.path.join('data', 'competitions.json')
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data:
            competition_name = item['competition_name']
            season_name = item['season_name']
            season = (competition_name, season_name)
            if season not in seasons:
                continue
            competition_id = item['competition_id']
            season_id = item['season_id']
            matches.append(
                'data/matches/' +
                str(competition_id) +
                '/' +
                str(season_id) +
                '.json'
            )
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone'
        ] + ['/' + path for path in matches])

        # clone events and matches
        for path in matches:
            path = os.path.normpath(path)
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for item in data:
                match_id = item['match_id']
                events.append(
                    '/data/events/' +
                    str(match_id) +
                    '.json'
                )
                lineups.append(
                    '/data/lineups/' +
                    str(match_id) +
                    '.json'
                )
        subprocess.run([
            'git',
            'sparse-checkout',
            'add',
            '--no-cone'
        ] + events + lineups)

def populate(cursor):
    person = []
    country = []
    team = []
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
    freeze_frame = []
    stadium = []
    match_ = []
    lineup_ = []
    card_ = []
    manager_ = []
    referee = []
    shot_id = 0
    with cd('json'):
        matches = glob.glob(os.path.join('data', 'matches', '**', '*.json'))
        for path in matches:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # add matches
            for item in data:
                match_id = item['match_id']
                match_date = item['match_date']
                kick_off = item['kick_off']
                home_team_id = item['home_team']['home_team_id']
                away_team_id = item['away_team']['away_team_id']
                home_team_gender = item['home_team']['home_team_gender']
                away_team_gender = item['away_team']['away_team_gender']
                home_score = item['home_score']
                away_score = item['away_score']
                match_week = item['match_week']
                competition_id = item['competition_stage']['id']
                country_name  = item['competition']['country_name']
                competition_name = item['competition']['competition_name']
                season_name = item['season']['season_name']
                cursor.execute(sql.season, (competition_name, season_name))
                season_id = cursor.fetchone()[0]
                stadium_id = item.get('stadium', {}).get('id')
                if stadium_id != None:
                    stadium_name = item['stadium']['name']
                    country_id = item['stadium']['country']['id']
                    stadium.append((stadium_id, stadium_name, country_id))
                match_.append((
                    match_id,
                    match_date,
                    kick_off,
                    country_name,
                    season_id,
                    home_team_id,
                    away_team_id,
                    home_team_gender,
                    away_team_gender,
                    home_score,
                    away_score,
                    match_week,
                    competition_id,
                    stadium_id
                ))

                # add managers
                for manager in item['home_team'].get('managers', []):
                    manager_id = manager['id']
                    manager_name = manager['name']
                    manager_nickname = manager['nickname']
                    country_id = manager['country']['id']
                    manager_.append((
                        manager_id,
                        manager_name,
                        match_id,
                        home_team_id,
                        manager_nickname,
                        country_id
                    ))
                for manager in item['away_team'].get('managers', []):
                    manager_id = manager['id']
                    manager_name = manager['name']
                    manager_nickname = manager['nickname']
                    country_id = manager['country']['id']
                    manager_.append((
                        manager_id,
                        manager_name,
                        match_id,
                        away_team_id,
                        manager_nickname,
                        country_id
                    ))

                # add referees
                if item.get('referee', {}):
                    referee_id = item['referee']['id']
                    referee_name = item['referee']['name']
                    country_id = item['referee']['country']['id']
                    referee.append((
                        referee_id,
                        referee_name,
                        match_id,
                        country_id
                    ))

                path = 'data/lineups/' + str(match_id) + '.json'
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for item in data:
                    team_id = item['team_id']
                    team_name = item['team_name']
                    team.append((team_id, team_name))

                    # add people
                    for lineup in item['lineup']:
                        person_name = lineup['player_name']
                        person_id = lineup['player_id']
                        person_nickname = lineup['player_nickname']
                        jersey_number = lineup['jersey_number']
                        country_id = lineup['country']['id']
                        country_name = lineup['country']['name']
                        country.append((country_id, country_name))
                        person.append((
                            person_id,
                            person_name,
                            person_nickname,
                            country_id
                        ))

                        # add positions
                        for position in lineup['positions']:
                            position_id = position['position_id']
                            from_ = position['from']
                            to_ = position['to']
                            from_period = position['from_period']
                            to_period = position['to_period']
                            start_reason = position['start_reason']
                            end_reason = position['end_reason']
                            lineup_.append((
                                match_id,
                                person_id,
                                position_id,
                                jersey_number,
                                from_,
                                to_,
                                from_period,
                                to_period,
                                start_reason,
                                end_reason
                            ))
                        
                        # add cards
                        for card in lineup['cards']:
                            time = card['time']
                            card_type_id = card['card_type']
                            reason = card['reason']
                            period = card['period']
                            card_.append((
                                match_id,
                                person_id,
                                time,
                                card_type_id,
                                reason,
                                period
                            ))

                # add events
                path = 'data/events/' + str(match_id) + '.json'
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
                    off_camera = 'off_camera' in item
                    common = (
                        match_id,
                        team_id,
                        person_id,
                        play_id,
                        position_id,
                        period,
                        minute,
                        second,
                        possession,
                        possession_id,
                        x,
                        y,
                        duration,
                        under_pressure
                    )
                    match type_id:
                        case 2:
                            ball_recovery_ = item.get('ball_recovery', {})
                            offensive = 'offensive' in ball_recovery_
                            recovery_failure = 'recovery_failure' in ball_recovery_
                            ball_recovery.append(common + (
                                offensive,
                                recovery_failure
                            ))
                        case 3:
                            dispossessed.append(common)
                        case 4:
                            duel_ = item['duel']
                            duel_type_id = duel_['type']['id']
                            duel_outcome_id = duel_.get('outcome', {}).get('id')
                            duel.append(common + (
                                counter_pressure,
                                duel_type_id,
                                duel_outcome_id
                            ))
                        case 5:
                            camera_on.append(common)
                        case 6:
                            block_ = item.get('block', {})
                            deflection = 'deflection' in block_
                            offensive = 'offensive' in block_
                            save_block = 'save_block' in block_
                            block.append(common + (
                                counter_pressure,
                                deflection,
                                offensive,
                                save_block
                            ))
                        case 8:
                            offside.append(common)
                        case 9:
                            clearance_ = item.get('clearance')
                            aerial_won = 'aerial_won' in clearance_
                            body_part_id = clearance_['body_part']['id']
                            clearance.append(common + (
                                aerial_won,
                                body_part_id
                            ))
                        case 10:
                            interception.append(common)
                        case 14:
                            dribble_ = item['dribble']
                            overrun = 'overrun' in dribble_
                            nutmeg = 'nutmeg' in dribble_
                            no_touch = 'no_touch' in dribble_
                            outcome_id = dribble_['outcome']['id']
                            dribble.append(common + (
                                overrun,
                                nutmeg,
                                no_touch,
                                outcome_id
                            ))
                        case 16:
                            shot_ = item['shot']
                            xg = shot_['statsbomb_xg']
                            first_time = 'first_time' in shot_
                            end_x = shot_['end_location'][0]
                            end_y = shot_['end_location'][1]
                            end_z = (shot_['end_location'][2] if
                                len(shot_['end_location']) > 2 else 0)
                            aerial_won = 'aerial_won' in shot_
                            follows_dribble = 'follows_dribble' in shot_
                            open_goal = 'open_goal' in shot_
                            deflected = 'defleceted' in shot_
                            technique_id = shot_['technique']['id']
                            body_part_id = shot_['body_part']['id']
                            type_id = shot_['type']['id']
                            outcome_id = shot_['outcome']['id']
                            shot.append(common + (
                                shot_id,
                                xg,
                                first_time,
                                end_x,
                                end_y,
                                end_z,
                                aerial_won,
                                follows_dribble,
                                open_goal,
                                deflected,
                                technique_id,
                                body_part_id,
                                type_id,
                                outcome_id
                            ))
                            for frame in shot_.get('freeze_frame', []):
                                x_ = frame['location'][0]
                                y_ = frame['location'][1]
                                person_id = frame['player']['id']
                                position_id = frame['position']['id']
                                freeze_frame.append((
                                    shot_id,
                                    person_id,
                                    x_,
                                    y_,
                                    position_id
                                ))
                            shot_id += 1
                        case 17:
                            pressure.append(common + (counter_pressure, ))
                        case 18:
                            half_start_ = item.get('half_start', {})
                            late_video_start = 'late_video_start' in half_start_
                            half_start.append(common + (late_video_start, ))
                        case 19:
                            substitution_ = item['substitution']
                            replacement_id = substitution_['replacement']['id']
                            outcome_id = substitution_['outcome']['id']
                            substitution.append(common + (
                                replacement_id,
                                outcome_id
                            ))
                        case 20:
                            own_goal_against.append(common)
                        case 21:
                            foul_won_ = item.get('foul_won', {})
                            defensive = 'defensive' in foul_won_
                            advantage = 'advantage' in foul_won_
                            penalty = 'penalty' in foul_won_
                            foul_won.append(common + (
                                defensive,
                                advantage,
                                penalty
                            ))
                        case 22:
                            foul_committed_ = item.get('foul_committed', {})
                            offensive = 'offensive' in foul_committed_
                            type_id = foul_committed_.get('type', {}).get('id')
                            advantage = 'advantage' in foul_committed_
                            penalty = 'penalty' in foul_committed_
                            card_id = foul_committed_.get('card', {}).get('id')
                            foul_committed.append(common + (
                                counter_pressure,
                                offensive,
                                type_id,
                                advantage,
                                penalty,
                                card_id
                            ))
                        case 23:
                            goal_keeper_ = item.get('goal_keeper', {})
                            stance_id = goal_keeper_.get('stance', {}).get('id')
                            technique_id = goal_keeper_.get('technique', {}).get('id')
                            body_part_id = goal_keeper_.get('body_part', {}).get('id')
                            type_id = goal_keeper_.get('type', {}).get('id')
                            outcome_id = goal_keeper_.get('outcome', {}).get('id')
                            goal_keeper.append(common + (
                                stance_id,
                                technique_id,
                                body_part_id,
                                type_id,
                                outcome_id
                            ))
                        case 24:
                            bad_behaviour_ = item.get('bad_behaviour', {})
                            card_id = bad_behaviour_.get('card', {}).get('id')
                            bad_behaviour.append(common + (card_id, ))
                        case 25:
                            own_goal_for.append(common)
                        case 26:
                            player_on.append(common)
                        case 27:
                            player_off_ = item.get('player_off', {})
                            permanent = 'permanent' in player_off_
                            player_off.append(common + (permanent, ))
                        case 28:
                            shield.append(common)
                        case 30:
                            pass__ = item['pass']
                            recipient_id = pass__.get('recipient', {}).get('id')
                            length = pass__['length']
                            angle = pass__['angle']
                            height_id = pass__['height']['id']
                            end_x = pass__['end_location'][0]
                            end_y = pass__['end_location'][1]
                            backheel = 'backheel' in pass__
                            deflected = 'deflected' in pass__
                            miscommunication = 'miscommunication' in pass__
                            cross = 'cross' in pass__
                            cut_back = 'cut_back' in pass__
                            switch = 'switch' in pass__
                            shot_assist = 'shot_assist' in pass__
                            goal_assist = 'goal_assist' in pass__
                            body_part_id = pass__.get('body_part', {}).get('id')
                            type_id = pass__.get('type', {}).get('id')
                            outcome_id = pass__.get('outcome', {}).get('id')
                            technique_id = pass__.get('technique', {}).get('id')
                            pass_.append(common + (
                                recipient_id,
                                length,
                                angle,
                                height_id,
                                end_x,
                                end_y,
                                backheel,
                                deflected,
                                miscommunication,
                                cross,
                                cut_back,
                                switch,
                                shot_assist,
                                goal_assist,
                                body_part_id,
                                type_id,
                                outcome_id,
                                technique_id,
                                off_camera
                            ))
                        case 33:
                            fifty_fifty_ = item['50_50']
                            outcome_id = fifty_fifty_['outcome']['id']
                            fifty_fifty.append(common + (
                                outcome_id,
                                counter_pressure
                            ))
                        case 34:
                            half_end_ = item.get('half_end', {})
                            early_video_start = 'early_video_start' in half_end_
                            match_suspended = 'match_suspended' in half_end_
                            half_end.append(common + (
                                early_video_start,
                                match_suspended
                            ))
                        case 35:
                            tactics_ = item['tactics']
                            for lineup in tactics_['lineup']:
                                person_id = lineup['player']['id']
                                position_id = lineup['position']['id']
                                jersey_number = lineup['jersey_number']
                                starting_xi.append((
                                    match_id,
                                    team_id,
                                    person_id,
                                    position_id,
                                    jersey_number
                                ))
                        case 36:
                            tactical_shift.append(common)
                        case 37:
                            error.append(common)
                        case 38:
                            miscontrol_ = item.get('miscontrol', {})
                            aerial_won = 'aerial_won' in miscontrol_
                            miscontrol.append(common + (aerial_won, ))
                        case 39:
                            dribbled_past.append(common + (counter_pressure, ))
                        case 40:
                            injury_stoppage_ = item.get('injury_stoppage', {})
                            in_chain = 'in_chain' in injury_stoppage_
                            injury_stoppage.append(common + (in_chain, ))
                        case 41:
                            referee_ball_drop.append(common + (off_camera, ))
                        case 42:
                            ball_receipt_ = item.get('ball_receipt', {})
                            outcome_id = ball_receipt_.get('outcome', {}).get('id')
                            ball_receipt.append(common + (outcome_id, ))
                        case 43:
                            carry_ = item['carry']
                            end_x = carry_['end_location'][0]
                            end_y = carry_['end_location'][1]
                            carry.append(common + (
                                end_x,
                                end_y
                            ))

    # run sql
    cursor.executemany(sql.country, country)
    cursor.executemany(sql.stadium, stadium)
    cursor.executemany(sql.team, team)
    cursor.executemany(sql.match_, match_)
    cursor.executemany(sql.person, person)
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
    cursor.executemany(sql.freeze_frame, freeze_frame)
    cursor.executemany(sql.lineup, lineup_)
    cursor.executemany(sql.card, card_)
    cursor.executemany(sql.manager, manager_)
    cursor.executemany(sql.referee, referee)

def export():
    os.environ['PGPASSWORD'] = password
    subprocess.run([
        'pg_dump.exe',
        '--file', os.path.join('..', 'dbexport.sql'),
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
    download()

    # json to sql
    connection = psycopg.connect(
        dbname=name,
        user=username,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()
    cursor.execute(sql.drop)
    cursor.execute(sql.create)
    populate(cursor)
    
    # export sql
    connection.commit()
    cursor.close()
    connection.close()
    export()

if __name__ == '__main__':
    main()
