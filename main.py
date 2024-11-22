from modules.client import Client
from modules.debugger import Debugger
from modules.calculator import Calculator
from modules.helpers import *
import traceback
import time
import json


def extract(client_message: str):
    target = json.loads(client_message)["solution"]["target_variable"]
    variables = json.loads(client_message)["solution"]["variable_definitions"]
    equation = json.loads(client_message)["solution"]["proposed_equation"]

    return target, variables, equation

def handle_error(start_time: float, debugger: Debugger, error_message: str, client_message: str):
    try:
        debugged_message = debugger.debug(error_message=error_message, client_message=client_message)
        target, variables, equation = extract(client_message=debugged_message)

        calculator = Calculator(equation=equation, target=target, variables=variables)
        output, solution = calculator.calulate()
        print(f"OUTPUT:\n{output}\nCALCULATED:\n{solution}\n{'='*50}\n\n")
    except Exception as error:
        if time.time() - start_time >= 300:
            print("ERROR: client failed to debug.")
            exit()

        print("Re-Attempting Debugging")
        error_message = traceback.format_exc()
        print(error)
        handle_error(start_time=start_time, debugger=debugger, error_message=error_message, client_message=debugged_message)
    finally:
        print(f"Debugging completed after {time.time() - start_time}")

def main():
    questions = load_json(filepath="data\\questions.json")
    client = Client(provider="openai", model="gpt-4o-mini")
    #client = Client(provider="ollama", model="mistral:7b-instruct")
    debug_list = []

    for key, value in questions.items():
        question = value["question"]
        answer = value["answer"]

        try:
            client.append_history(input_message=question)
            client_message = client.chat()

            target, variables, equation = extract(client_message=client_message)

            print(f"\nEQUATION: {equation}\n")

            print(f"ANSWER: {answer}\n")

            calculator = Calculator(equation=equation, target=target, variables=variables)
            output, solution = calculator.calulate()
            print(f"OUTPUT:\n{output}\nCALCULATED:\n{solution}\n{'='*50}\n\n")
            client.history = [client.history[0]]

        except Exception as error:
            print(f"Debugging Started for {key}")
            debug_list.append(key)
            start = time.time()
            debugger = Debugger(provider="openai", model="gpt-4o-mini")
            error_message = traceback.format_exc()
            print(error)
            handle_error(start_time=start, debugger=debugger, error_message=error_message, client_message=client_message)

    print(f"Number of Debugs: {len(debug_list)}\n{debug_list}")

if __name__ == "__main__":
    main()

