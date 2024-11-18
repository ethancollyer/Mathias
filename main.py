from modules.ollama_agent import OllamaAgent
from modules.openai_agent import OpenAiAgent
from modules.calculator import Calculator
import json


with open("questions.json", "r") as fp:
    questions = json.load(fp)

with open("sys_messages.json", "r") as fp:
    sys_messages = json.load(fp)

parser_agent = OpenAiAgent(sys_message=sys_messages["sys_message"])
question = questions['question_6']

parser_agent.append_history(input_message=question['question'])
response = parser_agent.chat()
print(f"EXPLINATION:\n{response}\n{'='*50}")

target = json.loads(response)["solution"]["target_variable"]
variables = json.loads(response)["solution"]["variable_definitions"]
equation = json.loads(response)["solution"]["proposed_equation"]

print(f"EQUATION:\n{equation}\n{'='*50}")

print(f"ANSWER:\n{question['answer']}")

calculator = Calculator(function=equation, target=target, variables=variables)
output, solution = calculator.calulate()
print(f"OUTPUT:\n{output}\n\nCALCULATED:\n{solution}")

