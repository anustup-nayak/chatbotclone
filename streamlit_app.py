import streamlit as st
from openai import OpenAI

# Set page title
st.title("ChatGPT-like App")

# Initialize session state for storing conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Setup for OpenAI API key
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
model = st.sidebar.selectbox("Select Model:", ["gpt-3.5-turbo", "gpt-4"], index=0)

# Initialize OpenAI client
if api_key:
    client = OpenAI(api_key=api_key)
else:
    st.sidebar.warning("Please enter your OpenAI API key to continue")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask something..."):
    # Don't proceed if API key is not provided
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

