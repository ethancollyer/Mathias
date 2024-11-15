import ollama


class DeclarativeAgent(ollama.Client):
    def __init__(self, model: str = 'mistral:7b-instruct'):
        super().__init__()
        self.model = model
        self.sys_message1 = {
            "role": "system",
            "content": """Your purpose is to generate step-by-step variable and equation declarations. To declare a variable and an equation, use the following format exactly as it is written: 'Let [[var a]] be... . We now have the equation [[eq a = #]]'. Ensure variables are declared as single letters."""
        }
        self.sys_message2 = {
            "role": "system",
            "content": """Make sure to include the double square brackets in your output for both 'var' and 'eq' expressions. Define the expression in the square brackets as either a variable '[[var (insert_variable_here)]]' or an equation '[[eq (insert_variable_here) = (insert_expression_here)]]'. DO NOT perform any math. Only provide the step-by-step variable and equation declarations."""
        }
        self.history = [self.sys_message1, self.sys_message2]

    def append_history(self, input_message: str, role: str = 'user'):
        message = {
            "role": role,
            "content": input_message
        }
        self.history.append(message)

    def chat(self):
        response = super().chat(model=self.model, messages=self.history)
        return response['message']['content']
    
