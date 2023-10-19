import openai
from constants import PROMPT_TEXT_CLEANING

class NoteProcessor:
    def __init__(self, note: str):
        self.note = note

    def clean_record(self):
        try:
            messages = [
                { "role" : "system", "content" : PROMPT_TEXT_CLEANING },
                { "role": "user", "content": self.note }
            ]
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            return completion.choices[0].message.content
        except Exception as error:
            print(f"Error during note cleaning: {error}")
            return ""