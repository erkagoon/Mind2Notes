import openai
import copy
import json
from constants import PROMPT_COMMANDS, FUNCTION_CALLS_COMMANDS
from utils import replace_in_dict, set_active_project, get_active_project
from components.OpenAIHandler import OpenAIHandler
from models.ProjectsDB import ProjectsDB
from models.CategoriesDB import CategoriesDB

class VocalCommandsManager:
    def __init__(self, vocal_command: str):
        self.vocal_command = vocal_command
        self.projects_db = ProjectsDB('projectsAndCats.db')
        self.categories_db = CategoriesDB('projectsAndCats.db')

    def execute_command(self, projects_list: list = []):
        try:
            commands = copy.deepcopy(FUNCTION_CALLS_COMMANDS)
            
            projects = self.projects_db.fetch_all()
            projects_list = [project[1] for project in projects]
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

            # Check for function_call and process it
            function_call = response.get('message', {}).get('function_call', {})
            print(f"Function call : {function_call}")
            if function_call:
                function_name = function_call.get('name')
                function_args = json.loads(function_call.get('arguments', '{}'))
                if function_name and hasattr(self, function_name):
                    getattr(self, function_name)(**function_args)

            # Check for content and display notification
            content = response.get('message', {}).get('content')
            if content:
                self.display_notification(content)

            return response
        except Exception as error:
            print(f"Error during vocal command treatment: {error}")
            return ""

    # System functions
    def get_currently_active_project(self):
        active_project = get_active_project()
        print(f"Active project: {active_project}")

    def switch_to_project_id(self, project_id):
        print(f"Switching to project with ID: {project_id}")
        set_active_project(project_id)

    def switch_to_project_name(self, project_name):
        print(f"Switching to project with name: {project_name}")
        project = self.projects_db.get_from_name(project_name)
        print(f"ID: {project}")
        set_active_project(project[0])

    def display_category_list(self, project_name=None, project_id=None):
        # If project_name is provided
        if project_name:
            print(f"Fetching categories for project named: {project_name}")
            project = self.projects_db.get_from_name(project_name)
            project_id = project[0]
            
        # Else if project_id is provided
        elif project_id:
            print(f"Fetching categories for project with ID: {project_id}")
            
        # Else fetch categories for the currently active project
        else:
            project_id = get_active_project()
            print(f"Fetching categories for the currently active project: {project_id}")

        categories = self.categories_db.fetch_by_project_id(project_id)
        
        # Print the fetched categories
        print(f"Categories: {categories}")


    # Display notifications
    def display_notification(self, content):
        print(f"Notification: {content}")
