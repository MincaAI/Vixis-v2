import streamlit as st
import os

# Must be the first Streamlit command (before any other st.* calls)
st.set_page_config(page_title="Financial Report Generator", layout="wide")

from streamlit_js_eval import streamlit_js_eval  # Handles cookies
from datetime import datetime
from navbar import navbar
from interface import interface
from interface1 import interface1


def get_user_email():
    """Get user email from Azure Easy Auth headers or environment"""
    # Try to get from environment (Azure Easy Auth sets this)
    user_email = os.getenv("X-MS-CLIENT-PRINCIPAL-NAME", None)
    if not user_email:
        # Fallback for local development
        user_email = os.getenv("USER_EMAIL", "dev@local.com")
    return user_email


if __name__ == "__main__":
    # Store user email in session state for use in navbar
    if "user_email" not in st.session_state:
        st.session_state.user_email = get_user_email()

    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Note d’analyse sectorielle"

    navbar()
    
    if st.session_state.selected_page == "Note d’analyse sectorielle":
        st.title("Note d’analyse sectorielle")
        interface()
    elif st.session_state.selected_page == "Note d’analyse mono sous-jacent":
        st.title("Note d’analyse mono sous-jacent")
        interface1()
    # main()
