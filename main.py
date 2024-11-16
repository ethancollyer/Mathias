from modules.eq_agent import EqAgent
from modules.declarative_agent import DeclarativeAgent
import json


with open("questions.json", "r") as fp:
    questions = json.load(fp)

declarative_agent = DeclarativeAgent()
equation_agent = EqAgent()
question = questions['question_2']

declarative_agent.append_history(input_message=question['question'])
response = declarative_agent.chat()
print(f"EXPLINATION:\n{response}\n{'='*50}")

equation_agent.append_history(input_message=response)
response = equation_agent.chat()
print(f"RESPONSE:\n{response}")

print(f"ANSWER:\n{question['answer']}")

