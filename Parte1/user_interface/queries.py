from neo4j import GraphDatabase
from graphdatascience import GraphDataScience
import pandas as pd

def get_dungeon_gold(dungeon_name):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri,  auth=("neo4j", "BDII2023"))
    with driver.session() as session:
        query = '''
        MATCH (:Area)-[i:IS_CONNECTED]->(startRoom:Room)
        MATCH (:Area)<-[i2:IS_CONNECTED]-(:Room)
        WHERE i.dungeon_name = $dungeon_name AND i2.dungeon_name = $dungeon_name
        CALL apoc.path.subgraphNodes(startRoom, {
            relationshipFilter: "IS_CONNECTED",
            labelFilter: "Room"
        }) YIELD node
        MATCH (node)-[:CONTAINS]->(l:Loot)
        RETURN sum(l.gold) as gold

        '''
        result = session.run(query, dungeon_name=dungeon_name)
        data = pd.DataFrame([r.values() for r in result], columns=result.keys())
        
    return data

def get_mean_monster_lvl(dungeon_name):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri,  auth=("neo4j", "BDII2023"))
    with driver.session() as session:
        query = '''
        MATCH (:Area)-[i:IS_CONNECTED]->(startRoom:Room)
        MATCH (:Area)<-[i2:IS_CONNECTED]-(:Room)
        WHERE i.dungeon_name = $dungeon_name AND i2.dungeon_name = $dungeon_name
        CALL apoc.path.subgraphNodes(startRoom, {
            relationshipFilter: "IS_CONNECTED",
            labelFilter: "Room"
        }) YIELD node
        MATCH (node)-[:CONTAINS]->(m:Monster)
        RETURN avg(m.level) as average_level

        '''
        result = session.run(query, dungeon_name=dungeon_name)
        data = pd.DataFrame([r.values() for r in result], columns=result.keys())
        
    return data

def get_mean_relationships_in_dungeon(dungeon_name):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri,  auth=("neo4j", "BDII2023"))
    with driver.session() as session:
        query = '''
        MATCH (:Area)-[i:IS_CONNECTED]->(startRoom:Room)
        MATCH (:Area)<-[i2:IS_CONNECTED]-(:Room)
        WHERE i.dungeon_name = $dungeon_name AND i2.dungeon_name = $dungeon_name
        CALL apoc.path.subgraphNodes(startRoom, {
            relationshipFilter: "IS_CONNECTED",
            labelFilter: "Room"
        }) YIELD node
        MATCH (node)-[r:IS_CONNECTED]-(:Room)
        RETURN node.room_id as id , count(r) as number_of_relationships
        '''
        result = session.run(query, dungeon_name=dungeon_name)
        data = pd.DataFrame([r.values() for r in result], columns=result.keys())
        avg = data['number_of_relationships'].mean()
        # make a groupby to count the number of relationships and get the mean

        
    return avg

def get_max_monster_lvl(dungeon_name):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri,  auth=("neo4j", "BDII2023"))
    with driver.session() as session:
        query = '''
        MATCH (:Area)-[i:IS_CONNECTED]->(startRoom:Room)
        MATCH (:Area)<-[i2:IS_CONNECTED]-(:Room)
        WHERE i.dungeon_name = $dungeon_name AND i2.dungeon_name = $dungeon_name
        CALL apoc.path.subgraphNodes(startRoom, {
            relationshipFilter: "IS_CONNECTED",
            labelFilter: "Room"
        }) YIELD node
        MATCH (node)-[:CONTAINS]->(m:Monster)
        RETURN m.name as monster_name, max(m.level) as max_level, node.room_id as room_id, node.room_name as room_name

        '''
        result = session.run(query, dungeon_name=dungeon_name)
        data = pd.DataFrame([r.values() for r in result], columns=result.keys())
        max_level_row = data.loc[data['max_level'].idxmax()]
        
    return max_level_row

def get_exp_per_room(dungeon_name):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri,  auth=("neo4j", "BDII2023"))
    with driver.session() as session:
        query = '''
        MATCH (:Area)-[i:IS_CONNECTED]->(startRoom:Room)
        MATCH (:Area)<-[i2:IS_CONNECTED]-(:Room)
        WHERE i.dungeon_name = $dungeon_name AND i2.dungeon_name = $dungeon_name
        CALL apoc.path.subgraphNodes(startRoom, {
            relationshipFilter: "IS_CONNECTED",
            labelFilter: "Room"
        }) YIELD node
        MATCH (node)-[:CONTAINS]->(m:Monster)
        RETURN node.room_id as room_id, node.room_name as room_name, sum(m.exp) as total_exp

        '''
        result = session.run(query, dungeon_name=dungeon_name)
        data = pd.DataFrame([r.values() for r in result], columns=result.keys())
        # sort by total_exp
        data = data.sort_values(by='total_exp', ascending=False)
        data.reset_index(drop=True, inplace=True)
        
    return data

def most_exp_room(dungeon_name):
    room = get_exp_per_room(dungeon_name=dungeon_name).iloc[0][['room_id', 'room_name']]
    return room

def get_top5_monster_recomendations(room_id):
    gds = GraphDataScience("neo4j://localhost:7687", auth=("neo4j", "BDII2023"))
    node_query = """
        MATCH (b1:Monster)<-[:CONTAINS]-(u:Room)-[:CONTAINS]->(b2:Monster) 
        WITH b1, b2, count(distinct u) as liked 
        RETURN DISTINCT id(b1) as id
    """
    edge_query = """
        MATCH (b1:Monster)<-[:CONTAINS]-(u:Room)-[:CONTAINS]->(b2:Monster) 
        WITH b1, b2, count(distinct u) as liked 
        RETURN id(b1) as source, id(b2) as target, (liked) as weight
    """

    with gds.graph.project.cypher("coliked_beers_temp", node_query, edge_query) as g_temp:
        q_source = """
            MATCH (:Room {room_id: $id})-[:CONTAINS]->(b:Monster) RETURN collect(id(b)) as sources
        """
        sources = gds.run_cypher(q_source,params={"id": str(room_id)}).sources[0]
        result = gds.pageRank.stream(g_temp, sourceNodes=sources, relationshipWeightProperty="weight")
        result = result.query("score > 0")

    nodes = result.nodeId.to_list()
    q = """
    MATCH (:Room {room_id: $id})-[:CONTAINS]->(b:Monster) WITH collect(b) as sources
    MATCH (b:Monster) WHERE id(b) IN $nodes AND not(b in sources)
    RETURN id(b) AS nodeId, b.name AS monster
    """
    df = gds.run_cypher(q, params={"id":str(room_id),"nodes": nodes})

    res = result.join(df.set_index("nodeId"), on="nodeId").dropna().sort_values("score", ascending=False).head(10)
    res.reset_index(drop=True, inplace=True)
    return res

def get_monster_recomendations(room_id):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri,  auth=("neo4j", "BDII2023"))
    with driver.session() as session:
        query = '''
        MATCH (r:Room {room_id: $room_id})-[:CONTAINS]->(m:Monster)<-[:CONTAINS]-(r2:Room)-[:CONTAINS]->(m2:Monster)
        RETURN DISTINCT m2.name as monster_name, m2.level as monster_level, m2.exp as monster_exp
        '''
        result = session.run(query, room_id=room_id)
        data = pd.DataFrame([r.values() for r in result], columns=result.keys())
        
    return data