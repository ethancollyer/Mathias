import openai
import os


class OpenAiClient:
    def __init__(self, sys_message: str, model: str = 'gpt-4o-mini', api_key: str = os.getenv("OPENAI_API_KEY")):
        openai.api_key = api_key
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
        response = openai.chat.completions.create(model=self.model, messages=self.history)
        return response.choices[0].message.content
    
    