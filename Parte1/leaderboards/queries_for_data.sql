select webuser.country, dungeon.idD as dungeon_id, dungeon.name as dungeon_name, webuser.email, webuser.userName as user_name, completeddungeons.time as time_minutes, completeddungeons.date
from completeddungeons 
inner join dungeon on completeddungeons.idD = dungeon.idD
inner join webuser on webuser.email = completeddungeons.email;

select webuser.email, COUNT(*) as n_kills
from event 
inner join kills on event.idE = kills.idE
inner join webuser on webuser.email = kills.email
WHERE webuser.country = 'de_DE' AND event.idE = 0
GROUP BY webuser.country, event.idE, webuser.email
ORDER BY n_kills DESC;

select completeddungeons.email, completeddungeons.idD as dungeon_id, completeddungeons.time as time_minutes, completeddungeons.date
from completeddungeons;

select email, COUNT(*) from kills 

WHERE country='de_DE' AND idE=0 GROUP BY country, event_id, email;

select * from kills;