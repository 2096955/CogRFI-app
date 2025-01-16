import streamlit as st

# Cognizant brand colors
COGNIZANT_BLUE = "#0033A1"
LIGHT_BLUE = "#E8EEF9"
WHITE = "#FFFFFF"

def apply_theme():
    st.markdown(f"""
        <style>
        .main {{
            background-color: {WHITE};
        }}
        
        .stApp header {{
            background-color: {WHITE};
            border-bottom: 1px solid #ddd;
        }}
        
        h1 {{
            color: {COGNIZANT_BLUE};  /* Ensure the title color is Cognizant Blue */
            font-weight: 600;
            padding: 1rem 0;
        }}
        
        .stChatMessage {{
            background-color: {WHITE};
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stChatMessage[data-testid="user-message"] {{
            background-color: {LIGHT_BLUE};
        }}
        
        .stChatMessage[data-testid="assistant-message"] {{
            background-color: #FFFFFF;
            border: 1px solid #E8EEF9;
            color: #333;  /* Ensures the text color is dark gray */
        }}
        
        .stChatInputContainer {{
            border-color: {COGNIZANT_BLUE};
            padding: 1rem;
        }}
        
        .stButton button {{
            background-color: {COGNIZANT_BLUE};
            color: {WHITE};
            border-radius: 5px;
        }}
        
        .citation-box {{
            background-color: {LIGHT_BLUE};
            padding: 0.5rem;
            border-radius: 5px;
            margin: 0.5rem 0;
        }}

        /* Cognizant logo styles */
        .logo-container {{
            display: flex;
            align-items: center;
            margin-bottom: 2rem;
        }}

        .logo-icon {{
            width: 40px;
            height: 40px;
            background: linear-gradient(45deg, #00A9E0, #1B1464);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            margin-right: 1rem;
        }}

        .logo-text {{
            margin: 0;
            color: {COGNIZANT_BLUE};
            font-size: 1.5rem;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)