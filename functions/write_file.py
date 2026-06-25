import os 
from functions.utilities.paths import is_safe_path
from google.genai import types
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        if not is_safe_path(working_directory, file_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        full_path = os.path.normpath( os.path.join(working_directory, file_path) )


        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        
        if not os.path.isfile(full_path):
            os.makedirs(os.path.normpath(os.path.join(full_path, "..")), exist_ok=True)
    
        with open(full_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as E:
        return f"Error: {E}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="create and write the content in the file_path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, 
                description="a path to the file to run be sure it's, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="The content you want to put in the file",      
            ),
        },
        required=["file_path", "content"]
    ),
)

