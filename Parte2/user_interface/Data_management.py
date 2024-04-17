from ClipEmbeddingsGenerator import ClipEmbeddingsGenerator, draw_images 
import streamlit as st
from pymilvus import MilvusClient


# Web page configuration ---------------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Avatar Generator")

# Define your code here
def avatar_from_text(input_text, model_for_query, client):
    # Example: Print the input text
    print("You have written:", input_text)

    embedded_vector = model_for_query.embedd_texts([input_text])

    limit = 5

    res = client.search(
        collection_name="avatars", # Replace with the actual name of your collection
        # Replace with your query vector
        data=embedded_vector,
        limit=limit, # Max. number of search results to return
        search_params={"metric_type": "COSINE", "params": {}}, # Search parameters
        output_fields=["image_path"] 
    )

    draw_images([res[0][i]['entity']['image_path'] for i in range(limit)], [f'avatar {i+1}' for i in range(limit)])


# Streamlit app
def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Initialize Milvus client
    client = MilvusClient(host="localhost", port=19530, database='dungeons')

    model_for_query = ClipEmbeddingsGenerator()

    st.write("## Enter a descprition to find the most similar images")
    # Get user input
    input_text = st.text_input("Enter text")

    # Execute code when button is clicked
    if st.button("Execute", key="text"):
        avatar_from_text(input_text, model_for_query, client)

    st.write("## Or upload an image to find the most similar images")
    # Get user input
    uploaded_file = st.file_uploader("Choose a file")

    # Execute code when button is clicked

    if st.button("Execute", key="image"):
        if uploaded_file is not None:
            # Save the uploaded file
            with open("uploaded_image.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())

            embedded_vector = model_for_query.embedd_images(["uploaded_image.jpg"])

            limit = 5

            res = client.search(
                collection_name="avatars", # Replace with the actual name of your collection
                # Replace with your query vector
                data=embedded_vector,
                limit=limit, # Max. number of search results to return
                search_params={"metric_type": "COSINE", "params": {}}, # Search parameters
                output_fields=["image_path"] 
            )

            draw_images([res[0][i]['entity']['image_path'] for i in range(limit)], [f'avatar {i+1}' for i in range(limit)])



# Run the app
if __name__ == "__main__":
    main()