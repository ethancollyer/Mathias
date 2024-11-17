from sympy import Eq, sympify, symbols, simplify, solve
import math
import re


class Calculator():
    def __init__(self, function: str):
        self.function = function

    def split(self):
        right = self.function
        expressions = list()
        expression_count = self.function.count("=")
        if expression_count > 0:
            while expression_count > 0:
                left = right[:right.find("=")]
                right = right[right.find("=") + 1:]
                expressions.append(left)

                expression_count = right.count("=")
                if expression_count == 0:
                    expressions.append(right)
        else:
            expressions.append(right)

        return expressions

    def symbolfy(self):
        self.expressions = self.split()
        variables = set()
        pattern = re.compile(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])")
        for expression in self.expressions:
            matches = re.findall(pattern, expression)
            if matches:
                variables.update({match for match in matches})
        
        return symbols(variables)
    
    def simplify(self):
        self.symbols = self.symbolfy()
        expressions_simplified = list()
        for expression in self.expressions:
            expressions_simplified.append(simplify(sympify(expression)))
        
        return expressions_simplified


    def calulate(self):
        self.expressions_simplified = self.simplify()
        expression_count = len(self.expressions_simplified)
        output = ""
        if expression_count > 1:
            for i in range(expression_count - 1):
                left = self.expressions_simplified[i]
                right = self.expressions_simplified[i + 1]
                equation = Eq(left, right)
                calc = solve(equation)
                output += f"Calculation for {equation}:\n {calc}\n\n"
        else:
                equation = Eq(self.expressions_simplified[0], 0)
                calc = solve(equation)
                output += f"Calculation for {equation}:\n {calc}\n\n"
        return output

