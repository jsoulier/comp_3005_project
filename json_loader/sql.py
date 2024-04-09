drop = '''
DROP TABLE IF EXISTS freeze_frame;
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
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS lineup;
DROP TABLE IF EXISTS manager;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS stadium;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS season;
DROP TABLE IF EXISTS play;
DROP TABLE IF EXISTS position;
DROP TABLE IF EXISTS definition;
DROP TABLE IF EXISTS height;
'''
create = '''
CREATE TABLE position (
    position_id INT PRIMARY KEY,
    position_name VARCHAR(128)
);
INSERT INTO position VALUES (0, 'None');
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
CREATE TABLE season (
    season_id SERIAL PRIMARY KEY,
    competition_name VARCHAR(15),
    season_name VARCHAR(10),
    CONSTRAINT season_unique UNIQUE (competition_name, season_name)
);
CREATE TABLE team (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(128)
);
CREATE TABLE country (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(128)
);
CREATE TABLE person (
    person_id INT PRIMARY KEY,
    person_name VARCHAR(128),
    person_nickname VARCHAR(128),
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country (country_id)
);
CREATE TABLE stadium (
    stadium_id INT PRIMARY KEY,
    stadium_name VARCHAR(128),
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country (country_id)
);
CREATE TABLE match (
    match_id INT PRIMARY KEY,
    match_date DATE,
    kick_off VARCHAR(32),
    country_id INT,
    season_id INT,
    home_team_id INT,
    away_team_id INT,
    home_team_gender VARCHAR(32),
    away_team_gender VARCHAR(32),
    home_score INT,
    away_score INT,
    match_week INT,
    competition_stage VARCHAR(32),
    stadium_id INT,
    FOREIGN KEY (home_team_id) REFERENCES team (team_id),
    FOREIGN KEY (away_team_id) REFERENCES team (team_id),
    FOREIGN KEY (season_id) REFERENCES season (season_id),
    FOREIGN KEY (country_id) REFERENCES country (country_id),
    FOREIGN KEY (stadium_id) REFERENCES stadium (stadium_id)
);
CREATE TABLE manager (
    match_id INT,
    person_id INT,
    FOREIGN KEY (match_id) REFERENCES match (match_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id)
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
CREATE TABLE definition (
    definition_id INT PRIMARY KEY,
    definition_name VARCHAR(128)
);
INSERT INTO definition VALUES (1, 'Lost');
INSERT INTO definition VALUES (10, 'Aerial Lost');
INSERT INTO definition VALUES (100, 'Saved');
INSERT INTO definition VALUES (101, 'Wayward');
INSERT INTO definition VALUES (102, 'Injury');
INSERT INTO definition VALUES (103, 'Tactical');
INSERT INTO definition VALUES (104, 'Inswinging');
INSERT INTO definition VALUES (105, 'Outswinging');
INSERT INTO definition VALUES (106, 'No Touch');
INSERT INTO definition VALUES (107, 'Straight');
INSERT INTO definition VALUES (108, 'Through Ball');
INSERT INTO definition VALUES (109, 'Penalty Saved To Post');
INSERT INTO definition VALUES (11, 'Tackle');
INSERT INTO definition VALUES (110, 'Saved To Post');
INSERT INTO definition VALUES (113, 'Shot Saved Off Target');
INSERT INTO definition VALUES (114, 'Shot Saved To Post');
INSERT INTO definition VALUES (115, 'Saved Off Target');
INSERT INTO definition VALUES (116, 'Saved To Post');
INSERT INTO definition VALUES (117, 'Punched Out');
INSERT INTO definition VALUES (13, 'Lost In Play');
INSERT INTO definition VALUES (14, 'Lost Out');
INSERT INTO definition VALUES (15, 'Success');
INSERT INTO definition VALUES (16, 'Success In Play');
INSERT INTO definition VALUES (17, 'Success Out');
INSERT INTO definition VALUES (19, '6 Seconds');
INSERT INTO definition VALUES (2, 'Success To Opposition');
INSERT INTO definition VALUES (20, 'Backpass Pick');
INSERT INTO definition VALUES (21, 'Dangerous Play');
INSERT INTO definition VALUES (22, 'Dive');
INSERT INTO definition VALUES (23, 'Foul Out');
INSERT INTO definition VALUES (24, 'Handball');
INSERT INTO definition VALUES (25, 'Collected');
INSERT INTO definition VALUES (26, 'Goal Conceded');
INSERT INTO definition VALUES (28, 'Penalty Conceded');
INSERT INTO definition VALUES (29, 'Penalty Saved');
INSERT INTO definition VALUES (3, 'Success To Team');
INSERT INTO definition VALUES (30, 'Punch');
INSERT INTO definition VALUES (31, 'Save');
INSERT INTO definition VALUES (32, 'Shot Faced');
INSERT INTO definition VALUES (33, 'Shot Saved');
INSERT INTO definition VALUES (34, 'Smother');
INSERT INTO definition VALUES (35, 'Both Hands');
INSERT INTO definition VALUES (36, 'Chest');
INSERT INTO definition VALUES (37, 'Head');
INSERT INTO definition VALUES (38, 'Left Foot');
INSERT INTO definition VALUES (39, 'Left Hand');
INSERT INTO definition VALUES (4, 'Won');
INSERT INTO definition VALUES (40, 'Right Foot');
INSERT INTO definition VALUES (41, 'Right Hand');
INSERT INTO definition VALUES (42, 'Moving');
INSERT INTO definition VALUES (43, 'Prone');
INSERT INTO definition VALUES (44, 'Set');
INSERT INTO definition VALUES (45, 'Diving');
INSERT INTO definition VALUES (46, 'Standing');
INSERT INTO definition VALUES (47, 'Claim');
INSERT INTO definition VALUES (48, 'Clear');
INSERT INTO definition VALUES (49, 'Collected Twice');
INSERT INTO definition VALUES (5, 'Yellow Card');
INSERT INTO definition VALUES (50, 'Fail');
INSERT INTO definition VALUES (51, 'In Play');
INSERT INTO definition VALUES (52, 'In Play Danger');
INSERT INTO definition VALUES (53, 'In Play Safe');
INSERT INTO definition VALUES (55, 'No Touch');
INSERT INTO definition VALUES (56, 'Saved Twice');
INSERT INTO definition VALUES (58, 'Touched In');
INSERT INTO definition VALUES (6, 'Second Yellow');
INSERT INTO definition VALUES (61, 'Corner');
INSERT INTO definition VALUES (62, 'Free Kick');
INSERT INTO definition VALUES (63, 'Goal Kick');
INSERT INTO definition VALUES (64, 'Interception');
INSERT INTO definition VALUES (65, 'Kick Off');
INSERT INTO definition VALUES (66, 'Recovery');
INSERT INTO definition VALUES (67, 'Throw In');
INSERT INTO definition VALUES (68, 'Drop Kick');
INSERT INTO definition VALUES (69, 'Keeper Arm');
INSERT INTO definition VALUES (7, 'Red Card');
INSERT INTO definition VALUES (70, 'Other');
INSERT INTO definition VALUES (74, 'Injury Clearance');
INSERT INTO definition VALUES (75, 'Out');
INSERT INTO definition VALUES (76, 'Pass Offside');
INSERT INTO definition VALUES (77, 'Unknown');
INSERT INTO definition VALUES (8, 'Complete');
INSERT INTO definition VALUES (87, 'Open Play');
INSERT INTO definition VALUES (88, 'Penalty');
INSERT INTO definition VALUES (89, 'Through Ball');
INSERT INTO definition VALUES (9, 'Incomplete');
INSERT INTO definition VALUES (90, 'Diving Header');
INSERT INTO definition VALUES (91, 'Half Volley');
INSERT INTO definition VALUES (92, 'Lob');
INSERT INTO definition VALUES (93, 'Normal');
INSERT INTO definition VALUES (94, 'Overhead Kick');
INSERT INTO definition VALUES (95, 'Volley');
INSERT INTO definition VALUES (96, 'Blocked');
INSERT INTO definition VALUES (97, 'Goal');
INSERT INTO definition VALUES (98, 'Off Target');
INSERT INTO definition VALUES (99, 'Post');
CREATE TABLE height (
    height_id INT PRIMARY KEY,
    height_name VARCHAR(128)
);
INSERT INTO height VALUES (1, 'Ground Pass');
INSERT INTO height VALUES (2, 'Low Pass');
INSERT INTO height VALUES (3, 'High Pass');
CREATE TABLE lineup (
    match_id INT,
    person_id INT,
    position_id INT,
    jersey_number INT,
    from_ DATE,
    to_ DATE,
    from_period INT,
    to_period INT,
    FOREIGN KEY (match_id) REFERENCES match (match_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id)
);
CREATE TABLE card (
    match_id INT,
    person_id INT,
    time VARCHAR(32),
    type_id INT,
    reason VARCHAR(32),
    period INT,
    FOREIGN KEY (match_id) REFERENCES match (match_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (type_id) REFERENCES definition (definition_id)
);
CREATE TABLE ball_recovery (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    offensive BOOLEAN,
    recovery_failure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE dispossessed (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE duel (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    counter_pressure BOOLEAN,
    type_id INT,
    outcome_id INT,
    FOREIGN KEY (type_id) REFERENCES definition (definition_id),
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE camera_on (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE block (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    counter_pressure BOOLEAN,
    deflection BOOLEAN,
    offensive BOOLEAN,
    save_block BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE offside (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE clearance (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    aerial_won BOOLEAN,
    body_part_id INT,
    FOREIGN KEY (body_part_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE interception (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE dribble (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    overrun BOOLEAN,
    nutmeg BOOLEAN,
    no_touch BOOLEAN,
    outcome_id INT,
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE shot (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    shot_id INT PRIMARY KEY,
    end_x FLOAT,
    end_y FLOAT,
    end_z FLOAT,
    aerial_won BOOLEAN,
    follows_dribble BOOLEAN,
    open_goal BOOLEAN,
    xg FLOAT,
    deflected BOOLEAN,
    technique_id INT,
    first_time BOOLEAN,
    body_part_id INT,
    type_id INT,
    outcome_id INT,
    FOREIGN KEY (technique_id) REFERENCES definition (definition_id),
    FOREIGN KEY (body_part_id) REFERENCES definition (definition_id),
    FOREIGN KEY (type_id) REFERENCES definition (definition_id),
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE pressure (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    counter_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE half_start (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    late_video_start BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE substitution (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    replacement_id INT,
    outcome_id INT,
    FOREIGN KEY (replacement_id) REFERENCES person (person_id),
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE own_goal_against (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE foul_won (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    defensive BOOLEAN,
    advantage BOOLEAN,
    penalty BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE foul_committed (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    counter_pressure BOOLEAN,
    offensive BOOLEAN,
    type_id INT,
    advantage BOOLEAN,
    penalty BOOLEAN,
    card_id INT,
    FOREIGN KEY (type_id) REFERENCES definition (definition_id),
    FOREIGN KEY (card_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE goal_keeper (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    stance_id INT,
    technique_id INT,
    body_part_id INT,
    type_id INT,
    outcome_id INT,
    FOREIGN KEY (stance_id) REFERENCES definition (definition_id),
    FOREIGN KEY (technique_id) REFERENCES definition (definition_id),
    FOREIGN KEY (body_part_id) REFERENCES definition (definition_id),
    FOREIGN KEY (type_id) REFERENCES definition (definition_id),
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE bad_behaviour (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    card_id INT,
    FOREIGN KEY (card_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE own_goal_for (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES team (team_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE player_on (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE player_off (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    permanent BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE shield (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE pass (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    recipient_id INT,
    length FLOAT,
    angle FLOAT,
    height_id INT,
    end_x FLOAT,
    end_y FLOAT,
    backheel BOOLEAN,
    deflected BOOLEAN,
    miscommunication BOOLEAN,
    cross_ BOOLEAN,
    cut_back BOOLEAN,
    switch BOOLEAN,
    shot_assist BOOLEAN,
    goal_assist BOOLEAN,
    body_part_id INT,
    type_id INT,
    outcome_id INT,
    technique_id INT,
    off_camera BOOLEAN,
    FOREIGN KEY (recipient_id) REFERENCES person (person_id),
    FOREIGN KEY (height_id) REFERENCES height (height_id),
    FOREIGN KEY (body_part_id) REFERENCES definition (definition_id),
    FOREIGN KEY (type_id) REFERENCES definition (definition_id),
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id),
    FOREIGN KEY (technique_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE fifty_fifty (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    outcome_id INT,
    counter_pressure BOOLEAN,
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE half_end (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    early_video_end BOOLEAN,
    match_suspended BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE starting_xi (
    match_id INT,
    person_id INT,
    position_id INT,
    jersey_number INT,
    FOREIGN KEY (match_id) REFERENCES match (match_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id)
);
CREATE TABLE tactical_shift (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE error (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE miscontrol (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    aerial_won BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE dribbled_past (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    counter_pressure BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE injury_stoppage (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    in_chain BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE referee_ball_drop (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE ball_receipt (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    outcome_id INT,
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE carry (
    match_id INT,
    person_id INT,
    play_id INT,
    position_id INT,
    period INT,
    minute INT,
    second INT,
    possession INT,
    possession_id INT,
    x FLOAT,
    y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    end_x FLOAT,
    end_y FLOAT,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);
CREATE TABLE freeze_frame (
    shot_id INT,
    person_id INT,
    x FLOAT,
    y FLOAT,
    position_id INT,
    FOREIGN KEY (shot_id) REFERENCES shot (shot_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id)
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
stadium = '''
INSERT INTO stadium (stadium_id, stadium_name, country_id)
VALUES (%s, %s, %s)
ON CONFLICT DO NOTHING;
'''
country = '''
INSERT INTO country (country_id, country_name)
VALUES (%s, %s)
ON CONFLICT DO NOTHING;
'''
person = '''
INSERT INTO person (person_id, person_name, person_nickname, country_id)
VALUES (%s, %s, %s, %s)
ON CONFLICT DO NOTHING;
'''
ball_recovery = '''
INSERT INTO ball_recovery (
    match_id,
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
    under_pressure,
    offensive,
    recovery_failure
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
dispossessed = '''
INSERT INTO dispossessed (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
duel = '''
INSERT INTO duel (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, type_id, outcome_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
camera_on = '''
INSERT INTO camera_on (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
block = '''
INSERT INTO block (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, deflection, offensive, save_block)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
offside = '''
INSERT INTO offside (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
clearance = '''
INSERT INTO clearance (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, aerial_won, body_part_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
interception = '''
INSERT INTO interception (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
dribble = '''
INSERT INTO dribble (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, overrun, nutmeg, no_touch, outcome_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
shot = '''
INSERT INTO shot (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, shot_id, xg, first_time, end_x, end_y, end_z, aerial_won, follows_dribble, open_goal, deflected, technique_id, body_part_id, type_id, outcome_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
pressure = '''
INSERT INTO pressure (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
half_start = '''
INSERT INTO half_start (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, late_video_start)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
substitution = '''
INSERT INTO substitution (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, replacement_id, outcome_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
own_goal_against = '''
INSERT INTO own_goal_against (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
foul_won = '''
INSERT INTO foul_won (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, defensive, advantage, penalty)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
foul_committed = '''
INSERT INTO foul_committed (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure, offensive, type_id, advantage, penalty, card_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
goal_keeper = '''
INSERT INTO goal_keeper (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, stance_id, technique_id, body_part_id, type_id, outcome_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
bad_behaviour = '''
INSERT INTO bad_behaviour (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, card_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
own_goal_for = '''
INSERT INTO own_goal_for (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, team_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
player_on = '''
INSERT INTO player_on (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
player_off = '''
INSERT INTO player_off (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, permanent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
shield = '''
INSERT INTO shield (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
pass_ = '''
INSERT INTO pass (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, recipient_id, length, angle, height_id, end_x, end_y, backheel, deflected, miscommunication, cross_, cut_back, switch, shot_assist, goal_assist, body_part_id, type_id, outcome_id, technique_id, off_camera)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
fifty_fifty = '''
INSERT INTO fifty_fifty (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, outcome_id, counter_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
half_end = '''
INSERT INTO half_end (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, early_video_end, match_suspended)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
starting_xi = '''
INSERT INTO starting_xi (match_id, person_id, position_id, jersey_number)
VALUES (%s, %s, %s, %s)
'''
tactical_shift = '''
INSERT INTO tactical_shift (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
error = '''
INSERT INTO error (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
miscontrol = '''
INSERT INTO miscontrol (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, aerial_won)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
dribbled_past = '''
INSERT INTO dribbled_past (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, counter_pressure)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
injury_stoppage = '''
INSERT INTO injury_stoppage (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, in_chain)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
referee_ball_drop = '''
INSERT INTO referee_ball_drop (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, off_camera)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
ball_receipt = '''
INSERT INTO ball_receipt (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, outcome_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
carry = '''
INSERT INTO carry (match_id, person_id, play_id, position_id, period, minute, second, possession, possession_id, x, y, duration, under_pressure, end_x, end_y)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
freeze_frame = '''
INSERT INTO freeze_frame (shot_id, person_id, x, y, position_id)
VALUES (%s, %s, %s, %s, %s)
'''
match_ = '''
INSERT INTO match (match_id, match_date, kick_off, country_id, season_id, home_team_id, away_team_id, home_team_gender, away_team_gender, home_score, away_score, match_week, competition_stage, stadium_id)
VALUES (%s, %s, %s, (
    SELECT country_id
    FROM country
    WHERE country.country_name = %s
), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
