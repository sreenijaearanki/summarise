# modules/action_extraction.py

import openai

def extract_action_items_gpt(transcript: str) -> str:
    """
    Extract action items and decisions from the transcript using OpenAI GPT.
    """
    prompt = (
        "Extract action items and decisions from this meeting transcript, "
        "listing each item with any owners and deadlines if mentioned.\n\n"
        f"Transcript:\n{transcript}"
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def extract_action_items(transcript: str, method: str) -> str:
    """
    If you have multiple approaches, unify them here.
    """
    if method == "OpenAI GPT":
        return extract_action_items_gpt(transcript)
    else:
        return "Action item extraction not implemented for this method."
