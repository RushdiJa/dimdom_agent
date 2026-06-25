import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file 

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""





parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY4")
if api_key == None: 
    raise ValueError("api key not found")

client = genai.Client(api_key = api_key)
user_prompt = args.user_prompt

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature = 0)        
    )
except:
    raise ConnectionError("API called limit error")

if response.usage_metadata is None:
    raise AttributeError("Something went wrong, data is missing!")

if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        kargs = function_call.args 
        name = function_call.name
        func = globals()[name] if name else None
        #from functions.get_files_info import get_files_info
        #from functions.get_file_content import get_file_content
        #from functions.run_python_file import run_python_file
        #from functions.write_file import write_file

        #if name == "get_files_info":
        #    func = get_files_info
        #elif name == "get_file_content":
        #    func = get_file_content
        #elif name == "run_python_file":
        #    name = run_python_file
        #elif name == "write_file":
        #    func = write_file
        # 
        if func and kargs:
            print(func(".", **kargs))
        
else:
    print(f"Respone: {response.text}")

