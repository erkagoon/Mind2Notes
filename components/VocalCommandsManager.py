import openai
import copy
from constants import PROMPT_COMMANDS, FUNCTION_CALLS_COMMANDS
from utils import replace_in_dict
from components.OpenAIHandler import OpenAIHandler

class VocalCommandsManager:
    def __init__(self, vocal_command: str):
        self.vocal_command = vocal_command

    def execute_command(self, projects_list: list = []):
        try:
            commands = copy.deepcopy(FUNCTION_CALLS_COMMANDS)
            projects_list = ["Mind2Notes", "Polarigon", "WP AI Trainer", "Création musique", "À faire"]
            projects_list_quoted = ["'"+project+"'" for project in projects_list]
            projects_str = ", ".join(projects_list_quoted)
            commands = replace_in_dict(commands, "<projects_string>", projects_str)
            commands = replace_in_dict(commands, "<list:projects_list>", projects_list)
            functions_list = list(commands.values())
            messages = [
                { "role" : "system", "content" : PROMPT_COMMANDS },
                { "role": "user", "content": self.vocal_command }
            ]
            openai_handler = OpenAIHandler()
            response = openai_handler.post_chat(model="gpt-3.5-turbo", messages=messages, functions_list=functions_list)
            return response
        except Exception as error:
            print(f"Error during vocal command treatment: {error}")
            return ""