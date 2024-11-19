from modules.ollama_client import OllamaClient
from modules.openai_client import OpenAiClient
from modules.calculator import Calculator
import json


with open("data\\questions.json", "r") as fp:
    questions = json.load(fp)

with open("data\\sys_messages.json", "r") as fp:
    sys_messages = json.load(fp)

parser_agent = OpenAiClient(sys_message=sys_messages["sys_message"])
question = questions['question_8']

parser_agent.append_history(input_message=question['question'])
response = parser_agent.chat()
print(f"EXPLINATION:\n{response}\n{'='*50}")

target = json.loads(response)["solution"]["target_variable"]
variables = json.loads(response)["solution"]["variable_definitions"]
equation = json.loads(response)["solution"]["proposed_equation"]

print(f"EQUATION:\n{'-'*50}\n{equation}\n{'='*50}")

print(f"ANSWER:\n{'-'*50}\n{question['answer']}\n{'='*50}")

calculator = Calculator(function=equation, target=target, variables=variables)
output, solution = calculator.calulate()
print(f"OUTPUT:\n{'-'*50}\n{output}\n{'='*50}\nCALCULATED:\n{'-'*50}\n{solution}\n{'='*50}")

