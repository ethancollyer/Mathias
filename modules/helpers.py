import pathlib
import json

        
def load_json(filepath):
    working_dir = pathlib.Path(__file__).parent.parent.absolute()
    path = working_dir.joinpath(filepath)
    with open(path, "r", encoding="utf-8") as fp:
        loaded_json = json.load(fp)

    return loaded_json

