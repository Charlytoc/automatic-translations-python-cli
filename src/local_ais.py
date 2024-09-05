from openai import OpenAI
from .utils import print_colored


def create_completion_ollama(system_prompt, prompt, stream=False):
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="llama3.1")
    response = client.chat.completions.create(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        max_tokens=3000,
        stream=stream,
    )
    if not stream:
        return response.choices[0].message.content

    _entire_response = ""

    for chunk in response:
        print_colored(chunk.choices[0].delta.content, "yellow")
        _entire_response += chunk.choices[0].delta.content
    return _entire_response
