drop = '''
DROP TABLE IF EXISTS ball_recovery;
DROP TABLE IF EXISTS dispossessed;
DROP TABLE IF EXISTS duel;
DROP TABLE IF EXISTS camera_on;
DROP TABLE IF EXISTS block;
DROP TABLE IF EXISTS offside;
DROP TABLE IF EXISTS clearance;
DROP TABLE IF EXISTS interception;
DROP TABLE IF EXISTS dribble;
DROP TABLE IF EXISTS shot;
DROP TABLE IF EXISTS pressure;
DROP TABLE IF EXISTS half_start;
DROP TABLE IF EXISTS substitution;
DROP TABLE IF EXISTS own_goal_against;
DROP TABLE IF EXISTS foul_won;
DROP TABLE IF EXISTS foul_committed;
DROP TABLE IF EXISTS goal_keeper;
DROP TABLE IF EXISTS bad_behaviour;
DROP TABLE IF EXISTS own_goal_for;
DROP TABLE IF EXISTS player_on;
DROP TABLE IF EXISTS player_off;
DROP TABLE IF EXISTS shield;
DROP TABLE IF EXISTS pass;
DROP TABLE IF EXISTS fifty_fifty;
DROP TABLE IF EXISTS half_end;
DROP TABLE IF EXISTS starting_xi;
DROP TABLE IF EXISTS tactical_shift;
DROP TABLE IF EXISTS error;
DROP TABLE IF EXISTS miscontrol;
DROP TABLE IF EXISTS dribbled_past;
DROP TABLE IF EXISTS injury_stoppage;
DROP TABLE IF EXISTS referee_ball_drop;
DROP TABLE IF EXISTS ball_receipt;
DROP TABLE IF EXISTS carry;
DROP TABLE IF EXISTS common;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS season;
DROP TABLE IF EXISTS play;
DROP TABLE IF EXISTS position;
DROP TABLE IF EXISTS duel_type;
'''
create = '''
CREATE TABLE season (
    season_id SERIAL PRIMARY KEY,
    competition_name VARCHAR(15),
    season_name VARCHAR(10),
    CONSTRAINT season_unique UNIQUE (competition_name, season_name)
);
CREATE TABLE person (
    person_id INT PRIMARY KEY,
    person_name VARCHAR(128)
);
CREATE TABLE team (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(128)
);
CREATE TABLE player (
    player_id SERIAL PRIMARY KEY,
    person_id INT,
    team_id INT,
    season_id INT,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (season_id) REFERENCES season (season_id),
    FOREIGN KEY (team_id) REFERENCES team (team_id),
    CONSTRAINT player_unique UNIQUE (person_id, season_id, team_id)
);
CREATE TABLE play (
    play_id INT PRIMARY KEY,
    play_name VARCHAR(128)
);
INSERT INTO play VALUES (1, 'Regular Play');
INSERT INTO play VALUES (2, 'From Corner');
INSERT INTO play VALUES (3, 'From Free Kick');
INSERT INTO play VALUES (4, 'From Throw In');
INSERT INTO play VALUES (5, 'Other');
INSERT INTO play VALUES (6, 'From Counter');
INSERT INTO play VALUES (7, 'From Goal Kick');
INSERT INTO play VALUES (8, 'From Keeper');
INSERT INTO play VALUES (9, 'From Kick Off');
CREATE TABLE position (
    position_id INT PRIMARY KEY,
    position_name VARCHAR(128)
);
INSERT INTO position VALUES (1, 'Goalkeeper');
INSERT INTO position VALUES (2, 'Right Back');
INSERT INTO position VALUES (3, 'Right Center Back');
INSERT INTO position VALUES (4, 'Center Back');
INSERT INTO position VALUES (5, 'Left Center Back');
INSERT INTO position VALUES (6, 'Left Back');
INSERT INTO position VALUES (7, 'Right Wing Back');
INSERT INTO position VALUES (8, 'Left Wing Back');
INSERT INTO position VALUES (9, 'Right Defensive Midfield');
INSERT INTO position VALUES (10, 'Center Defensive Midfield');
INSERT INTO position VALUES (11, 'Left Defensive Midfield');
INSERT INTO position VALUES (12, 'Right Midfield');
INSERT INTO position VALUES (13, 'Right Center Midfield');
INSERT INTO position VALUES (14, 'Center Midfield');
INSERT INTO position VALUES (15, 'Left Center Midfield');
INSERT INTO position VALUES (16, 'Left Midfield');
INSERT INTO position VALUES (17, 'Ring Wing');
INSERT INTO position VALUES (18, 'Right Attacking Midfield');
INSERT INTO position VALUES (19, 'Center Attacking Midfield');
INSERT INTO position VALUES (20, 'Left Attacking Midfield');
INSERT INTO position VALUES (21, 'Left Wing');
INSERT INTO position VALUES (22, 'Right Center Forward');
INSERT INTO position VALUES (23, 'Striker');
INSERT INTO position VALUES (24, 'Left Center Forward');
INSERT INTO position VALUES (25, 'Secondary Striker');
CREATE TABLE duel_type (
    duel_type_id INT PRIMARY KEY,
    duel_type_name VARCHAR(128)
);
INSERT INTO duel_type VALUES (1, 'Lost');
INSERT INTO duel_type VALUES (4, 'Won');
INSERT INTO duel_type VALUES (10, 'Aerial Lost');
INSERT INTO duel_type VALUES (11, 'Tackle');
INSERT INTO duel_type VALUES (13, 'Lost In Play');
INSERT INTO duel_type VALUES (14, 'Lost Out');
INSERT INTO duel_type VALUES (15, 'Success');
INSERT INTO duel_type VALUES (16, 'Success In Play');
INSERT INTO duel_type VALUES (17, 'Success Out');
CREATE TABLE common (
    player_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x INT,
    y INT,
    duration FLOAT,
    under_pressure BOOLEAN,
    counter_pressure BOOLEAN,
    FOREIGN KEY (player_id) REFERENCES player (player_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE ball_recovery (
    offensive BOOLEAN,
    recovery_failure BOOLEAN
) INHERITS (common);
CREATE TABLE dispossessed (
) INHERITS (common);
CREATE TABLE duel (
    duel_type_id INT,
    duel_outcome_id INT
) INHERITS (common);
CREATE TABLE camera_on (
) INHERITS (common);
CREATE TABLE block (
    deflection BOOLEAN,
    offensive BOOLEAN,
    save_block BOOLEAN
) INHERITS (common);
CREATE TABLE offside (
) INHERITS (common);
CREATE TABLE clearance (
) INHERITS (common);
CREATE TABLE interception (
) INHERITS (common);
CREATE TABLE dribble (
    completed BOOLEAN
) INHERITS (common);
CREATE TABLE shot (
    xg FLOAT,
    first_time BOOLEAN
) INHERITS (common);
CREATE TABLE pressure (
) INHERITS (common);
CREATE TABLE half_start (
) INHERITS (common);
CREATE TABLE substitution (
) INHERITS (common);
CREATE TABLE own_goal_against (
) INHERITS (common);
CREATE TABLE foul_won (
) INHERITS (common);
CREATE TABLE foul_committed (
) INHERITS (common);
CREATE TABLE goal_keeper (
) INHERITS (common);
CREATE TABLE bad_behaviour (
) INHERITS (common);
CREATE TABLE own_goal_for (
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES team (team_id)
) INHERITS (common);
CREATE TABLE player_on (
) INHERITS (common);
CREATE TABLE player_off (
) INHERITS (common);
CREATE TABLE shield (
) INHERITS (common);
CREATE TABLE pass (
    through_ball BOOLEAN
) INHERITS (common);
CREATE TABLE fifty_fifty (
) INHERITS (common);
CREATE TABLE half_end (
) INHERITS (common);
CREATE TABLE starting_xi (
) INHERITS (common);
CREATE TABLE tactical_shift (
) INHERITS (common);
CREATE TABLE error (
) INHERITS (common);
CREATE TABLE miscontrol (
) INHERITS (common);
CREATE TABLE dribbled_past (
) INHERITS (common);
CREATE TABLE injury_stoppage (
) INHERITS (common);
CREATE TABLE referee_ball_drop (
) INHERITS (common);
CREATE TABLE ball_receipt (
) INHERITS (common);
CREATE TABLE carry (
) INHERITS (common);
'''
season = '''
INSERT INTO season (competition_name, season_name)
VALUES (%s, %s)
ON CONFLICT ON CONSTRAINT season_unique DO UPDATE
SET season_name = season.season_name
RETURNING *;
'''
team = '''
INSERT INTO team (team_id, team_name) 
VALUES (%s, %s) 
ON CONFLICT DO NOTHING;
'''
person = '''
INSERT INTO person (person_id, person_name) 
VALUES (%s, %s) 
ON CONFLICT DO NOTHING;
'''
player = '''
INSERT INTO player (person_id, team_id, season_id) 
VALUES (%s, %s, %s) 
ON CONFLICT ON CONSTRAINT player_unique DO NOTHING;
'''
ball_recovery = '''
INSERT INTO ball_recovery (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, offensive, recovery_failure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
dispossessed = '''
INSERT INTO dispossessed (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
duel = '''
INSERT INTO duel (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, duel_type_id, duel_outcome_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
camera_on = '''
INSERT INTO camera_on (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
block = '''
INSERT INTO block (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, deflection, offensive, save_block) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
offside = '''
INSERT INTO offside (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
clearance = '''
INSERT INTO clearance (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
interception = '''
INSERT INTO interception (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
dribble = '''
INSERT INTO dribble (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, completed) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
shot = '''
INSERT INTO shot (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, xg, first_time) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
pressure = '''
INSERT INTO pressure (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
half_start = '''
INSERT INTO half_start (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
substitution = '''
INSERT INTO substitution (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
own_goal_against = '''
INSERT INTO own_goal_against (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
foul_won = '''
INSERT INTO foul_won (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
foul_committed = '''
INSERT INTO foul_committed (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
goal_keeper = '''
INSERT INTO goal_keeper (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
bad_behaviour = '''
INSERT INTO bad_behaviour (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
own_goal_for = '''
INSERT INTO own_goal_for (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, team_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
player_on = '''
INSERT INTO player_on (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
player_off = '''
INSERT INTO player_off (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
shield = '''
INSERT INTO shield (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
pass_ = '''
INSERT INTO pass (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, through_ball) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
fifty_fifty = '''
INSERT INTO fifty_fifty (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
half_end = '''
INSERT INTO half_end (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
starting_xi = '''
INSERT INTO starting_xi (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
tactical_shift = '''
INSERT INTO tactical_shift (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
error = '''
INSERT INTO error (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
miscontrol = '''
INSERT INTO miscontrol (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
dribbled_past = '''
INSERT INTO dribbled_past (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
injury_stoppage = '''
INSERT INTO injury_stoppage (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
referee_ball_drop = '''
INSERT INTO referee_ball_drop (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
ball_receipt = '''
INSERT INTO ball_receipt (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
carry = '''
INSERT INTO carry (player_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
