import streamlit as st
import os
from openai import AzureOpenAI
import time

# Initialize the Azure OpenAI client
def init_client():
    client = AzureOpenAI(
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
        api_key=st.secrets["AZURE_OPENAI_API_KEY"],
        api_version="2024-05-01-preview"
    )
    return client

# Create or get assistant
def get_assistant(client):
    # You may want to store this ID in secrets and reuse it
    assistant = client.beta.assistants.create(
        model="gpt-4",  # replace with your model deployment name
        instructions="""You are an AI language model specialized in drafting professional responses for bid proposals, as if you were Cognizant...""",  # Add full instructions here
        tools=[{"type": "file_search", "file_search": {"ranking_options": {"ranker": "default_2024_08_21", "score_threshold": 0}}}],
        tool_resources={"file_search": {"vector_store_ids": ["vs_BEttQaXKvQNZSnvVCwGUbkXz"]}},
        temperature=1,
        top_p=1
    )
    return assistant

# Process messages
def process_messages(client, thread, assistant):
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return [(msg.role, msg.content[0].text.value) for msg in messages]

def main():
    st.title("Cognizant RFI Assistant")
    
    # Initialize session state
    if "client" not in st.session_state:
        st.session_state.client = init_client()
    if "thread_id" not in st.session_state:
        thread = st.session_state.client.beta.threads.create()
        st.session_state.thread_id = thread.id
    if "assistant" not in st.session_state:
        st.session_state.assistant = get_assistant(st.session_state.client)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.write(content)

    # Chat input
    if prompt := st.chat_input("How can I help you?"):
        # Add user message to chat
        st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # Create and run the thread
        run = st.session_state.client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=st.session_state.assistant.id
        )

        # Show a spinner while processing
        with st.spinner("Thinking..."):
            # Poll for completion
            while run.status in ['queued', 'in_progress', 'cancelling']:
                time.sleep(1)
                run = st.session_state.client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )

            if run.status == 'completed':
                # Update messages
                st.session_state.messages = process_messages(
                    st.session_state.client,
                    thread=st.session_state.client.beta.threads.retrieve(st.session_state.thread_id),
                    assistant=st.session_state.assistant
                )
                st.rerun()
            else:
                st.error(f"Error: {run.status}")

if __name__ == "__main__":
    main()
