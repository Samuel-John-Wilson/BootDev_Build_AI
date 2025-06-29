import os 

def is_subdirectory(parent, child):
    parent = os.path.abspath(parent)
    child = os.path.abspath(child)
    return os.path.commonpath([parent, child]) == parent


def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    if not is_subdirectory(working_directory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


    
    dir_list = os.listdir(directory)
    output_list = []

    for file in dir_list:
        file_path = os.path.join(directory, file)
        is_dir = os.path.isdir(file_path)
        if not is_dir and os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            output_list.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        elif is_dir:
            output_list.append(f"- {file}: is_dir={is_dir}")
        else:
             output_list.append(f"- {file}: unrecognized entry")

    return output_list
        

    