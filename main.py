import streamlit as st

# Must be the first Streamlit command (before any other st.* calls)
st.set_page_config(page_title="Financial Report Generator", layout="wide")

from streamlit_js_eval import streamlit_js_eval  # Handles cookies
from datetime import datetime
from navbar import navbar
from interface import interface
from interface1 import interface1

# region agent log
import sys, os, json as _json
try:
    _secrets_path = os.path.join(os.path.dirname(__file__) or ".", ".streamlit", "secrets.toml")
    _secrets_exists = os.path.isfile(_secrets_path)
    _secrets_size = os.path.getsize(_secrets_path) if _secrets_exists else 0
    _sections = []
    _auth_redir = "MISSING"
    _has_sp = False
    if _secrets_exists:
        import tomllib
        with open(_secrets_path, "rb") as _sf:
            _parsed = tomllib.load(_sf)
        _sections = list(_parsed.keys())
        _auth_redir = _parsed.get("auth", {}).get("redirect_uri", "MISSING")
        _has_sp = "sharepoint" in _parsed
    _diag = {"exists": _secrets_exists, "size": _secrets_size, "sections": _sections, "auth_redirect_uri": _auth_redir, "has_sharepoint": _has_sp}
    print(f"DIAG main.py: secrets.toml = {_json.dumps(_diag)}", file=sys.stderr, flush=True)
except Exception as _e:
    print(f"DIAG main.py: error reading secrets.toml: {_e}", file=sys.stderr, flush=True)
# endregion


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
        st.session_state.selected_page = "Note d'analyse sectorielle"

    navbar()
    
    if st.session_state.selected_page == "Note d'analyse sectorielle":
        st.title("Note d'analyse sectorielle")
        interface()
    elif st.session_state.selected_page == "Note d'analyse mono sous-jacent":
        st.title("Note d'analyse mono sous-jacent")
        interface1()
    # main()
