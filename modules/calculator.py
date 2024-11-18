from sympy import Eq, sympify, simplify, solve
import re


class Calculator():
    def __init__(self, function: str, target: str, variables: dict):
        self.function = function
        self.variables = variables
        self.target = {target: self.variables.pop(target)}

    def split(self):
        right = self.function
        pattern = re.compile(r"[<>]=?|!=|==|=")
        match = re.search(pattern, right)
        if match:
                left = right[:match.start()]
                right = right[match.end() + 1:]
                self.expressions = [left, right]
        else:
            self.expressions = [right]

    def substitute(self, expressions: list):
        substitution_made = False
        for i in range(len(expressions)):
            original_expression = expressions[i]
            for key, value in self.variables.items():
                pattern = r'\b' + re.escape(key) + r'\b'
                expressions[i] = re.sub(pattern, value, expressions[i])
            if expressions[i] != original_expression:
                substitution_made = True
        
        if substitution_made:
            return self.substitute(expressions=expressions)
        else:
            self.expressions = expressions
   
    def simplify(self):
        self.split()
        self.substitute(expressions=self.expressions)
        self.expressions_simplified = list()
        for expression in self.expressions:
            self.expressions_simplified.append(simplify(sympify(expression)))

    def calulate(self):
        self.simplify()
        if len(self.expressions_simplified) > 1:
            left = self.expressions_simplified[0]
            right = self.expressions_simplified[1]
            equation = Eq(left, right)
        else:
            equation = Eq(self.expressions_simplified[0], 0)
        solution = ", ".join([f"{self.target} = {s}" for s in solve(equation)])
        output = f"Solved target variable \"{self.target}\" in the equation \"{self.function}\":\n{solution}"
        
        return output, solution

