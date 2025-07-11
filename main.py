import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info, get_files_info, is_subdirectory
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
system_prompt = """You are a helpful AI coding agent. When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. 
Only reply with clarifying questions if and only if no functions have been provided to you to fulfill the request. Ensure all goals specified in the prompt are accoumpished within your function call plan 
                """

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file]
)

def main():
    if len(sys.argv)<2:
        print("Error: Input prompt not provided") # Exit if no prompt!
        return
    verbose_flag = "--verbose" in sys.argv

    
    user_prompt = sys.argv[1] # Extract user prompt from command line input 
    # Create messages list 
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])] 
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)
    
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            call = call_function(function_call_part, verbose_flag)
            if not call.parts[0].function_response.response:
                raise Exception("Error: Invalid function response")
            else:
                if verbose_flag:
                    print(f"-> {call.parts[0].function_response.response}")
    else:
        print(response.text)
    if verbose_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__=="__main__":
    main()

