from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info, get_files_info, is_subdirectory
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_map = {"get_files_info" : get_files_info, "get_file_content" : get_file_content, "run_python_file" : run_python_file, "write_file" : write_file}

    arguments_map = {"working_directory" : "./calculator", **function_call_part.args}

    if not function_call_part.name in function_map:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    else:
        function = function_map[function_call_part.name]
        function_result = function(**arguments_map)
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
        )
    ],
)

    