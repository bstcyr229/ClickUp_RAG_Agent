import chromadb
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt   
import requests
import os
import json 
import holidays
from google import genai


from datetime import datetime as dt, timedelta , timezone 

from dotenv import load_dotenv
load_dotenv()
GOOGLE_GENAI_USE_VERTEXAI="false"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
from chromadb.utils.embedding_functions import GoogleGeminiEmbeddingFunction




def user_input_for_dashboard():
        start_date = st.datetime_input(label="Please enter start date", format="YYYY/MM/DD", value=dt(2026, 4, 1, tzinfo=timezone.utc), key="start_date")
        end_date =  st.datetime_input(label="Please enter end date", format="YYYY/MM/DD", value=dt(2026, 5, 1, tzinfo=timezone.utc), key="end_date" )
        dates_tuple = start_date, end_date
        return dates_tuple

def fetching_tasks(dates_tuple):
        start_date = dates_tuple[0]
        end_date = dates_tuple[1]

        click_up_api_key = os.getenv("cu_api_key")
        headers =   {"Authorization": click_up_api_key, 
                    "accept": "application/json",
                    "Content-Type": "application/json"}
                    
        workspace_id = os.getenv("workspace_id") #This will cause the API to only pull from one workspace
        test_space_id = os.getenv("test_space")            
        class API_client:
            def __init__(self,api_key, headers, workspace_id, test_space_id):
                self.api_key = api_key
                self.headers = headers
                self.workspace_id = workspace_id
                self.test_space_id = test_space_id
                    
        clickup_api_call = API_client(click_up_api_key, headers, workspace_id, test_space_id)
        if clickup_api_call.workspace_id is None:
            return st.write("No workspace Id")  