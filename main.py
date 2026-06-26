import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function


system_prompt = """You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

When fixing code, follow this process:
1. Inspect the project files to understand the structure.
2. Read the relevant source files before making changes.
3. Identify the root cause of the bug.
4. Modify only the files needed to fix the issue.
5. Run the relevant Python file or tests to verify the fix.
6. Continue using tools until the problem is fixed and verified.
7. When the fix is complete, provide a concise final response explaining what was changed and how it was verified.

Do not guess blindly. Always inspect files before editing them.
"""


load_dotenv()


api_key_num = 1
TOTAL_API_KEYS = 4
MAX_ITERATIONS = 10 

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


api_key = os.environ.get("GEMINI_API_KEY1")
if api_key == None: 
    raise EnvironmentError("Api key 1 not found, please put it in .env file")

client = genai.Client(api_key = api_key)
user_prompt = args.user_prompt

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]


def call_dimdom():
    global client
    global api_key_num
    for iteration in range(TOTAL_API_KEYS):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature = 0)        
            )
            if response.usage_metadata is None: raise ConnectionError("meta data is null")
            y = response.usage_metadata.prompt_token_count # if meta_data is null
            return response 
        except Exception as error:
            error_message = str(error)        
            api_key_num = (api_key_num) % (TOTAL_API_KEYS) + 1 
            api_key = os.environ.get(f"GEMINI_API_KEY{api_key_num}")
            
            if api_key == None: 
                raise EnvironmentError(f"Api key {api_key_num} not found, please put it in .env file")

            client = genai.Client(api_key = api_key)
            
    raise ConnectionError("All API keys hits the limit plesae try later Or there is a connectionError")
    

def main():
    prompt_token_count = 0 
    candidates_token_count = 0
    for iter in range(MAX_ITERATIONS):
        response = call_dimdom()
        if response.usage_metadata is None:
            raise Exception("Impossible to happen")
        
        prompt_token_count += response.usage_metadata.prompt_token_count or 0 
        candidates_token_count += response.usage_metadata.candidates_token_count or 0
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content: 
                    messages.append(candidate.content)
        
        if response.function_calls:
            list_functions_result = []
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, verbose=args.verbose)        
                if ((not function_call_result.parts)
                    or (function_call_result.parts[0].function_response is None)
                        or (function_call_result.parts[0].function_response.response is None)): raise Exception("function_calls_result")
                if args.verbose: 
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                    list_functions_result.append(function_call_result.parts[0])
                for fun in list_functions_result:
                    try:
                        messages.append(types.Content(role="function",
                        parts=[types.Part.from_function_response(name=fun.function_response.name,response=fun.function_response.response)]))
                    except:
                        pass

        else:
            if args.verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {prompt_token_count}")
                print(f"Response tokens: {candidates_token_count}")
            print(response.text)
            exit(0)

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")
    print("The Model didn't find a soultion please try again with better prompts")
    exit(1)

if __name__ == "__main__":
    main()
