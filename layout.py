import streamlit as st

def setup_page_layout():
    # No st.set_page_config here
    pass
    
def create_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: 2rem;">
                <img src="cognizant-logo.jpg" width="40" height="40" style="margin-right: 1rem;">
                <h1 style="
                    margin: 0;
                    color: #0033A1;
                    font-size: 2.5rem;
                    font-weight: 700;
                    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);">
                    RFI Assistant
                </h1>
            </div>

            """,
            unsafe_allow_html=True
        )
    
    return col1, col2, col3

def create_chat_container():
    st.markdown("""
        <div class="chat-container" style="
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        ">
        </div>
    """, unsafe_allow_html=True)