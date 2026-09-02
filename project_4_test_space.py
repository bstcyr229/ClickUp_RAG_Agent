import datetime
import time 
import os
from datetime import datetime as dt

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# GOOGLE_GENAI_USE_VERTEXAI="false"
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# from chromadb.utils.embedding_functions import GoogleGeminiEmbeddingFunction

#COMMENTED OUT TO USE A PRE-DEFINED DATE FOR TESTING start_date = st.datetime_input(label="Please enter start date", format="YYYY/MM/DD", value=dt(2026, 4, 1, tzinfo=timezone.utc), key="start_date")
#end_date =  st.datetime_input(label="Please enter end date", format="YYYY/MM/DD", value=dt(2026, 5, 1, tzinfo=timezone.utc), key="end_date" )

start_date = dt(2026, 4, 1, tzinfo=datetime.UTC)
end_date =  dt(2026, 5, 1, tzinfo=datetime.UTC)
unix_converter = 1000
mileseconds_converter = 3600000
start_date = int(start_date.timestamp() * unix_converter)
end_date = int(end_date.timestamp() * unix_converter)


class APIEndPointErrorMessage(Exception):
        pass 
class DateRange:
        def __init__(self, start_date, end_date):
                self.start_date = start_date
                self.end_date =  end_date     
        def calculate_total_work_days(self):
                business_dates = len(pd.bdate_range(start_date,  end_date))
                return(business_dates)

class ClickUpClient:
        click_up_api_key = os.getenv("cu_api_key")
        headers =   {"Authorization": click_up_api_key,  # noqa: RUF012
                        "accept": "application/json",
                        "Content-Type": "application/json"}    
        base_url = "https://api.clickup.com/api/v2/"
        workspace_id = os.getenv("workspace_id") 
        test_space_id = os.getenv("test_space")     
        
        def api_call_func(self, teams_end_point , get_tasks_end_point, get_entries_end_point):
                if not hasattr(self,"count"):
                        self.count = 0 
                if not hasattr(self, "number"):
                        self.number = 0
                if not hasattr(self,"results"):
                        self.results = {}
                
                end_point_list = [teams_end_point, get_tasks_end_point, get_entries_end_point ]
                
                while self.count < 3:            
                        endpoint = end_point_list[self.number]
                        self.number += 1 
                        self.count += 1 

                        click_up_api_call_request = requests.get(self.base_url + endpoint, headers=self.headers)
                        
                        if click_up_api_call_request.status_code != 200:
                                self.count -= 1 
                                self.number -= 1 
                                raise APIEndPointErrorMessage(f"User group request API call failed on endpoint {endpoint}. ERROR CODE: {click_up_api_call_request}")
                        elif self.count == 1:
                                user_teams_json = click_up_api_call_request.json().get("groups")
                                self.results["groups:"] = user_teams_json
                                continue
                        elif self.count == 2:
                                tasks_json = click_up_api_call_request.json().get("tasks")
                                self.results["tasks:"] = tasks_json 
                                continue
                        elif self.count == 3: 
                                entries_json = click_up_api_call_request.json().get("data")
                                self.results["entries"] = entries_json
                                return self.results
def data_normalization(results):
        user_groups_df = pd.json_normalize(results["groups:"])  
        user_groups_df = user_groups_df.explode('members')
        user_groups_df["team_name"] = user_groups_df['name']
        user_groups_df["team_member"] = user_groups_df['members'].apply(lambda x: x.get("username") if isinstance(x,dict) and len(x) > 0 else None)
        user_groups_df["team_member_id"] = user_groups_df['members'].apply(lambda x: x.get("id") if isinstance(x,dict) and len(x) > 0 else None)
        user_groups_df["team_member_id"] = user_groups_df['team_member_id'].astype('Int64')
        user_groups_df_filtered = user_groups_df[[
                'team_name',
                'team_member',
                'team_member_id',
                ]].copy
        print(user_groups_df_filtered)
        
def display_data():
        pass 
def rag_pipeline():
        pass 




def main():
        workspace_id = os.getenv("workspace_id") 
        test_space_id = os.getenv("test_space") 
        teams_end_point = f"group?team_id={workspace_id}" 
        get_tasks_end_point=f"team/{workspace_id}/task?space_ids[]={test_space_id}" 
        get_entries_end_point = f"team/{workspace_id}/time_entries?start_date={start_date}&end_date={end_date}"
        class_client = ClickUpClient()
        retries = 0
        max_retries = 5
        api_time_delay = 30 
        api_error_message = "API Authentication failed "
        last_error = None
        
        #while click_up_api_call_test = class_client.api_call_func
        
        while retries < max_retries:        
                
                
                try: 
                        click_up_api_call_test = class_client.api_call_func(teams_end_point, get_tasks_end_point, get_entries_end_point) 
                        print(f"CLICKUP API CALL TEST IS {type(click_up_api_call_test.results)}")        
                        #print(click_up_api_call_test.results)
                        # if click_up_api_call_test(self.result) is not None:
                        #         break 


                                                
                except APIEndPointErrorMessage as api_error_message: 
                                retries += 1
                                last_error = str(api_error_message)
                                print(f"This is attempt number {retries} you have {max_retries - retries} remaining")
                                print(api_error_message)
                                time.sleep(api_time_delay)

                                
        if retries == max_retries and last_error is not None :
                raise APIEndPointErrorMessage(last_error)
        else:
                print(api_error_message)
        #data_normalization(click_up_api_call_test)
main()


        

