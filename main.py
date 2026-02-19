import streamlit as st

# Must be the first Streamlit command (before any other st.* calls)
st.set_page_config(page_title="Financial Report Generator", layout="wide")

from streamlit_js_eval import streamlit_js_eval  # Handles cookies
from datetime import datetime
from navbar import navbar
from interface import interface
from interface1 import interface1


if __name__ == "__main__":
    if not st.user.is_logged_in:
        st.header("Please log in to continue.")
        st.button("Log in with Microsoft", on_click=st.login)
        st.stop()

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
