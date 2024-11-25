from .helpers import *
from .config import get_prompt
from .calculator import Calculator
import ollama
import json


class Ollama:
    def __init__(self, model: str):
        self.model = model
        self.tools = get_tools()
        self.sys_message = {"role": "system", "content": get_prompt(prompt_type="client")}
        self.history = [self.sys_message]

    def solve(self, input_message):
        self.plan(input_message=input_message)
        self.compute()
        print("STREAMING:")
        self.stream()

    def plan(self, input_message):
        """Takes problem as input then returns the client model's plan to solve the problem."""
        self.history.append({"role": "user", "content": input_message})
        completion = self.get_completion()
        message = self.get_message(completion)
        message["role"] = "user"
        message["content"] += f"\n\nUse the above information to solve for the following problem:\n{input_message}"
        self.history[-1] = message

    def compute(self):
        self.history[0] = {"role": "system", "content": get_prompt(prompt_type="calc")}
        completion = self.get_completion(tools=get_tools())
        message = self.get_message(completion)
        self.history.append(message)
        self.call_tool()

    def stream(self):
        """Streams the final response from the client"""
        self.history[0] = {"role": "system", "content": get_prompt(prompt_type="conc")}
        self.history.append({"role": "user", "content": "Walk me through how we solved the problem."})
        completion = self.get_completion(stream=True)
        
        for chunk in completion:
            content = chunk['message']['content']
            if content:
                print(content, end="", flush=True)

        self.history = [self.sys_message]

    def get_completion(self, tools: str = None, stream: bool = False):
        completion = ollama.chat(
            model=self.model,
            messages=self.history,
            tools=tools,
            stream=stream
        )

        return completion
    
    def get_message(self, completion):
        return json.loads(completion["message"].model_dump_json())
    
    def get_completion_args(self, message):
        """Retrieves the input arguments identified by the client and to be used in the function call"""
        return [f"{json.loads(message['tool_calls'][i]['function']['arguments']['equation'])}" for i in range(len(message["tool_calls"]))]
    
    def call_tool(self):
        """Aggregates all tool calls into history"""
        for i in range(len(self.history)):
            if "tool_calls" in self.history[i].keys() and self.history[i]["tool_calls"]:
                tool_calls = []
                for j in range(len(self.history[i]["tool_calls"])):
                    tool_calls.append(self.history[i]["tool_calls"][j])

                message = {
                    "role": "assistant",
                    "content": Calculator(self.history[i]["tool_calls"][j]["function"]["arguments"]["equation"]).calculate(),
                    "images": None,
                    "tool_calls": tool_calls
                }
                self.history[i] = message

