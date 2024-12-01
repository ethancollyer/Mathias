from sympy import *
from .helpers import *
import re

"""
Calculator that ingests the equation, performs transormations, then uses the transformed
equation to solve the equation using sympy.
"""


class Calculator():
    def __init__(self, equation: str):
        self.equation = equation
        print(f"Equation: {self.equation}\n")

    def parse_equation(self, expression: str):
        """Fixes common errors found in the equation produced by the client LLM."""
        cases = {"|": "regex", "arc": "a", "^": "**", ")(": ")*("}
        for case, replacement in cases.items():
            if replacement == "regex":
                pattern = re.compile(re.escape(case) + r"(.+)" + re.escape(case))
                expression = pattern.sub(r"abs(\1)", expression)
            else:
                expression = expression.replace(case, replacement)
        if expression.count('(') > expression.count(')'):
            expression += ')' * (expression.count('(') - expression.count(')'))
        elif expression.count(')') > expression.count('('):
            expression = '(' * (expression.count(')') - expression.count('(')) + expression

        return expression

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
        print(f"Split (l, o, r): {left}, {operator}, {right}\n")
        
        return left, operator, right
        
    def parse_sides(self, left: str, right: str):
        """
        Formats all expressions using sympify so it can be used by the simplify method
        to simplify the expression.
        """
        left = simplify(sympify(left.lower()))
        right = simplify(sympify(right.lower()))
        print(f"Simplify (l, r): {left}, {right}")

        return left, right

    def calculate(self):
        """
        Solves the equation by splitting the two sides, simplifying them,
        and then solving the equation.
        """
        left, operator, right = self.split()
        left = self.parse_equation(left)
        right = self.parse_equation(right)
        left, right = self.parse_sides(left, right)

        if isinstance(left, Number) and isinstance(right, Number):
            return f"{left} {operator} {right}"
        equation = Eq(left, right)
        print(f"Final Equation: {equation}")

        #Joins the list returned by solve(equation)
        try:
            solution = f" {operator} ".join(f"{s}" for s in with_timeout(15, solve, equation))
        except TimeoutError as e:
            print(f"Calculation timed out: {e}")
            solution = f"{left} {operator} {right}"
        
        return solution

