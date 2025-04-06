import assemblyai as aai
import yt_dlp
import os
from uuid import uuid4

# Initialize the transcriber
transcriber = aai.Transcriber()

# Transcription configuration
config = aai.TranscriptionConfig(speaker_labels=True)


def download_youtube_audio(youtube_url: str, output_folder: str = "audio_files") -> str:
    """
    Downloads audio from a YouTube video and saves it in the best available format.

    Args:
        youtube_url (str): The URL of the YouTube video.
        output_folder (str): The folder to save the downloaded audio file.

    Returns:
        str: The path to the downloaded audio file.
    """
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists
    unique_filename = f"{uuid4().hex}.m4a"  # Generate a unique filename
    output_path = os.path.join(output_folder, unique_filename)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"[INFO] Downloading audio from YouTube: {youtube_url}")
        ydl.download([youtube_url])

    print(f"[INFO] Audio downloaded and saved to {output_path}")
    return output_path


def transcribe_audio(input_source):
    """
    Transcribes audio using AssemblyAI's SDK.
    The input can be either a YouTube link or a local file path.

    Args:
        input_source (str): YouTube link or local file path.

    Returns:
        dict: The transcript object returned by AssemblyAI.
    """
    audio_path = None

    if isinstance(input_source, str) and (
        "youtube.com" in input_source or "youtu.be" in input_source
    ):
        # Input is a YouTube link
        print("[INFO] Detected YouTube link. Downloading audio...")
        audio_path = download_youtube_audio(input_source)

    if audio_path or input_source:
        # Transcribe the audio
        transcript = transcriber.transcribe(audio_path or input_source, config)
        return transcript, audio_path
    else:
        return None, None
