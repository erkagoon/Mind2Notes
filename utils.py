import json
import re

def replace_in_dict(data, search, replace):
    dict_str = json.dumps(data)

    if isinstance(replace, list):
        replace = json.dumps(replace)
        #print("REPLACE LIST TO STRING : ", replace)
        pattern = r'\"(' + re.escape(search) + r')\"'
        dict_str = re.sub(pattern, r'\1', dict_str)
        #print("QUOTES REMOVED AROUND LIST : ", dict_str)
    
    dict_str = dict_str.replace(search, replace)
    #print("NEW DICT STR : ", dict_str)
    dict_json = json.loads(dict_str)
    return dict_json

def clean_json(str_data):
    str_data = re.sub(r',\s*([\]}])', r'\1', str_data)  # Remove trailing commas
    str_data = re.sub(r'}\s*{', "},\n{", str_data)  # Check that there is "," between each object
    str_data = re.sub(r'}[^}]*$', '}', str_data)  # Remove everything after last } in case of incomplete JSON
    str_data = re.sub(r'\\(?=")', '', str_data)  # Remove backslashes before double quotes

    # Only add closing bracket if there's an opening bracket
    if '[' in str_data and ']' not in str_data:
        str_data += "\n]"
    
    return str_data


active_project = None
def set_active_project(project_id):
    global active_project
    active_project = project_id

def get_active_project():
    return active_project
