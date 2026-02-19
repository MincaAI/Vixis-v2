import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pytz
from sharepoint import SharePointClient

def navbar():
    # Ensure session state has selected_page
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Note d’analyse sectorielle"

    with st.sidebar:
        selected = option_menu(
            menu_title="Vixis - Note d’analyse",
            options=["Note d’analyse sectorielle", "Note d’analyse mono sous-jacent"],
            default_index=["Note d’analyse sectorielle", "Note d’analyse mono sous-jacent"].index(st.session_state.selected_page),
            key="navigation",
            styles={
                "container": {
                    "background-color": "#F8F9FA",
                    "padding": "8px",
                    "border-radius": "6px",
                },
                # Ensure icon style is commented out
                # "icon": {"color": "#4B0082", "font-size": "22px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "padding": "12px",
                    "color": "#333333",
                    "border-radius": "5px",
                    "transition": "0.3s ease-in-out",
                    "font-family": "Arial, sans-serif",
                },
                "nav-link-selected": {
                    "background-color": "#4B0082",
                    "color": "white",
                    "font-weight": "bold",
                    "font-family": "Arial, sans-serif",
                },
            }
        )

        # Update session state with selection
        st.session_state.selected_page = selected

        # Centered button with same style as navbar
        st.markdown(
            """
            <style>
                .update-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-top: 20px;
                }
                .update-button {
                    background-color: #4B0082;
                    color: white;
                    font-size: 21px;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    padding: 12px 20px;
                    border-radius: 5px;
                    width: 100%;
                    text-align: center;
                    cursor: pointer;
                    transition: 0.3s ease-in-out;
                    border: none;
                }
                .update-button:hover {
                    background-color: #5A0099;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Centered button (real Streamlit button inside styled layout)



        
        st.markdown(
            """
            <style>

                /* Email Text */
                .profile-email {
                    font-size: 50px;
                    color: #333;
                    font-weight: bold;
                    margin-top: 10px;
                    font-family: 'Arial', sans-serif;
                }

                /* Logout Button */
                .logout-button {
                    background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    border: none;
                    transition: 0.3s ease-in-out;
                    width: 100%;
                    margin-top: 15px;
                    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
                }
                .logout-button:hover {
                    background: linear-gradient(90deg, #d43f3f, #e64a4a);
                    transform: scale(1.05);
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # Add user guide link
        guide_url = "https://docs.google.com/document/d/1sk0GYlztWo-fny5LVjb3QsHz-IvRYDgj5wDL0obNZQU/edit?tab=t.0"
        st.markdown(f'<p style="font-size: 16px; color: #333; font-weight: bold; margin-top: 2px; font-family: Arial, sans-serif;">Guide d\'utilisation: <a href="{guide_url}" target="_blank" style="color: #0066cc; text-decoration: underline;">Lire le guide</a></p>', unsafe_allow_html=True)
        
        # Add divider
        st.markdown("<hr style='border: 0.5px solid #ccc;'>", unsafe_allow_html=True)
        
        # Add Sharepoint link and Update Data button side by side
        col1, col2 = st.columns([1,1])
        with col1:
            sharepoint_url = "https://vixis.sharepoint.com/:x:/s/Intranet/EUFYEJiKVDhPoW9ARN0jcLQBc6hugWQiIVi3rhu8OD2f9Q?e=UKxo3D"
            st.markdown(f'<p class="profile-email"><a href="{sharepoint_url}" target="_blank" style="color: #0066cc; text-decoration: underline;">Sharepoint data</a></p>', unsafe_allow_html=True)
        with col2:
            if st.button("Update Data", key="update_data", help="Click to refresh data"):
                with st.spinner("Updating data... ⏳"):
                    try:
                        sp = SharePointClient()
                        sp.load_data()
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Erreur lors de la mise à jour : {e}")
        
        # Add divider
        st.markdown("<hr style='border: 0.5px solid #ccc;'>", unsafe_allow_html=True)
        
        # Add current Paris date
        paris_tz = pytz.timezone('Europe/Paris')
        current_paris_time = datetime.now(paris_tz).strftime("%d/%m/%Y")
        st.markdown(f'<p style="font-size: 14px; color: #333; margin-top: 4px; margin-bottom: 2px; font-family: Arial, sans-serif;">Date: {current_paris_time}</p>', unsafe_allow_html=True)
        
        # Add user info
        user_email = "User: " + st.user.name
        st.markdown(f'<p style="font-size: 14px; color: #333; margin-top: 2px; font-family: Arial, sans-serif;">{user_email}</p>', unsafe_allow_html=True)
        
        # Add more vertical space before logout button
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        
        # Logout Button aligned with Update Data
        col1, col2 = st.columns([2,1])
        with col1:
            if st.button("🚪 Logout", key="logout"):
                st.logout()

        st.markdown('</div>', unsafe_allow_html=True)
