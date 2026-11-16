import os
import subprocess
from config import *

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    absolute_wd = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_wd, file_path))
    print(target_file)
    # Will be True or False
    valid_target_dir = os.path.commonpath([absolute_wd, target_file]) == absolute_wd

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    process_string = ""
    try:
        root, ext = os.path.splitext(target_file)
    
        if ext != ".py":
            return f'Error: "{file_path}" is not a Python file'
    
        command = ["python", target_file]
    
        if args:
            command.extend(args)
        
        process = subprocess.run(command, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT)
    
        if process.returncode != 0:
            process_string += f"Processexited with code {process.returncode}"
    
        if not process.stdout and not process.stderr:
            process_string += "\nNo output produced"
        else:
            if process.stdout:
                process_string += f"\nSTDOUT: {process.stdout}"
    
            if process.stderr:
                process_string += f"\nSTDERR: {process.stderr}"
    except Exception as e:
        print(f"Error: {e}")

    return process_string

schema_run_python_file= {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes python file in a specified directory relative to the working directory, providing the result of running the file (exit code, stdout, stderr if present)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the python file to execute, relative to the working directory (default is the working directory itself)",
                },
                "args":{
                    "type": "array of strings",
                    "description": "Optional array of arguments to pass into executable, defaults to None"
                }
            },
        },
    },
}