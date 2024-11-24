from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv() 

# Configure Google Generative AI with the API key from .env
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key is missing. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# Function to get responses from the Gemini Pro model
def get_gemini_response(question):
    try:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error communicating with the Gemini AI: {str(e)}")
        return None

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input box for user query
user_input = st.text_input("Ask a question:", key="input")
submit = st.button("Ask")

if submit and user_input:
    response = get_gemini_response(user_input)
    if response:
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", user_input))
        st.subheader("The Response is:")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    else:
        st.error("No response from the Gemini AI.")

# Display chat history
st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"**{role}:** {text}")
    