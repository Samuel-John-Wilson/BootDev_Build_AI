import os
from .get_files_info import is_subdirectory



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



        

            

