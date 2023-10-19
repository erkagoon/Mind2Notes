import openai
from constants import PROMPT_COMMANDS, FUNCTION_CALLS_COMMANDS

class VocalCommandsManager:
    def __init__(self, vocal_command: str):
        self.vocal_command = vocal_command

    def execute_command(self):
        try:
            messages = [
                { "role" : "system", "content" : PROMPT_COMMANDS },
                { "role": "user", "content": self.vocal_command }
            ]
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, functions=FUNCTION_CALLS_COMMANDS)
            return response.choices[0].message.function_call if hasattr(response.choices[0].message, 'function_call') else response.choices[0].message.content
        except Exception as error:
            print(f"Error during vocal command treatment: {error}")
            return ""