from cassandra.cluster import Cluster
import json


def sortFn(dict):
  return dict['n_killed']


def topk_players(country, event_id, k):
    cluster = Cluster(['localhost'], port = 9042)
    session = cluster.connect()
    session.set_keyspace("dungeons")
    query =f'''SELECT email, user_name, COUNT(*) as n_killed from top_horde WHERE country='{country}' AND event_id={event_id} GROUP BY country, event_id, email;'''
    raw = [{'email': row.email, 'user_name': row.user_name, 'n_killed': row.n_killed} for row in session.execute(query)]
    sorted_data = sorted(raw, key=lambda x: x['n_killed'], reverse=True)
    top_k = json.dumps(sorted_data[:k], indent=4)
    return top_k


def leaderboard_by_country(country):
    cluster = Cluster(['localhost'], port = 9042)
    session = cluster.connect()
    session.set_keyspace("dungeons")
    final = []
    for i in range(20):
        to_insert = {}
        
        query = f"SELECT dungeon_name, email, user_name, time_minutes, date from hall_of_fame WHERE country='{country}' AND dungeon_id={i} LIMIT 5;"
        aux = session.execute(query)
        dungeon_id = i
        res = [{'dungeon_name':row.dungeon_name, 'email': row.email, 'user_name': row.user_name,
        'time_minutes': row.time_minutes, 'date': row.date} for row in aux]
        dungeon_name = res[0]['dungeon_name']
        to_insert['dungeon_id'] = i
        to_insert['dungeon_name'] = dungeon_name
        to_insert['Top_5'] = []
        for e in res:
            del e['dungeon_name']
            to_insert['Top_5'].append(e)
            
        final.append(to_insert)
    return json.dumps(final, indent=4)


def user_stats_per_dun(email, dungeon_id):
    cluster = Cluster(['localhost'], port = 9042)
    session = cluster.connect()
    session.set_keyspace("dungeons")
    final = []
    query = f"select time_minutes, date from user_stats where email='{email}' AND dungeon_id={dungeon_id};"
    aux = session.execute(query)
    for row in aux:
        final.append({'time_minutes':row.time_minutes, 'date':row.date}) 
    return json.dumps(final, indent=4)
