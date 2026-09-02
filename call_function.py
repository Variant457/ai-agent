import json
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from collections.abc import Callable

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

def call_function(tool_call, verbose: bool = False) -> dict:
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments or '{}')
    if verbose:
        print(f" - Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    func_map: dict[str, Callable[..., str]] = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if func_name not in func_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {func_name}",
        }

    func_args["working_directory"] = "./calculator"
    result = func_map[func_name](**func_args)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
