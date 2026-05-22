import dashboard as dashboard
import chromadb
import streamlit as st
import numpy
import pandas as pd 
# from sentence_transformers import SentenceTransformer


# user_input = {
#     "User Input": "",
# }

client = chromadb.PersistentClient(path="./chroma_db")
final_df_collection = client.get_or_create_collection(name="clickup_final_df_collection")


final_data_frame_from_dashboard = dashboard.aggregrate_task_data(dashboard.fetching_tasks(dashboard.user_input()))
final_data_frame_from_dashboard = final_data_frame_from_dashboard[0]
sentence_to_be_chunked = final_data_frame_from_dashboard.apply(lambda x: f"{x['team_member']} , {x['team_member_id']} , {x['task_name']}, {x['task_id']}, {x['entry_date']}, {x['billable_hours']}, {x['non_billable']}, {x['actual_hours']}, {x['actual_hours']}, {x['team_name']}, {x['time_estimate']}, {x['task_start_date']}, {x['task_due_date']} . ",  axis=1 ).to_list()
ids_as_strings = final_data_frame_from_dashboard.index.astype(str).tolist()

# ids_as_strings = ", ".join(ids_as_strings)

# final_df_collection.add(
#     ids= ids_as_strings,
#     documents= sentence_to_be_chunked,
#     metadatas= final_data_frame_from_dashboard.apply(lambda x: x.to_list()) 

# )
