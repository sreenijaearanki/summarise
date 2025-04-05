# modules/summarization.py

import openai
from transformers import pipeline

# Pre-load local summarizer pipeline
summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text_local(text: str) -> str:
    """
    Summarize text using a local Hugging Face model (e.g., BART).
    """
    # For large transcripts, consider chunking if needed
    summary = summarizer_model(
        text, 
        max_length=130, 
        min_length=30, 
        do_sample=False
    )
    return summary[0]['summary_text']

def summarize_text_openai(text: str) -> str:
    """
    Use OpenAI API (GPT) for summarization. 
    Make sure openai.api_key is set in your environment or code.
    """
    prompt = f"Summarize the following text:\n{text}\n"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def summarize_text(text: str, method: str) -> str:
    """
    Dispatcher function to select local vs. OpenAI GPT summarization.
    """
    if method == "Local Summarizer":
        return summarize_text_local(text)
    elif method == "OpenAI GPT":
        return summarize_text_openai(text)
    else:
        return "No valid summarization method selected."
