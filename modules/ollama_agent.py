import ollama


class OllamaAgent:
    def __init__(self, sys_message: str, model: str = 'mistral:7b-instruct'):
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
        response = ollama.chat(model=self.model, messages=self.history)
        return response['message']['content']
    
