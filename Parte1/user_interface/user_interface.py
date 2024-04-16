import streamlit as st
import streamlit.components.v1 as components
import cassandra_queries
import queries
import visualization

# ----------------------------------------- Page configuration -----------------------------------------
st.set_page_config(layout="wide", page_title="The Jötun's Lair")

# ----------------------------------------- Main page content -----------------------------------------
def main():
    st.title("The Jötun's Lair")
    st.write("Welcome to The Jötun's Lair, a place of mystery and adventure.")
    
    # Sidebar menu
    menu_choice = st.sidebar.radio("Navigation", ["Home", "See world map", "See dungeon connection list", "Want to explore a dungeon?", "Get dungeon specific info" ,"Cassandra, let's see the community's stats"])

    # Display different pages based on menu selection
    if menu_choice == "Home":
        show_home_page()
    elif menu_choice == "Cassandra, let's see the community's stats":
        show_cassandra_queries_page()
    elif menu_choice == "Get dungeon specific info":
        show_queries_page()
    elif menu_choice == "See world map":
        show_mapamundi_page()
    elif menu_choice == "See dungeon connection list":
        show_list_dungeons_page()
    elif menu_choice == "Want to explore a dungeon?":
        show_mini_map_dungeons_page()

# -------------------------------------------- Functions ---------------------------------------------------
def show_home_page():
    st.write("This is the home page. Feel free to explore!")

def show_cassandra_queries_page():
    st.write("---------------------------------------------------")
    st.write("Let's see some stats about the community!")

    # Get user input for query selection
    query_choice = st.selectbox("Select a query", ('top k players', 'country leaderboard', 'user stats per dungeon'), placeholder="Select a query")

    # Perform queries based on user selection   
    if query_choice == 'top k players':
        st.write("Top k players")
        countries = ['ja_JP', 'en_US', 'es_ES', 'fr_FR', 'it_IT', 'pt_BR', 'ko_KR']
        country = st.selectbox("Select a country", countries, placeholder="Select a country")
        event_id = st.number_input("Enter event ID", min_value=0, step=1, placeholder="Enter event ID")
        k = st.number_input("Enter k", min_value=0, step=1, max_value=100, placeholder="Enter k")
        st.write(cassandra_queries.topk_players(country, event_id, k))
    
    elif query_choice == 'country leaderboard':
        st.write("Country leaderboard")
        countries = ['ja_JP', 'en_US', 'es_ES', 'fr_FR', 'it_IT', 'pt_BR', 'ko_KR']
        country = st.selectbox("Select a country", countries, placeholder="Select a country")
        st.write(cassandra_queries.leaderboard_by_country(country))

    elif query_choice == 'user stats per dungeon':
        st.write("User stats per dungeon")
        emails = ['aabe@example.net', 'aaoki@example.com', 'aaron03@example.com', 'aarongreen@example.com', 'aaubry@example.net', 'abag@example.com', 'abarbosa@example.org', 'abaresi@example.com']
        email = st.selectbox("Select an email", emails, placeholder="Select an email")
        dungeon_id = st.number_input("Enter dungeon ID", min_value=0, step=1, placeholder="Enter dungeon ID")
        st.write(cassandra_queries.user_stats_per_dun(email, dungeon_id))

def show_queries_page():
    st.write("----------------------Let's explore the dungeons!----------------------")
    # get the list of dungeons
    with open("dungeons.txt", "r") as file:
        dungeons = file.read().splitlines()
    selected_dungeon = st.selectbox("Select a dungeon", dungeons, placeholder="Select a dungeon")
    if selected_dungeon is not None:
        st.write("Dungeon selected: ", selected_dungeon)
        st.write("Here are some stats about the dungeon:")
        st.write("Total gold: ", queries.get_dungeon_gold(selected_dungeon))
        st.write("Mean number of relationships in the dungeon: ", queries.get_mean_relationships_in_dungeon(selected_dungeon))
        st.write("Mean monster level: ", queries.get_mean_monster_lvl(selected_dungeon))
        st.write("Max monster level: ", queries.get_max_monster_lvl(selected_dungeon))
        st.write("Total monster exp per room in dungeon: ", queries.get_exp_per_room(selected_dungeon))
        st.write("Room with max exp in dungeon: ", queries.most_exp_room(selected_dungeon))

    # Get user input for room_id
    st.write("Enter a room ID to get monster recommendations for that room: e.g 1040")
    room_id = st.number_input("Enter room ID", min_value=0, step=1, max_value=11580,placeholder="Enter room ID")

    # Perform queries based on room_id
    if room_id is not None:
        st.write("Room ID selected:", room_id)
        st.write("Here are some monster recomendations basen on chosen room:")
        st.write(queries.get_monster_recomendations(room_id))
        st.write(queries.get_top5_monster_recomendations(room_id))

def show_mapamundi_page():
    st.write("----------------------------------------------------------------------------------------------------")
    st.write("Discover the world of The Jötun's Lair! Check out the main areas and the dungeons connecting them.")
    st.write("Zoom in and out to explore the map.")
    visualization.mapamundi()
    p = open("mapamundi.html")
    components.html(p.read(),width=900, height=900, scrolling=False, )

def show_list_dungeons_page():
    st.write("----------------------------------------------------------------------")
    st.write("Explore dungeon connections! Click on whichever area node and see the neighbor dungeons.")
    visualization.list_dungeons()
    p = open("list_dungeons.html")
    components.html(p.read(),width=900, height=900, scrolling=False)

def show_mini_map_dungeons_page():
    st.write("----------------------------------------------------------------------")
    st.write("Explore the dungeons! Once a map shows, hover over the monster and loot icons to see their details.")
    # get the list of dungeons
    with open("dungeons.txt", "r") as file:
        dungeons = file.read().splitlines()
    selected_dungeon = st.selectbox("Select a dungeon", dungeons, placeholder="Select a dungeon")
    if selected_dungeon is not None:
        visualization.map_dungeon(selected_dungeon)
        p = open("mini_map_dungeon.html")
        components.html(p.read(),width=900, height=900, scrolling=False)

if __name__ == "__main__":
    #  Add the dungeon name as attribute to the room, first thing done as the app starts.
    dungeon_ref_room = """
    MATCH (:Area)-[i:IS_CONNECTED]->(:Room)
    WITH DISTINCT i.dungeon_name AS dungeonName

    CALL apoc.cypher.doIt("
        MATCH (a1:Area)-[i:IS_CONNECTED]->(startRoom:Room)
        WHERE i.dungeon_name = $dungeonName
        CALL apoc.path.subgraphNodes(startRoom, {
            relationshipFilter: 'IS_CONNECTED',
            labelFilter: 'Room'
        }) YIELD node
        SET node.dungeon_name = $dungeonName
        RETURN count(node) AS updatedRooms
    ", {dungeonName: dungeonName}) YIELD value

    RETURN dungeonName;
    """
    _ = visualization.run_query(dungeon_ref_room)
    main()