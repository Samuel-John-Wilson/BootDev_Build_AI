import os 
from .get_files_info import is_subdirectory 
from google import genai
from google.genai import types




def get_file_content(working_directory, file_path):
    
    working_directory = os.path.abspath(working_directory)
    relative_file_path = os.path.join(working_directory, file_path)
    try:
        # ensure file path is within working directory, and points to a file
        if not is_subdirectory(working_directory, relative_file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(relative_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        # set max character value, return string of file content up to max-character value. If string exceeds 10000, append truncation message
    
        max_char = 10000
        with open(relative_file_path, 'r') as f:
            limited_file_content_string = f.read(max_char)
            if not f.read(1):
                return limited_file_content_string
            else:
                return f'{limited_file_content_string} [...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {str(e)}"



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file as a string, constrained to 10000 characters. The file must be within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be read, relative to the working directory."
            ),
        },
    ),
)
    