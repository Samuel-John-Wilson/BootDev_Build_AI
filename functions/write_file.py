import os
from .get_files_info import is_subdirectory
from google import genai
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        relative_file_path = os.path.join(working_directory, file_path)
        target_directory = os.path.dirname(relative_file_path)
        #note that path.join will return an unchanged 2nd argument
        #if that path is absolute. So this next check is still necessary
        if not is_subdirectory(working_directory, relative_file_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        # if target directory doesn't exist, make it; if it does, pass 
        os.makedirs(target_directory, exist_ok=True)
        # open/f.write overwrites existing content or creates nonexistent files by default
        with open(relative_file_path, "w") as f:
            f.write(content)
        # note if the with block fails, python automatically jumps to the except block. 
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return (f"Error: {str(e)}")



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="""Open a file at input file path and overwrite it with input content. File path is contrained to the working directory. """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to be written to, relative to the working directory.",
            ),
            "content" : types.Schema(
                type=types.Type.STRING,
                description= "The content to be written to the file"
            )
        },
    ),
)
           
      

            

