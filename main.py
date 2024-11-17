from modules.agent import Agent
from modules.calculator import Calculator
import json


with open("questions.json", "r") as fp:
    questions = json.load(fp)

with open("sys_messages.json", "r") as fp:
    sys_messages = json.load(fp)

parser_agent = Agent(sys_message=sys_messages["sys_message_parser"])
equation_agent = Agent(sys_message=sys_messages["sys_message_eq"])
question = questions['question_2']

parser_agent.append_history(input_message=question['question'])
response = parser_agent.chat()
print(f"EXPLINATION:\n{response}\n{'='*50}")

equation_agent.append_history(input_message=response)
response = equation_agent.chat()
print(f"RESPONSE:\n{response}")

calculator = Calculator(function=response)
output = calculator.calulate()
print(f"CALCULATED:\n{output}")

print(f"ANSWER:\n{question['answer']}")

