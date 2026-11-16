#third party imports
import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI

#local imports
from call_functions import available_functions, call_function
from prompts import system_prompt
from config import AI_TEMPERATURE
def main():
    #command line args
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    
    # loading environment variables
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Open Router API key not found. Place key in .env file as OPENROUTER_API_KEY=\"[key]\"")

    #create OpenAi client with openrouter
    client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key=api_key
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages, # type:ignore
        temperature=AI_TEMPERATURE,
        tools=available_functions, #type:ignore
    )
    usage = response.usage
    prompt_tokens = usage.prompt_tokens # type:ignore
    response_tokens = usage.completion_tokens # type:ignore
    message = response.choices[0].message
    message_content = message.content
    tool_calls = message.tool_calls

    if usage:
        if args.verbose:
            print(f"User prompt: {messages[0]["content"]}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        if tool_calls:
            for tool_call in tool_calls:
                tool_message = call_function(tool_call)
                if not tool_message.get("content"):
                    raise Exception("Error: Tool call did not contain a result")

                if args.verbose:
                    print(f"-> {tool_message['content']}")
        else:
            print("Response:")
            print(message_content)
    else:
        raise RuntimeError("Usage object empty. API call failed.")


if __name__ == "__main__":
    main()
