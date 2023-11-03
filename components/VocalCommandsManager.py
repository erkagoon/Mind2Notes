import openai
import copy
import json
import inspect
from constants import PROMPT_COMMANDS, FUNCTION_CALLS_COMMANDS
from utils import replace_in_dict, set_active_project, get_active_project
from components.OpenAIHandler import OpenAIHandler
from models.ProjectsDB import ProjectsDB
from models.CategoriesDB import CategoriesDB
from components.UIManager import UIManager

# Pour rafraichir les cats, nécessites l'id de projet
# main_window.refresh_categories_needed.emit(1)

# Pour rafraichir les projets
# main_window.refresh_projects_needed.emit()

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
            # print(f"Function call : {function_call}")
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
        project = self.projects_db.get(active_project)
        self.display_notification(f"Active project: {project[1]} (ID: {active_project})")

    def switch_to_project_id(self, project_id):
        self.display_notification(f"Switching to project with ID: {project_id}")
        set_active_project(project_id)

    def switch_to_project_name(self, project_name):
        project = self.projects_db.get_from_name(project_name)
        self.display_notification(f"Switching to project with name: {project_name} (ID: {project[0]})")
        set_active_project(project[0])

    def display_category_list(self, project_name=None, project_id=None):
        # If project_name is provided
        if project_name:
            #print(f"Fetching categories for project named: {project_name}")
            project = self.projects_db.get_from_name(project_name)
            project_id = project[0]
            
        # Else if project_id is provided
        elif project_id:
            pass
            #print(f"Fetching categories for project with ID: {project_id}")
            
        # Else fetch categories for the currently active project
        else:
            project_id = get_active_project()
            #print(f"Fetching categories for the currently active project: {project_id}")

        categories = self.categories_db.fetch_by_project_id(project_id)
        
        # Print the fetched categories
        self.display_notification(f"Categories: {categories}")

    def add_project(self, project_name, project_description=None):
        project_name = project_name.capitalize()
        # Check if a project with this name already exists
        existing_project = self.projects_db.get_from_name(project_name)
        if existing_project:
            self.display_notification(f"A project with the name '{project_name}' already exists.")
            return

        # Insert the new project into the database
        project_id = self.projects_db.insert(project_name, project_description)
        if project_id:
            confirmation_msg = f"Project '{project_name}' has been added with ID: {project_id}"
            if project_description:
                confirmation_msg += f" and description: '{project_description}'"
            self.display_notification(confirmation_msg)
            # self.ui_refresh_projects()
            UIManager.refresh_projects()
        else:
            self.display_notification("Failed to add the project.")

    def add_category(self, category_name, category_description=None, project_name=None, project_id=None):
        # Determine the project_id either by name or use the active project
        if project_name:
            project = self.projects_db.get_from_name(project_name)
            if project:
                project_id = project[0]
            else:
                self.display_notification(f"No project with the name '{project_name}' found. Cannot add category.")
                return
        elif not project_id:
            # Use the currently active project if no project is specified
            project_id = get_active_project()
            if not project_id:
                self.display_notification("No valid project specified and no active project found for the new category.")
                return

        # Check if a category with this name already exists within the project to avoid duplicates
        existing_categories = self.categories_db.fetch_by_project_id(project_id)
        # print(f"Existing categories: {existing_categories}")
        if any(category[1] == category_name for category in existing_categories):
            self.display_notification(f"A category with the name '{category_name}' already exists in the specified project.")
            return

        # Insert the new category into the database
        category_id = self.categories_db.insert(category_name, project_id, category_description)
        if category_id:
            message = f"Category '{category_name}' has been added under project ID: {project_id}."
            if project_name:
                message += f" (Project name: {project_name})"
            if category_description:
                message += f" (Description: {category_description})"
            self.display_notification(message)
            # self.ui_refresh_categories(project_id)
            UIManager.refresh_categories(project_id)
        else:
            self.display_notification("Failed to add the category.")

    
    # UI functions
    # def ui_refresh_projects(self):
    #     uiInstance().refresh_projects_needed.emit()

    # def ui_refresh_categories(self, project_id):
    #     uiInstance().refresh_categories_needed.emit(project_id)



    # Display notifications
    def display_notification(self, content):
        print(f"Notification : {content}")
