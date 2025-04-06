import streamlit as st
from collections import defaultdict
import re

# Import our modules
from modules.transcription import transcribe_audio
from modules.summarization import summarize_transcript
from modules.action_extraction import extract_action_items
from modules.sentiment import analyze_sentiment


def is_valid_url(url):
    # Regex to validate a general URL
    url_regex = re.compile(
        r"^(https?://)?"  # http:// or https://
        r"((([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})|"  # Domain name
        r"localhost|"  # localhost
        r"(\d{1,3}\.){3}\d{1,3})"  # OR IPv4
        r"(:\d+)?(/.*)?$"  # Optional port and path
    )
    return re.match(url_regex, url) is not None


def is_youtube_url(url):
    # Check if the URL is a YouTube link
    return "youtube.com" in url or "youtu.be" in url


def main():
    # App Title and Description
    st.set_page_config(page_title="summarAIze", layout="wide")
    st.title("🎙️ SummarAIze: Your AI-Powered Meeting Assistant")
    st.markdown(
        """
        Welcome to **SummarAIze**, your AI-powered assistant for transcribing, summarizing, and analyzing audio content. 
        Whether you're a student, professional, or lifelong learner, this tool helps you:
        - **Transcribe** audio files or YouTube links into text.
        - **Summarize** the key points for quick understanding.
        - **Extract actionable items** and decisions from the content.
        - **Analyze sentiment** to understand the tone of the discussion.

        Upload your audio file or provide a link to get started!
        """
    )

    # Sidebar for Input
    st.sidebar.header("Input Options")
    audio_url = st.sidebar.text_input("Enter a link to an audio file (optional):", "")

    # Validate the URL
    if audio_url:
        if not is_valid_url(audio_url):
            st.sidebar.error(
                "The provided URL is not valid. Please enter a correct URL."
            )
        elif not is_youtube_url(audio_url):
            st.sidebar.warning(
                "The URL is not a YouTube link. Ensure it points to a valid audio source."
            )

    uploaded_file = st.sidebar.file_uploader(
        "Or upload your meeting audio", type=["wav", "mp3", "mp4"]
    )

    # Main Workflow
    if audio_url or uploaded_file:
        st.markdown("## 🛠️ Processing Steps")

        # Step 1: Transcription
        if st.button("Start Transcription"):
            with st.spinner("Transcribing your audio..."):
                transcript, downloaded_file = transcribe_audio(
                    uploaded_file or audio_url
                )

                # Check transcription status
                if (
                    transcript.status == "error"
                ):  # Replace with the actual status check logic from your library
                    st.error(f"Transcription failed: {transcript.error}")
                else:
                    st.success("Transcription Complete!")

                    # Create two columns for audio player and transcript
                    col1, col2 = st.columns(
                        [1, 2]
                    )  # Adjust column width ratio as needed

                    # Display audio player in the first column
                    with col1:
                        if uploaded_file:
                            st.audio(uploaded_file, format="audio/wav")
                        elif audio_url:
                            st.video(audio_url)
                            # st.audio(downloaded_file)

                    # Display transcript in the second column
                    with col2:
                        st.text_area("📜 Transcript", transcript.text, height=300)

            # Step 2: Summarization
            st.write("### Step 2: Summarization")
            with st.spinner("Summarizing the transcript..."):
                summary = summarize_transcript(transcript.text)
            st.success("Summarization Complete!")
            st.markdown("#### 📋 Summary")
            st.markdown(summary)

            # Step 3: Action Item Extraction
            st.write("### Step 3: Action Items & Decisions")
            with st.spinner("Extracting action items..."):
                actions = extract_action_items(transcript.text)
            st.success("Action Items Extracted!")

            # Group action items by owner
            tasks_by_owner = defaultdict(list)
            for item in actions["action_items"]:
                owner = item["owner"]
                tasks_by_owner[owner].append(item)

            # Display tasks grouped by owner
            if not tasks_by_owner:
                st.info("No action items were found.")
            else:
                for owner, tasks in tasks_by_owner.items():
                    display_owner = owner if owner != "N/A" else "Unassigned"
                    for i, task in enumerate(tasks, start=1):
                        with st.expander(f"{i}. {task['task']}"):
                            st.markdown(f"**Deadline:** {task['deadline']}")
                            st.markdown(f"**Notes:** {task['notes']}")

            # # Display decisions
            # st.markdown("#### 📝 Decisions")
            # if actions["decisions"]:
            #     for decision in actions["decisions"]:
            #         st.write(f"- {decision}")
            # else:
            #     st.info("No decisions were found.")

            # Step 4: Sentiment Analysis
            st.write("### Step 4: Sentiment Analysis")
            with st.spinner("Analyzing sentiment..."):
                sentiment_results = analyze_sentiment(transcript.text)
            st.success("Sentiment Analysis Complete!")
            st.markdown("#### 🎭 Sentiment Results")
            st.write(f"**Overall Sentiment:** {sentiment_results}")

    else:
        st.info("Please provide a link or upload an audio file to proceed.")


if __name__ == "__main__":
    main()
