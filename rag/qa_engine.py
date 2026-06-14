import streamlit as st
from langchain_groq import ChatGroq


def get_llm():

    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        st.error("GROQ_API_KEY is missing in secrets.toml")
        st.stop()

    return ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0.3,
        api_key=api_key
    )