import streamlit as st
import os
from openai import AzureOpenAI
import time
import re
from theme import apply_theme
from layout import (
    setup_page_layout,
    create_header,
    create_chat_container,
    format_assistant_message,
    format_user_message,
    create_sidebar
)

def init_client():
    return AzureOpenAI(
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"], 
        api_key=st.secrets["AZURE_OPENAI_API_KEY"],
        api_version="2024-05-01-preview"
    )

def create_assistant(client):
    if 'assistant_id' not in st.session_state:
        assistant = client.beta.assistants.create(
            model="gpt-4",
            instructions="""You are an AI language model specialized in drafting professional responses for bid proposals, as if you were Cognizant...""",
            tools=[{"type": "file_search", 
                   "file_search": {"ranking_options": {"ranker": "default_2024_08_21", "score_threshold": 0}}}],
            tool_resources={"file_search": {"vector_store_ids": ["vs_BEttQaXKvQNZSnvVCwGUbkXz"]}},
            temperature=1,
            top_p=1
        )
        st.session_state.assistant_id = assistant.id
    return st.session_state.assistant_id

def format_message_with_citations(message):
    parts = re.split(r'(\[\d+:\d+:source\])', message)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        formatted_text = ""
        for part in parts:
            if re.match(r'\[\d+:\d+:source\]', part):
                st.write(formatted_text, unsafe_allow_html=True)
                st.info(f"Citation: {part}")
                formatted_text = ""
            else:
                formatted_text += part
        if formatted_text:
            st.write(formatted_text, unsafe_allow_html=True)
    
    with col2:
        if re.search(r'\[\d+:\d+:source\]', message):
            with st.expander("📄 Source Files"):
                st.write("Available sources referenced")

def main():
    # Setup page layout and theme
    setup_page_layout()
    apply_theme()
    
    # Create layout
    col1, col2, col3 = create_header()
    create_sidebar()
    
    with col2:
        # Initialize session state
        if 'client' not in st.session_state:
            st.session_state.client = init_client()
        
        if 'thread_id' not in st.session_state:
            thread = st.session_state.client.beta.threads.create()
            st.session_state.thread_id = thread.id
        
        # Create or get assistant
        assistant_id = create_assistant(st.session_state.client)
        
        # Initialize messages list if not exists
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display existing messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    format_message_with_citations(message["content"])
                else:
                    st.write(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask your question about the RFI..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            st.session_state.client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )

            run = st.session_state.client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant_id
            )

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    while run.status in ['queued', 'in_progress', 'cancelling']:
                        time.sleep(1)
                        run = st.session_state.client.beta.threads.runs.retrieve(
                            thread_id=st.session_state.thread_id,
                            run_id=run.id
                        )

                    if run.status == 'completed':
                        messages = st.session_state.client.beta.threads.messages.list(
                            thread_id=st.session_state.thread_id
                        )
                        assistant_message = messages.data[0].content[0].text.value
                        st.session_state.messages.append(
                            {"role": "assistant", "content": assistant_message}
                        )
                        format_message_with_citations(assistant_message)
                    else:
                        st.error(f"Error: {run.status}")

if __name__ == "__main__":
    main()