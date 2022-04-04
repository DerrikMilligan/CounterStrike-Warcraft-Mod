DROP TABLE player;
CREATE TABLE player ( id INTEGER PRIMARY KEY, steam_id TEXT UNIQUE, current_race NUMERIC );
CREATE INDEX index_player_current_race on player ( current_race asc );

DROP TABLE race;
CREATE TABLE race (id INTEGER PRIMARY KEY, name TEXT unique);
CREATE UNIQUE INDEX index_race_name on race ( name ASC );

DROP TABLE xp;
CREATE TABLE xp (
id        INTEGER PRIMARY KEY,
player_id NUMERIC,
race_id   NUMERIC,
xp        NUMERIC,
level     NUMERIC,
skill_1   NUMERIC,
skill_2   NUMERIC,
skill_3   NUMERIC,
skill_4   NUMERIC,
skill_5   NUMERIC,
skill_6   NUMERIC,
skill_7   NUMERIC,
skill_8   NUMERIC,
skill_9   NUMERIC,
skill_10  NUMERIC );
CREATE INDEX index_xp_player_id on xp (player_id asc);
CREATE INDEX index_xp_race_id   on xp (race_id asc);