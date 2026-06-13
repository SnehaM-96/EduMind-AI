import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        google_api_key=st.secrets["GOOGLE_API_KEY"]
    )

    return llm