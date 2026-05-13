import dashboard as dashboard
#import chromadb
# import uuid
# from uuid import uuid4
# from sentence_transformers import SentenceTransformer


# user_input = {
#     "User Input": "",
# }

# client = chromadb.PersistentClient(path="./chroma_db")


final_data_frame_from_dashboard = dashboard.aggregrate_task_data(dashboard.fetching_tasks(dashboard.user_input()))
final_data_frame_from_dashboard = final_data_frame_from_dashboard[0]
final_data_frame_from_dashboard.apply(lambda x: f"{x['team_member']} , {x['team_member_id']} , {x['task_name']}", axis=1 )