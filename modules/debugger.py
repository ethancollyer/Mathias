import ollama
import openai
import os
from .helpers import *

"""
LLM debugger that supports either ollama or openai to ingest an error message and the
response from the client llm, then attempts to fix the error by editing the json object.
"""


class Debugger:
    def __init__(self, provider: str = "ollama", model: str = "deepseek-coder-v2:16b", sys_message: str = load_json("data\\sys_messages.json")["debugger_message"]):
        self.provider = provider.lower()
        self.model = model
        self.sys_message = {
            "role": "system",
            "content": sys_message
        }
        self.history = [self.sys_message]

        if provider not in ["ollama", "openai"]:
            raise Exception(f"Selected provider \"{provider}\" is not supported. Pick either \"ollama\" or \"openai\".")
        elif provider == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")

    def append_history(self, input_message: str, role: str = 'user'):
        """
        Adds new input_message and the role to self.history
        """
        message = {
            "role": role,
            "content": input_message
        }
        self.history.append(message)

    def debug(self, error_message: str, client_message: str):
        message = f"Solve the following error:\n\"{error_message}\"\n\nBy editing the following JSON:\n\"{client_message}\""
        self.append_history(input_message=message)

        if self.provider == "ollama":
            response = ollama.chat(model=self.model, messages=self.history)
            response = response['message']['content']

        elif self.provider == "openai":
            response = openai.chat.completions.create(model=self.model, messages=self.history)
            response = response.choices[0].message.content

        return response[response.find("{"):response.rfind("}") + 1]


"""
error_msg = "json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes:  line 1 column 433 (char 432)"
client_msg = "{\"problem\": \"Anna has 12 apples, and she gives 4 apples to Ben. How many apples does Anna have?\", \"steps\": [{\"step\": 1, \"description\": \"Let x represent the number of apples Anna has initially.\", \"equation\": \"x = 12\"}, {\"step\": 2, \"description\": \"Let y represent the number of apples Ben has after receiving apples from Anna.\", \"equation\": \"y = 4\"}], \"solution\": {\"target_variable\": \"z\", \"variable_definitions\": {\"x\": \"12\", \"y\": \"4\",}, \"proposed_equation\": \"z = x - y\"}}'''\n\nExample Output:\n->'''{\"problem\": \"Anna has 12 apples, and she gives 4 apples to Ben. How many apples does Anna have?\", \"steps\": [{\"step\": 1, \"description\": \"Let x represent the number of apples Anna has initially.\", \"equation\": \"x = 12\"}, {\"step\": 2, \"description\": \"Let y represent the number of apples Ben has after receiving apples from Anna.\", \"equation\": \"y = 4\"}], \"solution\": {\"target_variable\": \"z\", \"variable_definitions\": {\"x\": \"12\", \"y\": \"4\"}, \"proposed_equation\": \"z = x - y\"}}"

debugger = Debugger()
response = debugger.debug(client_message=client_msg, error_message=error_msg)

print(response)
"""

