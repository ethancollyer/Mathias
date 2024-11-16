from modules.agent import Agent
import json


with open("questions.json", "r") as fp:
    questions = json.load(fp)

with open("sys_messages.json", "r") as fp:
    parser_sys_message = json.load(fp)['sys_message_parser']
    eq_sys_message = json.load(fp)['sys_message_eq']

parser_agent = Agent(sys_message=parser_sys_message)
equation_agent = Agent(sys_message=eq_sys_message)
question = questions['question_1']

parser_agent.append_history(input_message=question['question'])
response = parser_agent.chat()
print(f"EXPLINATION:\n{response}\n{'='*50}")

equation_agent.append_history(input_message=response)
response = equation_agent.chat()
print(f"RESPONSE:\n{response}")

print(f"ANSWER:\n{question['answer']}")

