# modules/summarization.py

from openai import OpenAI
import streamlit as st

# Set up OpenAI API client
client = OpenAI()


def summarize_transcript(transcript: str) -> str:
    developer_message = {
        "role": "developer",
        "content": st.secrets["SUMMARIZATION_PROMPT"],
    }
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": transcript,
            }
        ],
    }

    messages = [developer_message, user_message]
    response = client.responses.create(model="gpt-4o", input=messages)
    return response.output_text
