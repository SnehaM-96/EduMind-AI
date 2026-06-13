import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():

    api_key = st.secrets.get("GOOGLE_API_KEY")

    if not api_key:
        st.error("GOOGLE_API_KEY is missing in secrets.toml")
        st.stop()

    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        google_api_key=api_key
    )