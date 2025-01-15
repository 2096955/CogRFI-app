import streamlit as st

def setup_page_layout():
    st.set_page_config(
        page_title="Cognizant RFI Assistant",
        page_icon="🤖",
        layout="wide"
    )

def create_header():
    # Create the three-column layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Add Cognizant logo and title
        st.markdown("""
            <div style="display: flex; align-items: center; margin-bottom: 2rem;">
                <img src="https://www.cognizant.com/content/dam/cognizant_foundation/Dotcom/images/svg/Cognizant-logo-blue.svg" 
                     style="height: 40px; margin-right: 1rem;">
                <h1 style="margin: 0;">RFI Assistant</h1>
            </div>
        """, unsafe_allow_html=True)
    
    return col1, col2, col3

def create_chat_container():
    # Create chat message container with styling
    st.markdown("""
        <div class="chat-container" style="
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        ">
        </div>
    """, unsafe_allow_html=True)

def format_assistant_message(message_content):
    st.markdown(f"""
        <div class="assistant-message" style="
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        ">
            {message_content}
        </div>
    """, unsafe_allow_html=True)

def format_user_message(message_content):
    st.markdown(f"""
        <div class="user-message" style="
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: right;
        ">
            {message_content}
        </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    with st.sidebar:
        st.markdown("### Features")
        st.markdown("- 💬 Chat Interface")
        st.markdown("- 📄 Document Search")
        st.markdown("- 🔍 Citation Support")
        
        st.markdown("---")
        
        st.markdown("### About")
        st.markdown("This AI assistant helps with RFI responses using Cognizant's knowledge base.")