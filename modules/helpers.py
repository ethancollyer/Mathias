import pathlib
import json

        
def load_json(filepath):
    working_dir = pathlib.Path(__file__).parent.parent.absolute()
    path = working_dir.joinpath(filepath)
    with open(path, "r", encoding="utf-8") as fp:
        loaded_json = json.load(fp)

    return loaded_json

def get_tools():
    tools = [{
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "takes an equation string as an input, parses the equation string into sympy expressions, then returns the computed solution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equation": {
                        "type": "string",
                        "description": "the mathmatical expression that needs to be computed. e.g. 3*x**2 = asin(16) / 4",
                    },
                },
                "required": ["equation"],
            },
        },
    }]

    return tools