from sympy import *
import json
import re

"""
Calculator that ingests LLM's equation, target variable, and variable definitions,
attempts to prepare the equation through the following techniques:
    1. Splits the equation into two sides, left and right, if an operator is found as a substring
    2. Truncates value if the LLM defined a variable as {key: key = def} to {key: def}
    3. Fixes key-value pairs having the key as a substring in the value (prevents infinite recursion in next step)
    4. Substitutes all values containing a substring that matches a key found in the variable definitions
    5. Simplifies the cleaned expressions for final calculation
    6. Callable caulculate method to calculate and return answer
"""


class Calculator():
    def __init__(self, equation: str):
        self.equation = equation

    def parse_equation(self, equaiton: str):
        return json.loads(equaiton)["equation"]

    def split(self):
        """
        Splits the original equation into two sides, 'left' and 'right',
        and returns the two sides with the operator that separated them.
        """
        left = self.equation
        pattern = re.compile(r"[<>]=?|!=|==|=")
        match = re.search(pattern, left)
        if match:
                right = left[match.end() + 1:]
                left = left[:match.start()]
                operator = match.group(0)
        else:
            right = "0"
            operator = "="

        return left, operator, right
        
    def parse_sides(self, left: str, right: str):
        """
        Formats all expressions using sympify so it can be used by the simplify method
        to simplify the expression.
        """
        left = simplify(sympify(left.lower()))
        right = simplify(sympify(right.lower()))

        return left, right

    def calculate(self):
        """
        Solves the equation, 'equaiton', by splitting the two sides, simplifying them,
        and then solving the equation.
        """
        left, operator, right = self.split()
        left, right = self.parse_sides(left, right)

        if isinstance(left, Number) and isinstance(right, Number):
            return f"{left} {operator} {right}"
        equation = Eq(left, right)

        #Joins the list returned by solve(equation)
        solution = f"{operator}".join([f"{s}" for s in solve(equation)])
        
        return solution