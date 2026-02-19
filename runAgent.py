from helpers.fetchApi import *
import streamlit as st
import re

def replace_headers(text):
    return re.sub(r'^(#{1,5})\s', '###### ', text, flags=re.MULTILINE)

def run_agent(col, agent_name, prompt_lines, api_url, key_output, key_button, uploads = None):
    """
    Function to run an agent in a specified Streamlit column.

    Parameters:
    - agent_name (str): The display name of the agent.
    - col (streamlit column): The Streamlit column where the agent will be displayed.
    - prompt_lines (list): List of user-inputted stock prompts.
    - api_url (str): The API endpoint to fetch data.
    - key_output (str): The session state key for storing output.
    - key_button (str): The unique key for the button to trigger the agent.
    """
    with col:
        st.subheader(agent_name)
        agent_placeholder = st.empty()
        output_placeholder = st.empty()
        output_placeholder.markdown(f"<small>{st.session_state.get(key_output, '')}</small>", unsafe_allow_html=True)  # Persist output in small text

        with agent_placeholder:
            with st.status("L’agent est prêt ...", expanded=True) as status:
                if st.button("Run", key=key_button):
                    if prompt_lines:
                        if uploads:
                            print("uploads", uploads)
                            st.session_state[key_output] = fetch_data(api_url, {"question": prompt_lines, "uploads": uploads})
                        else: 
                            st.session_state[key_output] = fetch_data(api_url, {"question": prompt_lines})
                        st.session_state[key_output] = replace_headers(st.session_state[key_output])

                        output_placeholder.markdown(f"<small>{st.session_state[key_output]}</small>", unsafe_allow_html=True)
                        status.update(label="Tâche exécutée!", state="complete", expanded=False)
                