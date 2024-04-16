import networkx as nx
from pyvis.network import Network
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import numpy as np
import os

def run_query(query, **kwargs):
    with GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j", "BDII2023")) as driver:
        with driver.session() as session:
                result = list(session.run(query, **kwargs))
                return result

def mapamundi():
    def get_data():
        query_areas = """ 
        MATCH (a:Area) RETURN id(a) as id, {label: a.name} as attributes
        """
        query_paths = """
        MATCH (a1:Area)-[i1:IS_CONNECTED]->(r1:Room)
        MATCH (a2:Area)<-[i2:IS_CONNECTED]-(r2:Room)
        WHERE i1.dungeon_name = i2.dungeon_name 
        CREATE (a1)-[r:PATH {dungeon_name: i1.dungeon_name}]->(a2)
        RETURN id(a1) as source ,id(a2) as target, {label: r.dungeon_name} as attributes
        """
        
        g = nx.MultiGraph()
        g.add_nodes_from([(r['id'], r['attributes']) for r in run_query(query_areas)])
        g.add_edges_from([(r['source'], r['target'], r['attributes']) for r in run_query(query_paths)], color='#B4A893', font={"size": 110, "align": "right", "strokeWidth": 70, "strokeColor": "white"})

        return g

    def visualize(g):
        # ------------------------------- Define group styles -------------------------------
        groups_styles = {
            
            "area1": {
                "shape": 'image',
                "image": "./app/static/1.png"},
                
            "area2": {
                "shape": 'image',
                "image": "./app/static/2.png"
            },
            "area3": {
                "shape": 'image',
                "image": "./app/static/3.png"
            },
            "area4": {
                "shape": 'image',
                "image": "./app/static/4.png"
            },
            "area5": {
                "shape": 'image',
                "image": "./app/static/5.png"
            },
            "area6": {
                "shape": 'image',
                "image": "./app/static/6.png"
            },
            "area7": {
                "shape": 'image',
                "image": "./app/static/7.png"
            },
            "area8": {
                "shape": 'image',
                "image": "./app/static/8.png"
            },
            "area9": {
                "shape": 'image',
                "image": "./app/static/9.png"
            },
            "area10": {
                "shape": 'image',
                "image": "./app/static/10.png"
            },
        
        }
        # ------------------------------- Join overlapping edges -------------------------------
        overlapping_edge_groups = []
        
        # Iterate through each edge in 'g'
        for u, v, key, data in g.edges(keys=True, data=True):
            # Check if there are other edges with the same source and target nodes
            overlapping_edges = [(u, v, k) for k in g[u][v] if k != key]
            if overlapping_edges:
                # Add the group of overlapping edges to the list
                overlapping_edge_groups.append([(u, v, key)] + overlapping_edges)
        
        # Iterate through each group of overlapping edges
        for group in overlapping_edge_groups:
            # Collect labels of overlapping edges in the group
            labels = [g[u][v][key].get('label', '') for u, v, key in group if g[u][v][key].get('label', '') != '']
        
            # Combine the collected labels into a single formatted label
            combined_label = '\n'.join(labels)
            combined_label += '\n'
            
            # Add extra newlines to the beginning if the edges have the same node as start and end
            if group[0][0] == group[0][1]:
                combined_label = '\t' + combined_label + '\n'
        
            # Assign the combined label to one of the edges in the group
            g[group[0][0]][group[0][1]][group[0][2]]['label'] = combined_label
        
            # Hide the labels of the other edges in the group
            for u, v, key in group[1:]:
                g[u][v][key]['label'] = ''
                
        # ------------------------------- Add images to nodes -------------------------------
        def add_groups(G):
            for n in G.nodes:
                G.nodes[n]["size"] = 500
                G.nodes[n]["shape"] = "image"
                G.nodes[n]["font"] = {
                
                "size": 110,           # Text size
                "color": "black",      # Text color
                "background": "white",# Background color behind the text
                "strokeWidth": 10,     # Stroke width around the text
                "strokeColor": "white", # Stroke color around the text
                "align": "left"     # Text alignment 
                }
                    
                if G.nodes[n]["label"] == 'Embarrassed Swamp of Fafnir' :
                    G.nodes[n]["group"] = "area4"
                    
                elif G.nodes[n]["label"] == 'Jolly Steppe of Emerald city' :
                    G.nodes[n]["group"] = "area1"

                elif G.nodes[n]["label"] == 'Uptight Shrubland of Avalon' :
                    G.nodes[n]["group"] = "area2"

                elif G.nodes[n]["label"] == 'Insane Jungle of Gondor' :
                    G.nodes[n]["group"] = "area3"

                elif G.nodes[n]["label"] == 'Empowered Steppe of Isengard' :
                    G.nodes[n]["group"] = "area5"

                elif G.nodes[n]["label"] == 'Terrible Moor of Babylon' :
                    G.nodes[n]["group"] = "area6"

                elif G.nodes[n]["label"] == 'Clumsy Tropical Rainforest of Bilbo' :
                    G.nodes[n]["group"] = "area7"

                elif G.nodes[n]["label"] == 'Terrible River of Gandalf' :
                    G.nodes[n]["group"] = "area8"

                elif G.nodes[n]["label"] == 'Panicky Desert of Fomalhaut' :
                    G.nodes[n]["group"] = "area9"

                elif G.nodes[n]["label"] == 'Old-Fashioned Mountain of Emerald city' :   
                    G.nodes[n]["group"] = "area10"

                else:
                    G.nodes[n]["size"] = 100
                    G.nodes[n]["shape"] = "dot" 
        
        
        add_groups(g)
        
        # ------------------------------- Custom layout -------------------------------
        pos = nx.kamada_kawai_layout(g)
        pos = nx.rescale_layout_dict(pos,15000)
        
        for node, coordinates in pos.items():
            x, y = coordinates
            g.nodes[node]['x'] = x
            g.nodes[node]['y'] = y
        
        net = Network(notebook=True,cdn_resources='remote', height='900px', width='100%',directed=True, neighborhood_highlight=True, bgcolor='#F3EDE4' )
        net.from_nx(g)
        net.toggle_physics(False)
        net.options.groups = groups_styles
        return net.show("mapamundi.html")

    g = get_data()
    visualize(g)

def map_dungeon(dungeonName):
    def get_data(dungeonName):
        # Get all monsters in room

        query_monsters = """
        MATCH p=(m:Monster)-[:CONTAINS]-(r:Room {room_id: $roomId})
        RETURN id(m) as id, {label: m.name + ' (level ' + toString(m.level) + ')'} as attributes
        """

        # Get all loot in room

        query_loot = """
        MATCH p=(l:Loot)-[:CONTAINS]-(r:Room {room_id: $roomId})
        RETURN id(l) as id, {label: l.name + ' (' + toString(l.gold)+ ' gold)'} as attributes
        """

        # Obtain rooms and conections
        query_rooms_areas = """
        MATCH (a1:Area)-[i:IS_CONNECTED]->(startRoom:Room)
        MATCH (a2:Area)<-[i2:IS_CONNECTED]-(endRoom:Room)
        WHERE i.dungeon_name=$dungeonName AND i2.dungeon_name = $dungeonName
        CALL apoc.path.subgraphAll(startRoom, {
            relationshipFilter: "IS_CONNECTED",
            labelFilter: "Room"
        }) YIELD nodes, relationships
        RETURN nodes, relationships, a1, a2, i, i2;
        """
        result = run_query(query_rooms_areas, dungeonName=dungeonName)
        response_data = result[0].data()

        #----------------------------- Extract rooms, areas and connections -----------------------------
        nodes_info = [(node["room_id"], {"label": node["room_name"]}) for node in response_data["nodes"]]
        edges_a = [(0, response_data['i'][2]["room_id"])]
        edges_a.append((1, response_data['i2'][0]["room_id"]))
        a_info = [(0, {"label": response_data["a1"]["name"]})]
        a_info.append((1, {"label": response_data["a2"]["name"]}))


        relationships_info = []
        for rel_tuple in response_data['relationships']:
            start_node = rel_tuple[0]["room_id"]
            end_node = rel_tuple[2]["room_id"]
            relationships_info.append((start_node, end_node))

        # create graph
        g = nx.Graph()

        g.add_nodes_from(nodes_info, node_type= "room") # rooms
        g.add_nodes_from(a_info, node_type= "area") # areas
        g.add_edges_from(relationships_info) # connections rooms
        g.add_edges_from(edges_a) # connections areas

        #----------------------------- Add monsters-----------------------------

        nodes_list = list(g.nodes(data=True))
        for room_id, room_data in nodes_list:
            if "label" in room_data:
                # Run the Cypher query to get monsters for the current room
                monsters_result = run_query(query_monsters, roomId=room_id)
                
                if monsters_result:
                    # Aggregate attributes of all monsters in the room
                    aggregated_monster_attributes = {}
                    for monster in monsters_result:
                        monster_id = monster["id"]
                        monster_attributes = monster["attributes"]
                        for key, value in monster_attributes.items():
                            # Concatenate values if the attribute already exists
                            if key in aggregated_monster_attributes:
                                aggregated_monster_attributes[key] += ", \n" + str(value)
                            else:
                                aggregated_monster_attributes[key] = value

                    # Create a single monster node for the room with concatenated labels
                    g.add_node(str(room_id) + '_monsters', node_type='monster', label = ' ')

                    # Set aggregated attributes as the title attribute of the room node
                    g.nodes[str(room_id) + '_monsters']['title'] = aggregated_monster_attributes['label']

                    # Add edge between room and monster node
                    g.add_edge(room_id, str(room_id) + '_monsters')

        #----------------------------- Add loot-----------------------------

        for room_id, room_data in nodes_list:
            if "label" in room_data:
                # Run the Cypher query to get monsters for the current room
                loot_result = run_query(query_loot, roomId=room_id)
                
                if loot_result:
                    # Aggregate attributes of all loot in the room
                    aggregated_loot_attributes = {}
                    for loot in loot_result:
                        loot_id = loot["id"]
                        loot_attributes = loot["attributes"]
                        for key, value in loot_attributes.items():
                            # Concatenate values if the attribute already exists
                            if key in aggregated_loot_attributes:
                                aggregated_loot_attributes[key] += ",\n " + str(value)
                            else:
                                aggregated_loot_attributes[key] = value

                    # Create a single loot node for the room with concatenated labels
                    g.add_node(str(room_id) + '_loot', node_type='loot', label = ' ')

                    # Set aggregated attributes as the title attribute of the room node
                    g.nodes[str(room_id) + '_loot']['title'] = aggregated_loot_attributes['label']

                    # Add edge between room and loot node
                    g.add_edge(room_id, str(room_id) + '_loot')
        
        return g

    def visualize(g):
        # ------------------------------- Define group styles -------------------------------
        groups_styles = {
            "loot": {
                "shape": 'image',
                "image": "./app/static/loot.png"
            },
            "monster": {
                "shape": 'image',
                "image": "./app/static/monster.png"
            },


        }
        # ------------------------------- Add images to nodes -------------------------------
        def add_groups(G):
            for n in G.nodes:
                G.nodes[n]["color"] = '#B4A893'
                G.nodes[n]["font"] = {
                
                "size": 110,           # Text size
                "color": "black",      # Text color
                "strokeWidth": 10,     # Stroke width around the text
                "align": "left"     # Text alignment 
                }
                    
                if G.nodes[n]["node_type"] == 'loot' :
                    G.nodes[n]["size"] = 50
                    G.nodes[n]["shape"] = "image"
                    G.nodes[n]["group"] = "loot"

                elif G.nodes[n]["node_type"] == 'monster' :
                    G.nodes[n]["size"] = 100
                    G.nodes[n]["shape"] = "image"
                    G.nodes[n]["group"] = "monster"

                elif G.nodes[n]["node_type"] == 'area' :
                    G.nodes[n]["size"] = 20
                    G.nodes[n]["shape"] = "dot"
                    G.nodes[n]["color"] = "red"
                    
                else:
                    G.nodes[n]["size"] = 100
                    G.nodes[n]["shape"] = "dot" 

        add_groups(g)
        # ------------------------------- Custom layout -------------------------------
        pos = nx.fruchterman_reingold_layout(g)
        pos = nx.rescale_layout_dict(pos,15000)

        for node, coordinates in pos.items():
            x, y = coordinates
            g.nodes[node]['x'] = x
            g.nodes[node]['y'] = y

        net = Network(notebook=True,cdn_resources='remote',height='900px', width='100%',directed=False, neighborhood_highlight=True, bgcolor='#F3EDE4' )
        net.from_nx(g)
        net.toggle_physics(False)
        net.options.groups = groups_styles
        return net.show("mini_map_dungeon.html")
        

    g = get_data(dungeonName)
    visualize(g) 
    
def list_dungeons():
    def get_data():
        query_areas = """ 
        MATCH (a:Area) RETURN id(a) as id, {label: a.name} as attributes
        """
        query_paths = """
        MATCH (a1:Area)-[i1:IS_CONNECTED]->(r1:Room)
        MATCH (a2:Area)<-[i2:IS_CONNECTED]-(r2:Room)
        WHERE i1.dungeon_name = i2.dungeon_name 
        CREATE (a1)-[r:PATH {dungeon_name: i1.dungeon_name}]->(a2)
        RETURN id(r) as source ,id(a1) as target_1, id(a2) as target_2, {label: r.dungeon_name} as dungeon_attributes
        """
        
        g = nx.Graph()
        results_areas = run_query(query_areas)
        results_paths = run_query(query_paths)
        
        g.add_nodes_from([(r['id'], r['attributes']) for r in results_areas], bipartite=0)
        g.add_nodes_from([(r['source'], r['dungeon_attributes']) for r in results_paths], bipartite=1)
        g.add_edges_from([(r['source'], r['target_1']) for r in results_paths], color='black')
        g.add_edges_from([(r['source'], r['target_2']) for r in results_paths], color='black')
        
        return g

    def visualize(g):
        # ---------------------------- Add corresponding icons ----------------------------
        groups_styles = {
            
            "area1": {
                "shape": 'image',
                "image": "./app/static/1.png"},
                
            "area2": {
                "shape": 'image',
                "image": "./app/static/2.png"
            },
            "area3": {
                "shape": 'image',
                "image": "./app/static/3.png"
            },
            "area4": {
                "shape": 'image',
                "image": "./app/static/4.png"
            },
            "area5": {
                "shape": 'image',
                "image": "./app/static/5.png"
            },
            "area6": {
                "shape": 'image',
                "image": "./app/static/6.png"
            },
            "area7": {
                "shape": 'image',
                "image": "./app/static/7.png"
            },
            "area8": {
                "shape": 'image',
                "image": "./app/static/8.png"
            },
            "area9": {
                "shape": 'image',
                "image": "./app/static/9.png"
            },
            "area10": {
                "shape": 'image',
                "image": "./app/static/10.png"
            },
        
        }
        
        def add_groups(G): 
            for n in G.nodes:
                if G.nodes[n]["bipartite"] == 1:
                    G.nodes[n]["label"] += ' ' * 80
                    G.nodes[n]["size"] = 1
                    G.nodes[n]["shape"] = "dot" 
                    G.nodes[n]["font"] = {
                        
                        "size": 1500,           # Text size
                        "color": "black",      # Text color
                        "align": "right",
                        "strokeWidth": 700, 
                        "strokeColor": "white"
                    }
                    
                else:
                    G.nodes[n]["size"] = 8000
                    G.nodes[n]["shape"] = "image"

                    if G.nodes[n]["label"] == 'Embarrassed Swamp of Fafnir' :
                        G.nodes[n]["group"] = "area4"
                        
                    elif G.nodes[n]["label"] == 'Jolly Steppe of Emerald city' :
                        G.nodes[n]["group"] = "area1"

                    elif G.nodes[n]["label"] == 'Uptight Shrubland of Avalon' :
                        G.nodes[n]["group"] = "area2"

                    elif G.nodes[n]["label"] == 'Insane Jungle of Gondor' :
                        G.nodes[n]["group"] = "area3"

                    elif G.nodes[n]["label"] == 'Empowered Steppe of Isengard' :
                        G.nodes[n]["group"] = "area5"

                    elif G.nodes[n]["label"] == 'Terrible Moor of Babylon' :
                        G.nodes[n]["group"] = "area6"

                    elif G.nodes[n]["label"] == 'Clumsy Tropical Rainforest of Bilbo' :
                        G.nodes[n]["group"] = "area7"

                    elif G.nodes[n]["label"] == 'Terrible River of Gandalf' :
                        G.nodes[n]["group"] = "area8"

                    elif G.nodes[n]["label"] == 'Panicky Desert of Fomalhaut' :
                        G.nodes[n]["group"] = "area9"
                    else:
                        G.nodes[n]["group"] = "area10"    
                    
        add_groups(g)
        
        # ---------------------------- Custom layout ----------------------------
        top = nx.bipartite.sets(g)[1]
        pos = nx.bipartite_layout(
            g,
            top # group of nodes on the left
        )
        
        pos = nx.rescale_layout_dict(pos,150000)
        
        for node, coordinates in pos.items():
            x, y = coordinates
            g.nodes[node]['x'] = x
            g.nodes[node]['y'] = y
        
        # Collect y-coordinates for nodes
        bipartite_nodes_0 = [data["y"] for node, data in g.nodes(data=True) if data.get("bipartite") == 0]
        bipartite_nodes_1 = [data["y"] for node, data in g.nodes(data=True) if data.get("bipartite") == 1]
        
        # Calculate min and max y-coordinates
        min_y_0, max_y_0 = min(bipartite_nodes_0), max(bipartite_nodes_0)
        num_bipartite_nodes_0 = len(bipartite_nodes_0)
        
        min_y_1, max_y_1 = min(bipartite_nodes_1), max(bipartite_nodes_1)
        num_bipartite_nodes_1 = len(bipartite_nodes_1)
        
        # Generate new y-coordinates using linspace
        space_0 = 20000
        space_1 = 50000
        new_y_coordinates_0 = np.linspace(min_y_0-space_0, max_y_0+space_0, num_bipartite_nodes_0)
        new_y_coordinates_1 = np.linspace(min_y_1-space_1, max_y_1+space_1, num_bipartite_nodes_1)
        
        # Assign new y-coordinates
        bipartite_index_0 = 0
        bipartite_index_1= 0
        for i, (node, data) in enumerate(g.nodes(data=True)):
            if data.get("bipartite") == 0:
                g.nodes[node]["y"] = new_y_coordinates_0[bipartite_index_0]
                bipartite_index_0 += 1
            if data.get("bipartite") == 1:
                g.nodes[node]["y"] = new_y_coordinates_1[bipartite_index_1]
                bipartite_index_1 += 1
            
        #  ---------------------------- Show graph  ----------------------------
        net = Network(notebook=True,cdn_resources='remote',height='900px', width='100%',neighborhood_highlight=True, bgcolor='#F3EDE4')
        net.from_nx(g)
        net.toggle_physics(False)
        net.options.groups = groups_styles
        
        return net.show("list_dungeons.html")

    g = get_data()
    visualize(g)


