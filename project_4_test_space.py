import chromadb
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt   
import requests
import os
import json 
import datetime

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



def call_api(DateRange):
        click_up_api_key = os.getenv("cu_api_key")
        headers =   {"Authorization": click_up_api_key, 
                "accept": "application/json",
                "Content-Type": "application/json"}    
        workspace_id = os.getenv("workspace_id") 
        test_space_id = os.getenv("test_space")  #This will cause the API to only pull from one workspace
        url = f'https://api.clickup.com/api/v2/team/{workspace_id}/task?space_ids[]={test_space_id}'
        class ClickUpClient:
                def __init__(self,api_key, headers, workspace_id, test_space_id, url):
                        self.api_key = api_key
                        self.headers = headers
                        self.workspace_id = workspace_id
                        self.test_space_id = test_space_id 
                        self.url = url 
                def print_params(self):
                        print(f"API KEY IS {self.api_key}")
                        print(f"HEADERS ARE {self.headers}")
                        print(f"WORKSPACE ID IS {self.workspace_id}")
                        print(f"TEST SPACE ID IS {self.test_space_id}")
                        print(f"URL IS {self.url}")

        clickup_api_call = ClickUpClient(click_up_api_key, headers, workspace_id, test_space_id, url)
        clickup_api_call_test = clickup_api_call.print_params()
        print(clickup_api_call_test)



        if clickup_api_call.workspace_id is None:
                raise ValueError("Workspace Id cannot be None.")  

call_api(DateRange)