import streamlit as st
import whisper
import torch
from transformers import pipeline
import openai

def main():
    st.title("AI Meeting Companion")

    # Sidebar selection for transcription method
    st.sidebar.subheader("Transcription Options")
    transcribe_method = st.sidebar.selectbox(
        "Select transcription method:",
        ("Local Whisper", "API Whisper")
    )

    # Sidebar selection for summarization method
    st.sidebar.subheader("Summarization Options")
    summarize_method = st.sidebar.selectbox(
        "Select summarization method:",
        ("Local Summarizer", "OpenAI GPT")
    )

    # Sidebar selection for action item extraction method
    st.sidebar.subheader("Action Item Extraction")
    action_method = st.sidebar.selectbox(
        "Select extraction method:",
        ("OpenAI GPT", "None")
    )

    # File uploader for audio
    uploaded_file = st.file_uploader("Upload your meeting audio", type=["wav", "mp3", "mp4"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp_audio_input", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 1) Transcription
        st.write("### Step 1: Transcription")
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio("temp_audio_input", transcribe_method)
        st.success("Transcription Complete!")
        st.text_area("Transcript", transcript, height=200)

        # 2) Summarization
        st.write("### Step 2: Summarization")
        with st.spinner("Summarizing..."):
            summary = summarize_text(transcript, summarize_method)
        st.success("Summarization Complete!")
        st.text_area("Summary", summary, height=150)

        # 3) Action Item Extraction
        st.write("### Step 3: Action Items & Decisions")
        if action_method != "None":
            with st.spinner("Extracting Action Items..."):
                actions = extract_action_items(transcript, action_method)
            st.success("Extraction Complete!")
            st.text_area("Action Items", actions, height=150)
        else:
            st.warning("No action item extraction method selected.")

        # 4) Sentiment Analysis
        st.write("### Step 4: Sentiment Analysis")
        with st.spinner("Analyzing sentiment..."):
            sentiment_results = analyze_sentiment(transcript)
        st.success("Sentiment Analysis Complete!")
        st.json(sentiment_results)  # or format nicely

if __name__ == "__main__":
    main()
