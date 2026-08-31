import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args is not None:
            command.extend(args)

        process: CompletedProcess = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output = ""
        if process.returncode != 0:
            output += f"Process exited with code {process.returncode}\n"
        if process.stdout == "" and process.stderr == "":
            output += "No output produced\n"
        if process.stdout != "":
            output += f"STDOUT: {process.stdout}\n"
        if process.stderr != "":
            output += f"STDERR: {process.stderr}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
