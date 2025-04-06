# from transformers import AutoTokenizer, pipeline
# import numpy as np


# # Chunk text with overlap and analyze sentiment
# def analyze_sentiment(text, model_name="bert-large-uncased"):
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

#     tokens = tokenizer.tokenize(text)
#     max_length = 450
#     overlap = 62
#     chunks = []

#     for i in range(0, len(tokens), max_length - overlap):
#         chunk_tokens = tokens[i : i + max_length]
#         chunks.append(tokenizer.convert_tokens_to_string(chunk_tokens))

#     sentiments = []
#     for chunk in chunks:
#         result = sentiment_analyzer(chunk)[0]
#         score = result["score"] * (1 if result["label"] == "POSITIVE" else -1)
#         sentiments.append(score)

#     avg_score = np.mean(sentiments)
#     final_label = "POSITIVE" if avg_score >= 0 else "NEGATIVE"

#     return {
#         "label": final_label,
#         "score": abs(avg_score),
#         "chunks_processed": len(chunks),
#     }


from openai import OpenAI
import streamlit as st

# Set up OpenAI API client
client = OpenAI()


def analyze_sentiment(transcript: str) -> str:
    developer_message = {
        "role": "developer",
        "content": st.secrets["SENTIMENT_ANALYSIS_PROMPT"],
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
