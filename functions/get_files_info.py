import os

def get_files_info(working_directory: str, directory: str = '.') -> str:
    file_data = f"Result for {"current" if directory == '.' else f"'{directory}'"} directory:\n"
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        if not os.path.isdir(target_dir):
            return file_data + f'    Error: "{directory}" is not a directory\n'
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
    except Exception as e:
        return file_data + f"    Error: {e}\n"
    
    if not valid_target_dir:
        return file_data + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory\n'

    try:
        for file in os.listdir(target_dir):
            file_path = '/'.join([target_dir, file])
            file_data += f"  - {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}\n"
        return file_data
    except Exception as e:
        return file_data + f"    Error: {e}\n"
