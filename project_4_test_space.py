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

#start_date = st.datetime_input(label="Please enter start date", format="YYYY/MM/DD", value=dt(2026, 4, 1, tzinfo=timezone.utc), key="start_date")
#end_date =  st.datetime_input(label="Please enter end date", format="YYYY/MM/DD", value=dt(2026, 5, 1, tzinfo=timezone.utc), key="end_date" )

start_date = dt(2026, 4, 1, tzinfo=timezone.utc)
end_date =  dt(2026, 5, 1, tzinfo=timezone.utc)
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
        test_space_id = os.getenv("test_space")  #This will cause the API to only pull from one workspace        
        get_tasks_end_point= f"team/{workspace_id}/task?space_ids[]={test_space_id}" 
                                
        def api_call_func(self, teams_end_point):
                



                get_teams_api_call = requests.get(self.base_url + teams_end_point, headers=self.headers)
                if get_teams_api_call.status_code != 200:
                        teams_api_end_point_error_message = f"User group request API call failed. ERROR CODE: {get_teams_api_call}"
                        return print(teams_api_end_point_error_message)   
                else:
                        user_teams_json = get_teams_api_call.json().get("groups")  
                        return(print(user_teams_json[0]['id']))
                #get_teams_api_call = requests.get(self.base_url + teams_end_point)

                #get_tasks_end_point = 

def main():
        workspace_id = os.getenv("workspace_id") 
        test_space_id = os.getenv("test_space") 
        teams_end_point = f"/group?team_id={workspace_id}" #Reomve / failure injection
        #get_tasks_end_point=
        class_client = ClickUpClient()
        click_up_api_call_test = class_client.api_call_func(teams_end_point)

main()

        

