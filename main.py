from modules.client import Client
from modules.calculator import Calculator
import json

with open("data\\questions.json", "r") as fp:
    questions = json.load(fp)

with open("data\\sys_messages.json", "r") as fp:
    sys_messages = json.load(fp)

#client = Client(sys_message=sys_messages["sys_message"], provider='openai', model='gpt-4o-mini')
client = Client(sys_message=sys_messages["sys_message"], provider='ollama', model='mistral:7b-instruct')

for key, value in questions.items():
    question = value["question"]
    answer = value["answer"]
    print(f"QUESTION: {key}\n{question}\n{answer}\n\n")

    try:
        client.append_history(input_message=question)
        response = client.chat()

        target = json.loads(response)["solution"]["target_variable"]
        variables = json.loads(response)["solution"]["variable_definitions"]
        equation = json.loads(response)["solution"]["proposed_equation"]

        print(f"\nEQUATION: {equation}\n")

        print(f"ANSWER: {answer}\n")

        calculator = Calculator(function=equation, target=target, variables=variables)
        output, solution = calculator.calulate()
        print(f"OUTPUT:\n{output}\nCALCULATED:\n{solution}\n{'='*50}\n\n")

    except BaseException as e:
        print("ERROR")
        with open("logs\\log.txt", "a") as fp:
            fp.write(f"ERROR on {key}: {e.with_traceback()}\n{'='*50}\n")

