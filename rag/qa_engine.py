import streamlit as st
from langchain_groq import ChatGroq


def get_llm():

    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        st.error("GROQ_API_KEY is missing in secrets.toml")
        st.stop()

    return ChatGroq(
        model="llama3-8b-8192",
        temperature=0.3,
        api_key=api_key
    )