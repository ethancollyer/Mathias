import ollama
import json


class DeclarativeAgent(ollama.Client):
    def __init__(self, model: str = 'mistral:7b-instruct'):
        super().__init__()
        with open("sys_messages.json", "r") as fp:
            sys_message = json.load(fp)['sys_message_parser']
            
        self.model = model
        self.sys_message = {
            "role": "system",
            "content": sys_message
        }
        self.history = [self.sys_message]

    def append_history(self, input_message: str, role: str = 'user'):
        message = {
            "role": role,
            "content": input_message
        }
        self.history.append(message)

    def chat(self):
        response = super().chat(model=self.model, messages=self.history)
        return response['message']['content']
    
