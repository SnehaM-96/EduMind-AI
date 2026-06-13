import streamlit as st
from google import genai

def get_llm():
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    return client

