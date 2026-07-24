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
# GOOGLE_GENAI_USE_VERTEXAI="false"
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# from chromadb.utils.embedding_functions import GoogleGeminiEmbeddingFunction

start_date = st.datetime_input(label="Please enter start date", format="YYYY/MM/DD", value=dt(2026, 4, 1, tzinfo=timezone.utc), key="start_date")
end_date =  st.datetime_input(label="Please enter end date", format="YYYY/MM/DD", value=dt(2026, 5, 1, tzinfo=timezone.utc), key="end_date" )
us_holidays = holidays.US()        
class DateRange:
        def __init__(self, start_date, end_date, us_holidays):
                self.start_date = start_date
                self.end_date =  end_date        
                self.holidays = us_holidays
        def calculate_total_work_days(self, start_date, end_date):
                self.start_date = start_date
                self.end_date = end_date

                date_differences = end_date - start_date
                total_work_days = date_differences.days
                date_differences_delta = range(total_work_days)
DateRange.calculate_total_work_days()
                                

def call_api(DateRange):
                


        click_up_api_key = os.getenv("cu_api_key")
        headers =   {"Authorization": click_up_api_key, 
                "accept": "application/json",
                "Content-Type": "application/json"}    
        workspace_id = os.getenv("workspace_id") 
        test_space_id = os.getenv("test_space")  #This will cause the API to only pull from one workspace          
        class ClickUpClient:
                def __init__(self,api_key, headers, workspace_id, test_space_id):
                        self.api_key = api_key
                        self.headers = headers
                        self.workspace_id = workspace_id
                        self.test_space_id = test_space_id
                
        clickup_api_call = ClickUpClient(click_up_api_key, headers, workspace_id, test_space_id)



        if clickup_api_call.workspace_id is None:
                raise ValueError("Workspace Id cannot be None.")
        print  
        

call_api()