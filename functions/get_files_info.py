import os
from functions.utilities.paths import is_safe_path
from google.genai import types

def organizer(full_directory: str, file: str) -> str:
    merged_path: str = os.path.join(full_directory, file)
    size_in_bytes: int = os.path.getsize(merged_path)
    is_dir: bool = bool(os.path.isdir(merged_path))
    return f"-{file}: file_size= {size_in_bytes} bytes, is_dir={is_dir}"

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        if not is_safe_path(working_directory, directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        full_directory = os.path.join(working_directory, directory)
        
        if not os.path.isdir(full_directory): 
            return f'Error: "{directory}" is not a directory'

        list_directory = os.listdir(full_directory) # here we are taking input from outter source it's doese'nt satfsife the FP rules
        return "\n".join(map(lambda file : organizer(full_directory, file), list_directory))
    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

