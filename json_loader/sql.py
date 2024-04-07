
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
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS season;
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
CREATE TABLE ball_recovery (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE dispossessed (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE duel (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE camera_on (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE block (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE offside (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE clearance (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE interception (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE dribble (
    player_id INT,
    completed BOOLEAN,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE shot (
    player_id INT,
    xg FLOAT,
    first_time BOOLEAN,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE pressure (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE half_start (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE substitution (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE own_goal_against (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE foul_won (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE foul_committed (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE goal_keeper (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE bad_behaviour (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE own_goal_for (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE player_on (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE player_off (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE shield (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE pass (
    player_id INT,
    through_ball BOOLEAN,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE fifty_fifty (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE half_end (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE starting_xi (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE tactical_shift (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE error (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE miscontrol (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE dribbled_past (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE injury_stoppage (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE referee_ball_drop (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE ball_receipt (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
CREATE TABLE carry (
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES player (player_id)
);
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
INSERT INTO ball_recovery (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

dispossessed = '''
INSERT INTO dispossessed (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

duel = '''
INSERT INTO duel (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

camera_on = '''
INSERT INTO camera_on (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

block = '''
INSERT INTO block (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

offside = '''
INSERT INTO offside (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

clearance = '''
INSERT INTO clearance (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

interception = '''
INSERT INTO interception (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

dribble = '''
INSERT INTO dribble (player_id, completed) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s)
'''

shot = '''
INSERT INTO shot (player_id, xg, first_time) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s, %s)
'''

pressure = '''
INSERT INTO pressure (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

half_start = '''
INSERT INTO half_start (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

substitution = '''
INSERT INTO substitution (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

own_goal_against = '''
INSERT INTO own_goal_against (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

foul_won = '''
INSERT INTO foul_won (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

foul_committed = '''
INSERT INTO foul_committed (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

goal_keeper = '''
INSERT INTO goal_keeper (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

bad_behaviour = '''
INSERT INTO bad_behaviour (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

own_goal_for = '''
INSERT INTO own_goal_for (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

player_on = '''
INSERT INTO player_on (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

player_off = '''
INSERT INTO player_off (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

shield = '''
INSERT INTO shield (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

pass_ = '''
INSERT INTO pass (player_id, through_ball) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
), %s)
'''

fifty_fifty = '''
INSERT INTO fifty_fifty (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

half_end = '''
INSERT INTO half_end (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

starting_xi = '''
INSERT INTO starting_xi (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

tactical_shift = '''
INSERT INTO tactical_shift (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

error = '''
INSERT INTO error (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

miscontrol = '''
INSERT INTO miscontrol (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

dribbled_past = '''
INSERT INTO dribbled_past (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

injury_stoppage = '''
INSERT INTO injury_stoppage (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

referee_ball_drop = '''
INSERT INTO referee_ball_drop (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

ball_receipt = '''
INSERT INTO ball_receipt (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''

carry = '''
INSERT INTO carry (player_id) 
VALUES ((
    SELECT player_id 
    FROM player 
    WHERE person_id = %s AND team_id = %s AND season_id = %s 
))
'''
