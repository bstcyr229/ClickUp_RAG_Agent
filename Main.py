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
final_data_frame_from_dashboard.apply(lambda x: f"{x['team_member']} , {x['team_member_id']} , {x['task_name']}, {x['task_id']}, {x['entry_date']}, {x['billable_hours']}, {x['non_billable']}, {x['actual_hours']}, x{['actual_hours']}, {x['team_name']}, {x['time_estimate']}, {x['task_start_date']}, x{['task_due_date']} ",  axis=1 )
