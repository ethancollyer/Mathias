import ollama


class EqAgent(ollama.Client):
    def __init__(self, model: str = 'mistral:7b-instruct'):
        super().__init__()
        self.model = model
        self.sys_message = {
            "role": "system",
            "content": """Your purpose is to generate a final equation as an output based on the input message. Substitute each variable with their respective numeric value. Only output the equation. No other text should be in your output. For example, your entire output should follow the following format exactly as it is written: '[insert_unkown_variable_here] = [insert_final_expression_here]'"""
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
    
