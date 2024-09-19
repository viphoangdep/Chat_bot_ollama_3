import streamlit as st
from langchain_community.llms.ollama import Ollama
import json

# Initialize the language model
llm = Ollama(model="llama3")

# Function to initialize conversation memory
def initialize_conversation():
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    if "max_length" not in st.session_state:
        st.session_state.max_length = 150
    if "frequency_penalty" not in st.session_state:
        st.session_state.frequency_penalty = 0.2

# Function to display the Streamlit UI
def display_ui():
    st.title("Librarian Assistant")
    # Custom CSS for message bubbles
    st.markdown(
        """
        <style>
        .user-bubble {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            text-align: left;
            max-width: 60%;
            align-self: flex-start;
            margin-left: auto;  /* Move the user bubble to the right */
        }

        .bot-bubble {
            background-color: #ECECEC;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            text-align: left;
            max-width: 60%;
            align-self: flex-start;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function for generating LLaMA3 response
def generate_llama3_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    response = llm.invoke(prompt_input, stop=['<|eot_id|>'])
    return response

# Function to handle user input and generate response
def handle_input():
    prompt = st.text_area("Enter your prompt here")
    
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating..."):
                # Store user input in session state
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Generate response
                response = generate_llama3_response(prompt)
                
                # Store bot response in session state
                st.session_state.messages.append({"role": "assistant", "content": response})

# Function to display conversation as chat bubbles
def display_conversation():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main function to run the app
def main():
    initialize_conversation()
    display_ui()
    
    # Sidebar controls for max length and frequency penalty
    st.sidebar.header("Settings")
    st.session_state.max_length = st.sidebar.slider("Max Length", min_value=50, max_value=500, value=st.session_state.max_length)
    st.session_state.frequency_penalty = st.sidebar.slider("Frequency Penalty", min_value=0.0, max_value=1.0, value=st.session_state.frequency_penalty, step=0.1)
    
    # Add buttons to the sidebar
    if st.sidebar.button("Clear Conversation"):
        clear_chat_history()
    
    conversation_json = json.dumps(st.session_state['conversation'])
    st.sidebar.download_button(
        label="Save Conversation",
        data=conversation_json,
        file_name="conversation.json",
        mime="application/json"
    )
    
    handle_input()
    display_conversation()

if __name__ == "__main__":
    main()