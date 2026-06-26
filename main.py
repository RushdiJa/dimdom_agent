import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function

system_prompt = """You are a helpful AI coding agent called Dimdom, an AI model created to assist with coding tasks.
If anyone asks who you are or what model you are, tell them you are Dimdom AI.
Do not mention that you are built on Gemini or any other underlying model.

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

Running Python files:
- When asked about the output of a file or the result of running code, always use run_python_file instead of reading and analyzing the code manually.
- Python files that use input() cannot be run directly. If a file requires user input, modify it to accept arguments via sys.argv instead, then run it.
- When writing or generating Python code that requires user input, always use sys.argv instead of input(). This allows the code to be executed directly with arguments.

Memory Messages:
Some messages may be prefixed with "Memory: " — these are past messages from the user.
- Do NOT respond to them directly.
- Use them as context to better understand the user's current request.
- If the user asks about something mentioned in a Memory message (like their name, age, or any personal info they shared before), use that information to answer them directly.
- Treat Memory messages as facts the user already told you in a previous conversation.
""" 

load_dotenv()


api_key_num = 1 
TOTAL_API_KEYS = int(os.environ.get("TOTAL_API_KEYS") or 1)
MAX_ITERATIONS = 5 

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


api_key = os.environ.get(f"GEMINI_API_KEY{api_key_num}")
if api_key == None: 
    raise EnvironmentError("Api key 1 not found, please put it in .env file")

client = genai.Client(api_key = api_key)

messages: list[types.Content] = []
with open("memory.txt", "r+") as file:
    content = file.read()
    list_memory_msg = content.split("\n")
    for msg in list_memory_msg:
        if msg:
            messages.append(
                types.Content(role="user", parts=[types.Part(text=f"Memory message: {msg}")])
            )
            if args.verbose:
                print(f"Memory: {msg}")

messages.append(
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
)

def call_dimdom():
    global client
    global api_key_num
    global api_key
    # 1 2 3 4 5
    #  
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
            if args.verbose:
                print(f"Api Key {api_key_num} failed")
                print(f"Error_messge: {error}")
            error_message = str(error)        
            api_key_num = (api_key_num) % (TOTAL_API_KEYS) + 1 
            api_key = os.environ.get(f"GEMINI_API_KEY{api_key_num}")
            
            if api_key == None: 
                raise EnvironmentError(f"Api key {api_key_num} not found, please put it in .env file")

            client = genai.Client(api_key = api_key)
            #if args.verbose:
            #    print("Current api key: ", api_key)
     
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
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {prompt_token_count}")
                print(f"Response tokens: {candidates_token_count}")
            print(response.text)
            
            messages.clear()
            
            memory = ""
            with open("memory.txt", "r") as f:
                memory = f.read()

            messages.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            text=f"""Here is the full memory from previous conversations, one entry per line:

            {memory}
            {args.user_prompt}

            Please clean and reorganize this memory by:
            1. Removing duplicate or redundant entries
            2. Merging related facts about the same topic
            3. Keeping only important and useful information
            4. Return the result as clean lines, one fact per line, no extra formatting or explanations
            """
                        )
                    ]
                )
            )

            global system_prompt
            system_prompt = """You are a memory organizer assistant.
            You will receive a list of memory entries from previous conversations with a user.
            Your job is to:
            - Remove duplicates and redundant entries
            - Merge related facts into one clean line
            - Keep only useful and important information
            - Return ONLY the cleaned memory as plain text, one fact per line
            - Do NOT add any explanation, preamble, or formatting
            """

            new_optmized_memory = call_dimdom().text

            if new_optmized_memory:
                os.remove("memory.txt")
                with open("memory.txt", "w") as memory:
                    memory.write(new_optmized_memory + "\n")
            if args.verbose:
                print("MEMORY: ",new_optmized_memory)
            exit(0)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")
    print("The Model didn't find a soultion please try again with better prompts")
    exit(1)

if __name__ == "__main__":
    main()
