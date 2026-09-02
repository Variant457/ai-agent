import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key is missing")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("API Request Failed")
    message = response.choices[0].message
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")
        result_msg = call_function(tool_call)
        if result_msg["content"] == "":
            raise Exception(f'Error: Function call "{func_name}({func_args})" did not return anything')
        if args.verbose:
            print(f"-> {result_msg['content']}")

    if args.verbose:
        print(
            f'''
            User prompt: {args.user_prompt}\n
            Prompt tokens: {response.usage.prompt_tokens}\n
            Response tokens: {response.usage.completion_tokens}
            '''
        )
    print(message.content)

if __name__ == "__main__":
    main()
