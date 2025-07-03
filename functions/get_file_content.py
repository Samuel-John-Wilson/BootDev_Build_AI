import os 
from .get_files_info import is_subdirectory 





def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    check_path = os.path.join(working_directory, file_path)
    try:
        if not os.path.exists(check_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        else:
            file_path = check_path
        # ensure file_path is within working directory, and points to a file
        if not is_subdirectory(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        # set max character value, return string of file content up to max-character value. If string exceeds 10000, append truncation message
    
        max_char = 10000
        with open(file_path, 'r') as f:
            limited_file_content_string = f.read(max_char)
            if not f.read(1):
                return limited_file_content_string
            else:
                return f'{limited_file_content_string} [...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {str(e)}"




    

