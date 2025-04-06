# SummarAIze: Your AI-Powered Meeting Assistant

SummarAIze is a web-based application designed to help users transcribe, summarize, and analyze audio content. Whether you're a student, professional, or lifelong learner, SummarAIze simplifies the process of extracting key insights from meetings, lectures, or any audio source.

## Features
- **Audio Transcription**: Convert audio, video files or YouTube links into text using advanced transcription models.
- **Summarization**: Generate concise summaries of the transcribed content for quick understanding.
- **Action Item Extraction**: Identify actionable tasks and decisions from the transcript.
- **Sentiment Analysis**: Analyze the tone and sentiment of the discussion.
- **YouTube Integration**: Embed YouTube videos alongside transcripts.

## How to Use
1. **Input Options**:
   - Upload an audio or video file (`.wav`, `.mp3`, `.mp4`).
   - Provide a YouTube video link.
2. **Processing Steps**:
   - Click "Start Transcription" to transcribe the audio.
   - View the transcript and audio/video side by side.
   - Summarize the transcript to extract key points.
   - Extract action items and decisions.
   - Analyze the sentiment of the discussion.
3. **Output**:
   - View and download the transcript, summary, and action items.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sreenijaearanki/summarise.git
   cd summarise
2. Create a secrets.toml file in the `./streamlit/` directory:
    ```bash
    mkdir -p ./streamlit
    touch ./streamlit/secrets.toml
3. Add the following content to `secrets.toml`:
    ```bash
    ASSEMBLYAI_API_KEY = "YOUR_ASSEMBLYAI_API_KEY"
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the application
    ```bash
    streamlit run app.py
    ```

## Future Enhancements
- Real-time transcript scrolling synchronized with YouTube videos.
- Support for additional audio formats and languages.
- Enhanced UI/UX for better user experience.

## Acknowledgments
Built using `Streamlit`, `AssemblyAI`, and `OpenAI`.
Inspired by the need for efficient tutorial and lecture summarization tools.