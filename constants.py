OPENAI_CHAT_MODEL = "gpt-3.5-turbo"
OPENAI_AUDIO_MODEL = "whisper-1"

# Prompt for translating natural language input into software commands.
PROMPT_COMMANDS = """
Your goal is to translate natural language input strings into predefined software commands. 
Your primary role is to trigger specific actions within the software, not to engage in conversational interactions. 
If a response is necessary, use a concise, system-like tone. Do not attempt to engage in casual conversation or provide explanations beyond the immediate command requirements.
"""

# Prompt for cleaning the input text generated from speech to text analysis.
PROMPT_TEXT_CLEANING = """
Your goal is to clean an input text, generated from a speech to text analysis. 
Your primary task is to preserve the original wording.
You have to write the whole modified text back, without adding any preceding or trailing comments.
Modify only the parts that are obviously wrong, make the minimal possible modifications to make correct sentences, but keep everything else exactly as in the input text.
Introduce punctuation if necessary, but under no circumstances should you modify the actual words, only punctuation marks if you feel some are missing.
"""

# Prompt for categorizing incoming textual notes.
PROMPT_NOTE_CATEGORIZATION = """
Your role is to categorize incoming textual notes within the existing notes of a project. 
You can choose to put the new note in an existing category if one is relevant, or to create a new category if none fits.
You have to prioritize choosing an existing category, the goal is to keep the number of categories small.
Only use the provided actions to make this choice, don't engage conversation or provide explanations.
Please make an estimation of how relevant the category is to the input note. If the relevancy is too small (less than 0.6), consider creating a new category instead.
Existing categories: 
- NOM : Description
- NOM : Description
...
"""


FUNCTION_CALLS_COMMANDS = {
    "get_currently_active_project": {
        "name": "get_currently_active_project",
        "description": "Get the currently active project.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    "switch_to_project_id": {
        "name": "switch_to_project_id",
        "description": "Switch to project with given ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "integer",
                    "description": "The project ID",
                },
            },
            "required": ["project_id"],
        },
    },
    "switch_to_project_name": {
        "name": "switch_to_project_name",
        "description": "Switch to project with given name. Here's the list of existing projects, choose amongst those names : <projects_string>. If the input seems close to one of the names specified, you have to modify it to stick to return the exact project name. Guess the right project based on input words pronunciation and closeness to the real existing project names",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "The project name",
                    "enum": "<list:projects_list>",
                },
            },
            "required": ["project_name"],
        },
    },
    "add_project": {
        "name": "add_project",
        "description": "Add a new project with given name, an optional description can be specified.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "The project name",
                },
                "project_description": {
                    "type": "string",
                    "description": "The project description",
                },
            },
            "required": ["category_name"],
        },
    },
    "add_category": {
        "name": "add_category",
        "description": "Add a new category with given name, an optional description can be specified. A project can be specified too, but it's optionnal.",
        "parameters": {
            "type": "object",
            "properties": {
                "category_name": {
                    "type": "string",
                    "description": "The category name",
                },
                "category_description": {
                    "type": "string",
                    "description": "The category description",
                },
                "project_name": {
                    "type": "string",
                    "description": "The project name",
                },
                "project_id": {
                    "type": "integer",
                    "description": "The project ID",
                },
            },
            "required": ["category_name"],
        },
    },
    "display_category_list": {
        "name": "display_category_list",
        "description": "Return all the categories. If a project name or ID is specified, return categories from this project, if not, return all categories from the current project.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "The project name",
                },
                "project_id": {
                    "type": "integer",
                    "description": "The project ID",
                },
            },
        },
    },
}

FUNCTION_CALLS_CATEGORIZE = [
    {
        "name": "put_in_existing_category",
        "description": "Put the input textual note in an existing category. Estimate how relevant the category is for this note. The existing categories are: <categories>.",
        "parameters": {
            "type": "object",
            "properties": {
                "category_name": {
                    "type": "string",
                    "description": "The existing category name",
                },
                "relevancy": {
                    "type": "string",
                    "description": "Estimation of how relevant the category is for this note, between 0 (not relevant) and 1 (very relevant)",
                },
            },
            "required": ["category_name", "relevancy"],
        },
    },
    {
        "name": "create_new_category",
        "description": "Put the input textual note in a new category you'll create. Do this only if no existing category is relevant. Choose a name for the new category. If it is relevant, you can choose a description for the category too.",
        "parameters": {
            "type": "object",
            "properties": {
                "category_name": {
                    "type": "string",
                    "description": "The name of the new category to create",
                },
                "category_description": {
                    "type": "string",
                    "description": "The optional description of the new category",
                },
            },
            "required": ["category_name"],
        },
    },
]
