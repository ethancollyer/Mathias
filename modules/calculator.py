import sympy
import re


def parse_func(function: str):
    pattern = re.compile(r"[A-Za-z]")
    matches = re.findall(pattern, function)
    return sympy.sympify(function)

def calulate(function):
    return function

func = parse_func("a = (5 - 2) + (5 - 2)")

print(func)