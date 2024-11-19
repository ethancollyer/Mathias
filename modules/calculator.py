from sympy import Eq, sympify, simplify, solve
import re


class Calculator():
    def __init__(self, function: str, target: str, variables: dict):
        self.function = function
        self.variables = variables
        if target in variables.keys():
            self.target_variable = target
            self.target_expression = self.variables.pop(target)
        else:
            self.target_variable = target
            self.target_expression = f"IGNORE: definition of \"{target}\" not found in variable_definitions"

        tmp_expressions = self.split()
        self.variables = self.parse_variables()
        self.substitute(expressions=tmp_expressions)
        self.expressions = self.simplify(expressions=tmp_expressions)

    def split(self):
        right = self.function
        pattern = re.compile(r"[<>]=?|!=|==|=")
        match = re.search(pattern, right)
        if match:
                left = right[:match.start()]
                right = right[match.end() + 1:]
                expressions = [left, right]
        else:
            expressions = [right]

        return expressions

    def parse_variables(self):
        parse_check = False
        for key, value in self.variables.items():
            if key in value:
                new_key = f"variable_{key}"
                variables = {k: v.replace(key, new_key) if k != key else value for k, v in self.variables.items()}
                variables.update({new_key: variables.pop(key)})
                parse_check = True

        if parse_check:
            return variables
        else:
            return self.variables


    def substitute(self, expressions: list):
        substitution_check = False
        for i in range(len(expressions)):
            original_expression = expressions[i]
            for key, value in self.variables.items():
                pattern = r'\b' + re.escape(key) + r'\b'
                expressions[i] = re.sub(pattern, value, expressions[i])
            if expressions[i] != original_expression:
                substitution_check = True
        
        if substitution_check:
            return self.substitute(expressions=expressions)
   
    def simplify(self, expressions: list):
        expressions_simplified = list()
        for expression in expressions:
            expressions_simplified.append(simplify(sympify(expression.lower())))

        return expressions_simplified

    def calulate(self):
        left = self.expressions[0]
        if len(self.expressions) > 1:
            right = self.expressions[1]
            equation = Eq(left, right)
        else:
            equation = Eq(left, 0)
        solution = ", ".join([f"{self.target_variable} = {s}" for s in solve(equation)])
        output = f"Calculated target variable \"{self.target_variable}\" in the equation \"{self.function}\" as:\n{solution}"
        
        return output, solution

