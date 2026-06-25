import os 
# from utilities.paths import is_safe_path
from functions.utilities.paths import is_safe_path
from google.genai import types
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        MAX_CHARS = 10000 # const 
        full_path = os.path.join(working_directory, file_path)
        if not is_safe_path(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        file = open(full_path)
        content = file.read(MAX_CHARS)
        if file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as E:
        return f"Error: {E}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gives you the file content at the directory you gave him",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="a path to the file you need it's content, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)

