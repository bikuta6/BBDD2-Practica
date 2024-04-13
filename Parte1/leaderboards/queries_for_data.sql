select webuser.country, dungeon.idD as dungeon_id, dungeon.name as dungeon_name, webuser.email, webuser.userName as user_name, completeddungeons.time as time_minutes, completeddungeons.date
from completeddungeons 
inner join dungeon on completeddungeons.idD = dungeon.idD
inner join webuser on webuser.email = completeddungeons.email
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dungeon_completion.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';


select completeddungeons.email, completeddungeons.idD as dungeon_id, completeddungeons.time as time_minutes, completeddungeons.date
from completeddungeons
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/player_stats.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

select webuser.country as country, event.idE as event_id, webuser.email as email, webuser.userName as user_name, kills.idM as monster_id, kills.idK as kill_id
from event
inner join kills on event.idE = kills.idE
inner join webuser on webuser.email = kills.email
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/kill_event.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
