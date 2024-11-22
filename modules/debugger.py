import pathlib
import json
import re
import datetime


class Debugger:
    def __init__(self, error_type: type, error_message: str, response: str):
        self.error_type = error_type
        self.error_message = error_message
        self.response = response

    def debug(self):
        if self.error_type == json.decoder.JSONDecodeError:
            print("DEBUGGING")
            self.json_decode_error()
            print("ERROR RESOLVED!")
        else:
            print("ERROR UNRESOVLED!")
            date = datetime.datetime.now(datetime.timezone.utc)
            working_dir = pathlib.Path(__file__).parent.parent.absolute()
            with open(working_dir.joinpath("logs\\log.txt"), "a") as fp:
                fp.write(f"{self.error_message}\n{'='*50}\n")
            with open(working_dir.joinpath("error_scenarios\\{date}.txt"), "a") as fp:
                fp.write(f"{self.error_message}\n{'='*50}\n{self.response}")

    def json_decode_error(self):
        pattern = r"\(char\s(\d+)"
        match = re.search(pattern=pattern, string=self.error_message)
        if match:
            left = self.response[:int(match.group(1))].replace(" ", "").replace("\n", "")[:-1]
            right = self.response[int(match.group(1)):].replace(" ", "").replace("\n", "")
            self.response = left + right

