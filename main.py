import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY2")
if api_key == None: 
    raise ValueError("api key not found")

client = genai.Client(api_key = api_key)
user_prompt = args.user_prompt

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

try:
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents= messages
    )
except:
    raise ConnectionError("API called limit error")

if response.usage_metadata is None:
    raise AttributeError("Something went wrong, data is missing!")

if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Respone: {response.text}")

