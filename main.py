from modules.openai_client import OpenaiClient
from modules.helpers import *


def main():
    questions = load_json(filepath="data\\questions.json")
    client = OpenaiClient(model="gpt-3.5-turbo-1106")
    #client = Client(provider="ollama", model="mistral:7b-instruct")

    for key, value in questions.items():
        question = value["question"]
        answer = value["answer"]

        client.update_history(input_message=question)

        #print(f"Chat History: {client.history}\n\n")
        print(f"Question: {question}\nAnswer: {answer}\nArguments: {client.args}\n{'-'*125}")

        client.chat()
        print(f"\n{'='*125}")
        

if __name__ == "__main__":
    main()

