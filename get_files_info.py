import os 

def is_subdirectory(parent, child):
    parent = os.path.abspath(parent)
    child = os.path.abspath(child)
    return os.path.commonpath([child]) == os.path.commonpath([child, parent])


def get_files_info(working_directory, directory=None):
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    if not is_subdirectory(working_directory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    