import ollama
import openai
import os

"""
LLM Client that supports either ollama or openai to ingest a problem and output
metadata about the problem in json format (prompts can be found in data/sys_messages.json)
that can be used by calculator class to fidn the answer.
"""


class Client:
    def __init__(self, sys_message: str, provider: str, model: str):
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

    def chat(self):
        """
        Streams the response of the llm and returns the full response.
        """
        response = ""
        if self.provider == "ollama":
            lstrip_check = False  # Checks if first chunk has been lstripped
            for chunk in ollama.chat(model=self.model, messages=self.history, stream=True):
                if lstrip_check:
                    content = chunk['message']['content']
                else:
                    content = chunk['message']['content'].lstrip()
                    lstrip_check = True
                print(content, end='', flush=True)
                response += content

        elif self.provider == "openai":
            for chunk in openai.chat.completions.create(model=self.model, messages=self.history, stream=True):
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end='', flush=True)
                    response += content

        return response

