# modules/action_extraction.py

from openai import OpenAI
import json

# Set up OpenAI API client
client = OpenAI()

SYSTEM_PROMPT = """
You are an AI assistant helping a student review a lecture or tutorial. You will read the transcript below and identify any key tasks or next steps (i.e., "action items") the student (or speaker) suggests. You will also note any important decisions that were made during the lecture. Please follow these rules when you respond:

1. List each action item (e.g., "Complete reading assignment," "Watch additional tutorial," "Email the professor," etc.) as an object in an array called "action_items."
   - Include a short descriptive label for the task in the "task" field.
   - If an owner (or a responsible person) is explicitly mentioned, fill it under the "owner" field; otherwise, use "N/A."
   - If a specific deadline or date is mentioned, include it in the "deadline" field. Otherwise, set "deadline" to "N/A."
   - In the "notes" field, include any extra instructions or references (e.g., textbook chapters, URLs, or additional resources).

2. If the lecture mentions clear decisions (e.g., "We decided to schedule a Q&A session next week," "We chose topic X for the group project"), place them as strings in an array called "decisions."

3. Return your final output in valid JSON format enclosed in a code block (using triple backticks). For example:

{
  "action_items": [
    {
      "task": "...",
      "owner": "...",
      "deadline": "...",
      "notes": "..."
    },
    ...
  ],
  "decisions": [
    "...",
    ...
  ]
}

4. If there are no action items or decisions, return empty arrays.

Below is the transcript. Use only the details explicitly stated or clearly implied in the text. Do not invent tasks or deadlines.
"""


def extract_action_items(transcript: str):
    developer_message = {"role": "developer", "content": SYSTEM_PROMPT}
    user_message = {
        "role": "user",
        "content": transcript,
    }

    messages = [developer_message, user_message]
    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, response_format={"type": "json_object"}
    )

    # Extract the JSON from the code block
    raw_output = response.choices[0].message.content

    # Parse the JSON string
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return {"action_items": [], "decisions": []}
