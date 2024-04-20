from cassandra.cluster import Cluster
import json
import pandas as pd


def sortFn(dict):
  return dict['n_killed']


def topk_players(country, event_id, k):
    cluster = Cluster(['localhost'], port = 9042)
    session = cluster.connect()
    session.set_keyspace("dungeons")
    query =f'''SELECT email, user_name, COUNT(*) as n_killed from top_horde WHERE country='{country}' AND event_id={event_id} GROUP BY country, event_id, email;'''
    raw = [{'email': row.email, 'user_name': row.user_name, 'n_killed': row.n_killed} for row in session.execute(query)]
    sorted_data = sorted(raw, key=lambda x: x['n_killed'], reverse=True)
    df = pd.DataFrame(sorted_data[:k])
    positions = [str(i)+'º' for i in range(1, k+1)]
    df.insert(0, 'Position', positions)
    df.set_index('Position', inplace=True)
    return df


def leaderboard_by_country(country):
    cluster = Cluster(['localhost'], port = 9042)
    session = cluster.connect()
    session.set_keyspace("dungeons")
    final = []
    for i in range(20):
        try:
            to_insert = {}
            
            query = f"SELECT dungeon_name, email, user_name, time_minutes, date from hall_of_fame WHERE country='{country}' AND dungeon_id={i} LIMIT 5;"
            aux = session.execute(query)
            dungeon_id = i
            res = [{'dungeon_name':row.dungeon_name, 'email': row.email, 'user_name': row.user_name,
            'time_minutes': row.time_minutes, 'date': str(row.date)} for row in aux]
            dungeon_name = res[0]['dungeon_name']
            to_insert['dungeon_id'] = i
            to_insert['dungeon_name'] = dungeon_name
            to_insert['Top_5'] = []
            for e in res:
                del e['dungeon_name']
                to_insert['Top_5'].append(e)
                
            final.append(to_insert)
        except:
            pass
    headers = ['dungeon_id', 'dungeon_name', 'email', 'user_name', 'time_minutes', 'date']
    array_for_df = []
    for e in final:
        for i in e['Top_5']:
            array_for_df.append([e['dungeon_id'], e['dungeon_name'], i['email'], i['user_name'], i['time_minutes'], i['date']])
    df = pd.DataFrame(array_for_df, columns=headers)
    df.set_index(['dungeon_id', 'dungeon_name'], inplace=True)
    return df


def user_stats_per_dun(email, dungeon_id):
    cluster = Cluster(['localhost'], port = 9042)
    session = cluster.connect()
    session.set_keyspace("dungeons")
    final = []
    query = f"select time_minutes, date from user_stats where email='{email}' AND dungeon_id={dungeon_id};"
    aux = session.execute(query)
    for row in aux:
        final.append({'time_minutes':row.time_minutes, 'date': str(row.date)})
    df = pd.DataFrame(final) 
    return df
