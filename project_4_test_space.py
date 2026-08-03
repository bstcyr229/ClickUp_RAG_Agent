import os
import datetime
import requests
import json 

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt   

import chromadb


from google import genai
from datetime import datetime as dt, timedelta , timezone 
from dotenv import load_dotenv
load_dotenv()

# GOOGLE_GENAI_USE_VERTEXAI="false"
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# from chromadb.utils.embedding_functions import GoogleGeminiEmbeddingFunction

#COMMENTED OUT TO USE A PRE-DEFINED DATE FOR TESTING start_date = st.datetime_input(label="Please enter start date", format="YYYY/MM/DD", value=dt(2026, 4, 1, tzinfo=timezone.utc), key="start_date")
#end_date =  st.datetime_input(label="Please enter end date", format="YYYY/MM/DD", value=dt(2026, 5, 1, tzinfo=timezone.utc), key="end_date" )

start_date = dt(2026, 4, 1, tzinfo=timezone.utc)
end_date =  dt(2026, 5, 1, tzinfo=timezone.utc)
unix_converter = 1000
mileseconds_converter = 3600000
start_date = int(start_date.timestamp() * unix_converter)
end_date = int(end_date.timestamp() * unix_converter)
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
                end_point_list = [teams_end_point, get_tasks_end_point, get_entries_end_point ]
                count = 0
                number = 0
                while count < 3:     
                        endpoint = end_point_list[number]
                        number += 1 
                        count += 1 


                        click_up_api_call_request = requests.get(self.base_url + endpoint, headers=self.headers)
                        if click_up_api_call_request.status_code != 200:
                                click_up_api_end_point_error_message = f"User group request API call failed. ERROR CODE: {click_up_api_call_request}"
                                return print(click_up_api_end_point_error_message)   
                        elif count == 1 :
                                user_teams_json = click_up_api_call_request.json().get("groups")
                        elif count == 2:
                                tasks_json = click_up_api_call_request.json().get("tasks")
                        else: 
                                entries_json = click_up_api_call_request.json().get("data")
                if type(user_teams_json) and type(tasks_json) and type(entries_json) != None:
                        return user_teams_json, tasks_json , entries_json
def main():
        workspace_id = os.getenv("workspace_id") 
        test_space_id = os.getenv("test_space") 
        teams_end_point = f"group?team_id={workspace_id}" #No / failure injection
        get_tasks_end_point=f"team/{workspace_id}/task?space_ids[]={test_space_id}"
        get_entries_end_point = f"team/{workspace_id}/time_entries?start_date={start_date}&end_date={end_date}"
        class_client = ClickUpClient()
        click_up_api_call_test = class_client.api_call_func(teams_end_point, get_tasks_end_point, get_entries_end_point)

main()


        

