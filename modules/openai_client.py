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

    def chat(self):
        """Streams the final response from the client"""
        self.history[0] = {"role": "system", "content": get_prompt(prompt_type="client")}
        response = openai.chat.completions.create(
            model=self.model,
            messages=self.history,
            tools=self.tools,
            tool_choice="none",
            stream=True
        )

        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)

        self.history = [self.sys_message]


    def update_history(self, input_message: str):
        """Updates client history after the user sends a message to the client"""
        self.history.append({"role": "user", "content": input_message})
        self.setup()
        self.history[0] = {"role": "system", "content": get_prompt(prompt_type="calc")}
        completion = self.get_completion(tool_choice=self.tool_choice)
        self.args = self.get_completion_args(completion)
        message = self.get_message(completion)
        message["content"] = self.get_content(completion, message)
        self.history.append(message)

        if completion.tool_calls:
            self.history.extend(message for message in self.get_tool_messages(self.history))

    def setup(self):
        """Prepares logic for llm calculation"""
        completion = self.get_completion(tool_choice="none")
        message = self.get_message(completion)
        self.history.append(message)

    def get_completion(self, tool_choice):
        """Retrieves the client message metadata"""
        response = openai.chat.completions.create(
            model=self.model,
            messages=self.history,
            tools=self.tools,
            tool_choice=tool_choice
        )

        return response.choices[0].message

    def get_message(self, completion):
        "Parses the message metadata into a python dict"
        return json.loads(completion.model_dump_json())

    def get_content(self, completion, message: dict):
        """Retrieves the content of the message"""
        if completion.tool_calls:
            return str(message["tool_calls"][0]["function"])
        else:
            return str(message["content"])

    def get_tool_messages(self, history: list):
        "Aggregates all tool messages into a list"
        messages = []
        for i in range(len(history)):
            if "tool_calls" in history[i].keys() and history[i]["tool_calls"]:
                for j in range(len(history[i]["tool_calls"])):
                    message = {
                        "role": "tool",
                        "tool_call_id": history[i]["tool_calls"][j]["id"],
                        "name": history[i]["tool_calls"][j]["function"]["name"],
                        "content": Calculator(history[i]["tool_calls"][j]["function"]["arguments"]).calculate()
                    }
                    messages.append(message)

        return messages

    def get_completion_args(self, completion):
        """Retrieves the input arguments identified by the client and to be used in the function call"""
        if completion.tool_calls:
            return [f"{json.loads(completion.tool_calls[i].function.arguments)}" for i in range(len(completion.tool_calls))]
        else:
            return None

