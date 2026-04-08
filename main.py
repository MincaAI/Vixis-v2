import streamlit as st

# Must be the first Streamlit command (before any other st.* calls)
st.set_page_config(page_title="Financial Report Generator", layout="wide")

from streamlit_js_eval import streamlit_js_eval  # Handles cookies
from datetime import datetime
from navbar import navbar
from interface import interface
from interface1 import interface1


if __name__ == "__main__":
    # Check if user is logged in (st.login must be configured in secrets)
    try:
        logged_in = st.user.is_logged_in
    except AttributeError:
        logged_in = True  # skip auth gate when st.login is not configured
    if not logged_in:
        st.header("Veuillez vous connecter pour continuer.")
        st.button("Se connecter avec Microsoft", on_click=st.login)
        st.stop()

    # Store user email in session state
    if "user_email" not in st.session_state:
        st.session_state.user_email = getattr(st.user, "email", None) or "Unknown"

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
