from modules.openai_client import OpenAI
from modules.ollama_client import Ollama
from modules.helpers import *


def main():
    questions = load_json(filepath="data\\questions.json")
    #client = OpenAI(model="gpt-3.5-turbo-1106")
    client = Ollama(model="llama3.1")

    for key, value in questions.items():
        question = value["question"]
        answer = value["answer"]

        print(f"Question: {question}\nAnswer: {answer}\n{'-'*125}")
        client.solve(input_message=question)
        print(f"\n{'-'*125}\nArguments: {client.args}")
        client.history = [client.sys_message]
        print(f"\n{'='*125}")
        

if __name__ == "__main__":
    main()

