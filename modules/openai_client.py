from .helpers import *
from .config import get_prompt
from .calculator import Calculator
import openai
import os


class OpenAI:
    def __init__(self, model: str):
        self.model = model
        self.tools = get_tools()
        self.tool_choice = {"type": "function", "function": {"name": "calculate"}}
        self.sys_message = {"role": "system", "content": get_prompt(prompt_type="client")}
        self.history = [self.sys_message]
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def solve(self, input_message: str):
        self.plan(input_message)
        self.compute()
        self.stream()

    def plan(self, input_message: str):
        """Takes problem as input then returns the client model's plan to solve the problem."""
        self.history.append({"role": "user", "content": input_message})
        completion = self.get_completion()
        message = self.get_message(completion)
        self.history.append(message)

    def compute(self):
        self.history[0] = {"role": "system", "content": get_prompt(prompt_type="calc")}
        completion = self.get_completion(tool_choice=self.tool_choice)
        message = self.get_message(completion)
        self.history.append(message)
        self.call_tool(completion)

    def stream(self):
        """Streams the final response from the client"""
        self.history[0] = {"role": "system", "content": get_prompt(prompt_type="conc")}
        completion = self.get_completion(stream=True)

        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)

        self.history = [self.sys_message]

    def get_completion(self, tool_choice: str = "none", stream: bool = False):
        """Retrieves the client message metadata"""
        completion = openai.chat.completions.create(model=self.model, messages=self.history, tools=self.tools, tool_choice=tool_choice, stream=stream)
        return completion

    def get_message(self, completion):
        "Parses the message metadata into a python dict"
        return json.loads(completion.choices[0].message.model_dump_json())
        
    def get_args(self, completion):
        """Retrieves the input arguments identified by the client and to be used in the function call"""
        return [json.loads(completion.tool_calls[i].function.arguments) for i in range(len(completion.tool_calls))]

    def call_tool(self, completion):
        "Aggregates all tool messages into a list"
        for i in range(len(self.history)):
            if "tool_calls" in self.history[i].keys() and self.history[i]["tool_calls"]:
                for j in range(len(self.history[i]["tool_calls"])):
                    self.args = self.get_args(completion.choices[0].message)
                    message = {
                        "role": "tool",
                        "tool_call_id": self.history[i]["tool_calls"][j]["id"],
                        "name": self.history[i]["tool_calls"][j]["function"]["name"],
                        "content": str(Calculator(self.args[0]["equation"]).calculate())
                    }
                    self.history.append(message)

