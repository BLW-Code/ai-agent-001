import os
from config import *
def get_file_content(working_directory: str, file_path: str) -> str:
    absolute_wd = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_wd, file_path))

    # Will be True or False
    valid_target_dir = os.path.commonpath([absolute_wd, target_file]) == absolute_wd

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open (target_file, "r", encoding="utf-8") as file:
           content = file.read(MAX_CHARS) 
    
           # check if file was bigger than max
           if file.read(1):
               content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e}"

    return content

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets content of file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to be read, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}