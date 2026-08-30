import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory'
        
        # Ensures all parent directories exist
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
