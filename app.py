import streamlit as st
import os

# Import our modules
from modules.transcription import (
    transcribe_audio,
    download_audio_from_link
)
from modules.summarization import summarize_text
from modules.action_extraction import extract_action_items
from modules.sentiment import analyze_sentiment

def main():
    st.title("summarAIze")

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

    # Provide two ways to get audio: by file upload OR by link
    st.write("### Audio Input")
    audio_url = st.text_input("Enter a link to an audio file (optional):", "")
    uploaded_file = st.file_uploader("Or upload your meeting audio", type=["wav", "mp3", "mp4"])

    audio_path = None

    # If user provided a URL, try to download it
    if audio_url:
        try:
            with st.spinner("Downloading audio from link..."):
                download_audio_from_link(audio_url, "temp_audio_input")
            audio_path = "temp_audio_input"
            st.success("Downloaded audio from link successfully!")
        except Exception as e:
            st.error(f"Error downloading audio: {e}")

    # If user uploaded a file, use that instead (overriding the link-based audio if both provided)
    if uploaded_file is not None:
        with open("temp_audio_input", "wb") as f:
            f.write(uploaded_file.getbuffer())
        audio_path = "temp_audio_input"
        st.success("Uploaded file saved locally.")

    if audio_path is not None:
        # Show partial transcription slider
        st.write("### Step 1: Select Audio Range for Transcription")

        # Let's figure out the duration of the file to set slider range
        try:
            from pydub import AudioSegment
            audio_segment = AudioSegment.from_file(audio_path)
            duration_sec = len(audio_segment) / 1000.0
        except Exception as e:
            st.error(f"Failed to load audio: {e}")
            return

        st.write(f"Audio Duration: {duration_sec:.2f} seconds")

        # Create a range slider for partial selection
        start_time, end_time = st.slider(
            "Select the portion of the audio to process (in seconds)",
            min_value=0.0,
            max_value=float(duration_sec),
            value=(0.0, float(duration_sec)),
            step=0.5
        )

        # Transcription
        st.write("### Step 2: Transcription")
        if st.button("Transcribe Selected Range"):
            with st.spinner("Transcribing..."):
                transcript = transcribe_audio(audio_path, transcribe_method, start_time, end_time)
            st.success("Transcription Complete!")
            st.text_area("Transcript", transcript, height=200)

            # Summarization
            st.write("### Step 3: Summarization")
            with st.spinner("Summarizing..."):
                summary = summarize_text(transcript, summarize_method)
            st.success("Summarization Complete!")
            st.text_area("Summary", summary, height=150)

            # Action Item Extraction
            st.write("### Step 4: Action Items & Decisions")
            if action_method != "None":
                with st.spinner("Extracting Action Items..."):
                    actions = extract_action_items(transcript, action_method)
                st.success("Extraction Complete!")
                st.text_area("Action Items", actions, height=150)
            else:
                st.warning("No action item extraction method selected.")

            # Sentiment Analysis
            st.write("### Step 5: Sentiment Analysis")
            with st.spinner("Analyzing sentiment..."):
                sentiment_results = analyze_sentiment(transcript)
            st.success("Sentiment Analysis Complete!")
            st.json(sentiment_results)  # or format nicely
        else:
            st.info("Click 'Transcribe Selected Range' to process the chosen audio segment.")

    else:
        st.info("Please provide a link OR upload an audio file to proceed.")

if __name__ == "__main__":
    main()
