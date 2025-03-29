import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get your API key from environment variable
api_key = os.getenv("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")

# Initialize OpenAI client with the key
client = OpenAI(api_key=api_key)

# Define system message (Agent AIPC's personality and rules)
agent_prompt = {
    "role": "system",
    "content": """
You are Agent AIPC, a Counsellor AI trained in client-centred therapy. 
You demonstrate empathy, emotional intelligence, and adhere to the SOLER method. 
Only play the role of counsellor when asked to 'Be a counsellor'. 
When asked to 'Be a client', respond as a realistic client based on case studies. 
Do not switch roles unless instructed. Remain consistent and emotionally authentic.
"""
}

# Streamlit UI
st.set_page_config(page_title="Agent AIPC - Counsellor AI", layout="wide")
st.title("🧠 Agent AIPC - Counselling Practice Tool")

st.markdown("Type below to interact with Agent AIPC as a counsellor or client.")

# Set up chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [agent_prompt]

# Input box
user_input = st.text_area("You:", height=100)

if st.button("Send"):
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call OpenAI API using new SDK format
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )

        # Extract reply
        reply = response.choices[0].message.content

        # Add assistant reply to history
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Show full conversation
for msg in st.session_state.messages[1:]:  # Skip system prompt
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Agent AIPC:** {msg['content']}")