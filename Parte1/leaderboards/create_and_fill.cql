CREATE KEYSPACE IF NOT EXISTS dungeons WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};

USE dungeons;

CREATE TABLE IF NOT EXISTS hall_of_fame (
    country text,
    dungeon_id int,
    dungeon_name text,
    email text,
    user_name text,
    time_minutes int,
    date timestamp,
    PRIMARY KEY ((country, dungeon_id), time_minutes, date))
    WITH CLUSTERING ORDER BY (time_minutes ASC, date DESC);




CREATE TABLE IF NOT EXISTS user_stats (
    email text,
    dungeon_id int,
    time_minutes int,
    date timestamp,
    PRIMARY KEY ((email, dungeon_id), date))
    WITH CLUSTERING ORDER BY (date DESC);

CREATE TABLE IF NOT EXISTS top_horde (
    country text,
    event_id int,
    email text,
    user_name text,
    monster_id int,
    kill_id int,
    PRIMARY KEY ((country, event_id), email, kill_id)
);

COPY hall_of_fame (country, dungeon_id, dungeon_name, email, user_name, time_minutes, date)  
FROM '/var/lib/cassandra/dungeon_completion.csv'  
WITH DELIMITER=',' 
AND QUOTE='"' 
AND ESCAPE='"' 
AND HEADER=false;

COPY user_stats (email, dungeon_id, time_minutes, date)
FROM '/var/lib/cassandra/player_stats.csv'
WITH DELIMITER=','
AND QUOTE='"'
AND ESCAPE='"'
AND HEADER=false;

COPY top_horde (country, event_id, email, user_name, monster_id, kill_id)
FROM '/var/lib/cassandra/kill_event.csv'
WITH DELIMITER=','
AND QUOTE='"'
AND ESCAPE='"'
AND HEADER=false;
