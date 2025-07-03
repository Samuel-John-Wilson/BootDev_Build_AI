import os
import subprocess
from .get_files_info import is_subdirectory


def run_python_file(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        relative_file_path = os.path.join(working_directory, file_path)
        #note that path.join will return an unchanged 2nd argument
        #if that path is absolute. So this next check is still necessary
        if not is_subdirectory(working_directory, relative_file_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(relative_file_path):
            return f'Error: File "{file_path}" not found.'
        # os.path. 'split extention' - ensure file is a python file (returns tuple [0]root [1]ext)
        if os.path.splitext(relative_file_path)[1] != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            ["uv", "run", file_path],
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
            )
        # compile output in list to be returned by function    
        output_parts = []
        if result.stdout:
            output_parts.append(f"STDOUT: {result.stdout.strip()}")
        if result.stderr:
            output_parts.append(f"STDERR: {result.stderr.strip()}")

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."
        else:
            return "\n".join(output_parts)

    except subprocess.TimeoutExpired as e:
        # The assignment asks for a specific error string format for exceptions
        return f"Error: executing Python file: {e}"
    except Exception as e:
        # The assignment asks for a specific error string format for exceptions
        return f"Error: executing Python file: {e}"
    

        
