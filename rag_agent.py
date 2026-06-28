import dashboard as dashboard
import chromadb
import streamlit as st
import numpy
import pandas as pd 
import os
import dotenv
from google import genai

from chromadb.utils.embedding_functions import GoogleGeminiEmbeddingFunction
from dotenv import load_dotenv 



load_dotenv()
GOOGLE_GENAI_USE_VERTEXAI="false"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@st.cache_resource
def get_client():
    client = chromadb.PersistentClient(path="./chroma_db")
    gemini_ef = GoogleGeminiEmbeddingFunction(api_key_env_var = "GEMINI_API_KEY")
    _get_client_variables = client, gemini_ef
    
    return _get_client_variables

@st.cache_resource 
def load_data(_get_client_variables):
    client = _get_client_variables[0]    
    gemini_ef = _get_client_variables[1]
    final_df_collection = client.get_or_create_collection(name="final_df_collection", embedding_function=gemini_ef
    )
    user_input_collection = client.get_or_create_collection(name='user_input_collection', embedding_function=gemini_ef)
    final_data_frame_from_dashboard = dashboard.final_df
    sentence_to_be_chunked = final_data_frame_from_dashboard.apply(lambda x: f"{x['team_member']} , {x['team_member_id']} , {x['task_name']}, {x['task_id']}, {x['entry_date']}, {x['billable_hours']}, {x['non_billable']}, {x['actual_hours']}, {x['team_name']}, {x['time_estimate']}, {x['task_start_date']}, {x['task_due_date']} . ",  axis=1 ).to_list()
    metadatas = final_data_frame_from_dashboard.to_dict(orient='records')
    ids_as_strings = final_data_frame_from_dashboard.index.astype(str).tolist()


    final_df_collection.add(
        ids= ids_as_strings,
        documents= sentence_to_be_chunked,
        metadatas=metadatas

    )
    return final_df_collection
def get_input():
    st.write("Please enter your question: ")
    user_input = st.text_input(label="User Input", key="user_input")
    return user_input
def display_results(user_input, final_df_collection):
    if not user_input:
        st.write("Please submit a question") 
    
    else:
        results = final_df_collection.query(
            query_texts=user_input,
            n_results=10,)
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = "Never guessing, respond to the user's query by scanning the documents and metadatas to answer the user query if you cannot find the information state I don't know"
        flat_results = str(results)
        results_prompt_user_input = [prompt, flat_results, user_input]  
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=results_prompt_user_input
        )
        
        return response
def main():
    display_results(get_input(), load_data(get_client()))

if __name__ == "__main__":
    main()