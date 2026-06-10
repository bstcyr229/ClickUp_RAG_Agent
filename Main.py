import sys
print(sys.executable)
print("It worked")
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

CHROMA_API_KEY = os.getenv("GEMINI_API_KEY")
llm_api_key = CHROMA_API_KEY


client = chromadb.PersistentClient(path="./chroma_db")
gemini_ef = GoogleGeminiEmbeddingFunction(api_key_env_var = llm_api_key)

genai_client = genai.Client(api_key=llm_api_key)

final_df_collection = client.get_or_create_collection(name="final_df_collection", embedding_function=gemini_ef
    )
user_input_collection = client.get_or_create_collection(name='user_input_collection', embedding_function=gemini_ef)

user_input = input("Please enter your question: ")




final_data_frame_from_dashboard = dashboard.aggregrate_task_data(dashboard.fetching_tasks(dashboard.user_input()))
final_data_frame_from_dashboard = final_data_frame_from_dashboard[0]
sentence_to_be_chunked = final_data_frame_from_dashboard.apply(lambda x: f"{x['team_member']} , {x['team_member_id']} , {x['task_name']}, {x['task_id']}, {x['entry_date']}, {x['billable_hours']}, {x['non_billable']}, {x['actual_hours']}, {x['actual_hours']}, {x['team_name']}, {x['time_estimate']}, {x['task_start_date']}, {x['task_due_date']} . ",  axis=1 ).to_list()
metadatas = final_data_frame_from_dashboard.to_dict(orient='records')
ids_as_strings = final_data_frame_from_dashboard.index.astype(str).tolist()


final_df_collection.add(
    ids= ids_as_strings,
    documents= sentence_to_be_chunked,
    metadatas=metadatas

)
results = final_df_collection.query(
    query_texts=user_input,
    n_results=1,

)
