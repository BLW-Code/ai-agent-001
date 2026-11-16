import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    absolute_wd = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_wd, file_path))
    print(target_file)
    # Will be True or False
    valid_target_dir = os.path.commonpath([absolute_wd, target_file]) == absolute_wd

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        parent_dirs = os.path.dirname(target_file)
        os.makedirs(parent_dirs, exist_ok=True)
        with open (target_file, "w", encoding="utf-8") as file:
           file.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to file in a specified directory relative to the working directory, replacing the entire contents of the file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to be written to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "New content to write to the file, replacing all existing content"
                }
            },
        },
    },
}