import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    absolute_wd = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(absolute_wd, directory))

    # Will be True or False
    valid_target_dir = os.path.commonpath([absolute_wd, target_directory]) == absolute_wd

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_directory):
        return f'Error: "{target_directory}" is not a directory'

    results: list[str] = []
    try:
        for item in os.listdir(target_directory):
            item_path = f"{target_directory}/{item}"
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            results.append(f"- {item}: file_size={file_size}, is_dir={is_dir}")
    except Exception as e:
        return f"Error: {e}"

    return "\n".join(results)

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
