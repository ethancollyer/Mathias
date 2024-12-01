from modules.openai_client import OpenAI
from modules.ollama_client import Ollama
from modules.helpers import *
import pandas as pd


def main():
    #questions = load_json(filepath="data\\questions.json")
    #client = OpenAI(model="gpt-4o-mini")
    df = pd.read_csv("data\\MATH.csv")
    client = Ollama(model="llama3.1")

    for i in range(df.shape[0]):
        question = df["problem"].iloc[i]
        solution = df["solution"].iloc[i]

        print(f"Question {i + 1}: {question}\n\nAnswer: {solution}\n{'-'*125}")
        client.solve(input_message=question)
        print(f"\n{'-'*125}\nArguments: {client.args}\nParsed Equation: {client.equation}\n")
        client.history = [client.sys_message]
        print(f"\n{'='*125}")
        

if __name__ == "__main__":
    main()

