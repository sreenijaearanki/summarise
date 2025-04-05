# modules/transcription.py

import whisper
import requests
from pydub import AudioSegment
import os

# Load a single Whisper model at import time
# (You could load multiple if you want "tiny", "base", "large" options.)
whisper_model = whisper.load_model("base")  # or "small", "medium", "large", etc.

def download_audio_from_link(url: str, output_path: str = "temp_audio_input"):
    """
    Downloads audio from a given URL and saves it locally as 'temp_audio_input'.
    Raises an exception if the download fails.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download audio from {url}")
    with open(output_path, "wb") as f:
        f.write(response.content)

# def transcribe_audio_whisper_local(
#     audio_path: str,
#     start_time: float = 0.0,
#     end_time: float = None
# ) -> str:
#     """
#     Transcribe audio using local Whisper, allowing partial slicing via start_time and end_time (in seconds).
#     """
#     # Load entire audio with pydub
#     audio = AudioSegment.from_file(audio_path)
#     duration_sec = len(audio) / 1000.0

#     # Adjust end_time if not provided or out of range
#     if end_time is None or end_time > duration_sec:
#         end_time = duration_sec

#     # pydub slicing uses milliseconds
#     start_ms = int(start_time * 1000)
#     end_ms = int(end_time * 1000)

#     # Slice the audio
#     sliced_audio = audio[start_ms:end_ms]
#     temp_sliced_path = "temp_slice.wav"
#     sliced_audio.export(temp_sliced_path, format="wav")

#     # Transcribe the sliced audio
#     result = whisper_model.transcribe(temp_sliced_path)
#     return result["text"]

def transcribe_audio_whisper_local(audio_path: str, start_time: float = 0.0, end_time: float = None) -> str:
    from pydub import AudioSegment

    audio = AudioSegment.from_file(audio_path)
    duration_sec = len(audio) / 1000.0

    if end_time is None or end_time > duration_sec:
        end_time = duration_sec

    sliced_audio = audio[int(start_time * 1000):int(end_time * 1000)]
    temp_sliced_path = "temp_slice.wav"
    sliced_audio.export(temp_sliced_path, format="wav")

    # 🪵 Log step
    print(f"[INFO] Transcribing audio from {start_time}s to {end_time}s ({temp_sliced_path})")

    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(temp_sliced_path)

    print("[DEBUG] Whisper Result:", result)  # Log full output

    return result.get("text", "")  # safer way to access transcript




def transcribe_audio_whisper_api(
    audio_path: str,
    start_time: float = 0.0,
    end_time: float = None
) -> str:
    """
    Placeholder for an external Whisper API or any other cloud-based STT service.
    You can slice the audio locally first, then upload it to the API.
    """
    # For now, just returning a mock string
    return "Transcribed text from external API (placeholder)."

def transcribe_audio(
    audio_path: str,
    method: str,
    start_time: float = 0.0,
    end_time: float = None
) -> str:
    """
    Dispatcher function to choose which transcription method to use.
    """
    if method == "Local Whisper":
        return transcribe_audio_whisper_local(audio_path, start_time, end_time)
    elif method == "API Whisper":
        return transcribe_audio_whisper_api(audio_path, start_time, end_time)
    else:
        return "No valid transcription method selected."
