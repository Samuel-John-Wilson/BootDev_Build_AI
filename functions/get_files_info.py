import os
from google import genai
from google.genai import types

def is_subdirectory(parent, child):
    parent = os.path.abspath(parent)
    child = os.path.abspath(child)
    return os.path.commonpath([parent, child]) == parent


def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
    else:
        directory = os.path.abspath(os.path.join(working_directory, directory))

    if not is_subdirectory(working_directory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
   

    try:

        dir_list = os.listdir(directory)
        output_list = []

        for file in dir_list:
            file_path = os.path.join(directory, file)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)    
            output_list.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
            

        return "\n".join(output_list)
    except Exception as e:
        return f"Error: {str(e)}"

        
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    