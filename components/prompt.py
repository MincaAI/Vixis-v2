import streamlit as st

def prompt():
    prompt = st.text_area(
        "Market analysis for tech stocks",
        placeholder="Enter list of stocks (i.e, AI, Tech, etc.)",
        height=100,
        key="prompt2"
    )

    return prompt