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

CREATE TABLE lineup (
    game_id INT,
    person_id INT,
    position_id INT,
    jersey_number INT,
    from_ DATE,
    to_ DATE,
    from_period INT,
    to_period INT,
    FOREIGN KEY (game_id) REFERENCES game (game_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id)
);

CREATE TABLE stadium (
    stadium_id INT PRIMARY KEY,
    stadium_name VARCHAR(128),
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country (country_id)
);

CREATE TABLE game (
    game_id INT PRIMARY KEY,
    game_date DATE,
    kick_off VARCHAR(32),
    country_id INT,
    season_id INT,
    home_team_id INT,
    away_team_id INT,
    home_team_gender VARCHAR(32),
    away_team_gender VARCHAR(32),
    home_score INT,
    away_score INT,
    game_week INT,
    competition_stage VARCHAR(32),
    stadium_id INT,
    FOREIGN KEY (home_team_id) REFERENCES team (team_id),
    FOREIGN KEY (away_team_id) REFERENCES team (team_id),
    FOREIGN KEY (season_id) REFERENCES season (season_id),
    FOREIGN KEY (country_id) REFERENCES country (country_id),
    FOREIGN KEY (stadium_id) REFERENCES stadium (stadium_id)
);

CREATE TABLE card (
    game_id INT,
    person_id INT,
    time DATE,
    type_id INT,
    reason VARCHAR(32),
    period INT,
    FOREIGN KEY (game_id) REFERENCES game (game_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (type_id) REFERENCES definition (definition_id)
);

CREATE TABLE manager (
    game_id INT,
    person_id INT,
    FOREIGN KEY (game_id) REFERENCES game (game_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id)
);

CREATE TABLE ball_recovery (
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
    recovery_failure BOOLEAN
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (play_id) REFERENCES play (play_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (possession_id) REFERENCES team (team_id)
);

CREATE TABLE dispossessed (
) INHERITS (common);
CREATE TABLE duel (
    counter_pressure BOOLEAN,
    type_id INT,
    outcome_id INT,
    FOREIGN KEY (type_id) REFERENCES definition (definition_id),
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE camera_on (
) INHERITS (common);
CREATE TABLE block (
    counter_pressure BOOLEAN,
    deflection BOOLEAN,
    offensive BOOLEAN,
    save_block BOOLEAN
) INHERITS (common);
CREATE TABLE offside (
) INHERITS (common);
CREATE TABLE clearance (
    aerial_won BOOLEAN,
    body_part_id INT,
    FOREIGN KEY (body_part_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE interception (
) INHERITS (common);
CREATE TABLE dribble (
    overrun BOOLEAN,
    nutmeg BOOLEAN,
    no_touch BOOLEAN,
    outcome_id INT,
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE shot (
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
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE pressure (
    counter_pressure BOOLEAN
) INHERITS (common);
CREATE TABLE half_start (
    late_video_start BOOLEAN
) INHERITS (common);
CREATE TABLE substitution (
    replacement_id INT,
    outcome_id INT,
    FOREIGN KEY (replacement_id) REFERENCES person (person_id),
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE own_goal_against (
) INHERITS (common);
CREATE TABLE foul_won (
    defensive BOOLEAN,
    advantage BOOLEAN,
    penalty BOOLEAN
) INHERITS (common);
CREATE TABLE foul_committed (
    counter_pressure BOOLEAN,
    offensive BOOLEAN,
    type_id INT,
    advantage BOOLEAN,
    penalty BOOLEAN,
    card_id INT,
    FOREIGN KEY (type_id) REFERENCES definition (definition_id),
    FOREIGN KEY (card_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE goal_keeper (
    stance_id INT,
    technique_id INT,
    body_part_id INT,
    type_id INT,
    outcome_id INT,
    FOREIGN KEY (stance_id) REFERENCES definition (definition_id),
    FOREIGN KEY (technique_id) REFERENCES definition (definition_id),
    FOREIGN KEY (body_part_id) REFERENCES definition (definition_id),
    FOREIGN KEY (type_id) REFERENCES definition (definition_id),
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE bad_behaviour (
    card_id INT,
    FOREIGN KEY (card_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE own_goal_for (
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES team (team_id)
) INHERITS (common);
CREATE TABLE person_on (
) INHERITS (common);
CREATE TABLE person_off (
    permanent BOOLEAN
) INHERITS (common);
CREATE TABLE shield (
) INHERITS (common);
CREATE TABLE pass (
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
    FOREIGN KEY (technique_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE fifty_fifty (
    outcome_id INT,
    counter_pressure BOOLEAN,
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE half_end (
    early_video_end BOOLEAN,
    game_suspended BOOLEAN
) INHERITS (common);
CREATE TABLE starting_xi (
    starting_xi_id INT PRIMARY KEY,
    team_id INT,
    season_id INT,
    FOREIGN KEY (team_id) REFERENCES team (team_id),
    FOREIGN KEY (season_id) REFERENCES season (season_id)
);
CREATE TABLE tactical_shift (
) INHERITS (common);
CREATE TABLE error (
) INHERITS (common);
CREATE TABLE miscontrol (
    aerial_won BOOLEAN
) INHERITS (common);
CREATE TABLE dribbled_past (
    counter_pressure BOOLEAN
) INHERITS (common);
CREATE TABLE injury_stoppage (
    in_chain BOOLEAN
) INHERITS (common);
CREATE TABLE referee_ball_drop (
    off_camera BOOLEAN
) INHERITS (common);
CREATE TABLE ball_receipt (
    outcome_id INT,
    FOREIGN KEY (outcome_id) REFERENCES definition (definition_id)
) INHERITS (common);
CREATE TABLE carry (
    end_x FLOAT,
    end_y FLOAT
) INHERITS (common);
CREATE TABLE freeze_frame (
    person_id INT,
    shot_id INT,
    x FLOAT,
    y FLOAT,
    position_id INT,
    FOREIGN KEY (shot_id) REFERENCES shot (shot_id),
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id)
);
CREATE TABLE formation (
    person_id INT,
    position_id INT,
    jersey_number INT,
    starting_xi_id INT,
    FOREIGN KEY (person_id) REFERENCES person (person_id),
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (starting_xi_id) REFERENCES starting_xi (starting_xi_id)
);
