import os
import subprocess
from functions.utilities.paths import is_safe_path
from google.genai import types
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        if not is_safe_path(working_directory, file_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        full_path = os.path.normpath(os.path.join(working_directory, file_path))
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if len(full_path) < 3 or full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        # abc.py 2 
        command = ["python", full_path]
        if args: command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        result_array = []
        if result.returncode != 0:
            result_array.append(f"Process exited with code {result.returncode}")

        if (not result.stdout) and (not result.stderr):
            result_array.append("No output produced")
        else:
            result_array.append(f"STDOUT: {result.stdout}")
            result_array.append(f"STDERR: {result.stderr}")
        return "\n".join(result_array)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run a python with a given args and returns the output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="a path to the file to run be sure it's .py, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                items = types.Schema(
                    type=types.Type.STRING
                ),
                description="args you want to gives the python file to take",
            ),
        },
        required=["file_path"]
    ),
)
    


