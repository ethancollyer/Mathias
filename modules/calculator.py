from sympy import Eq, sympify, simplify, solve, Number
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
    def __init__(self, equation: str, target: str, variables: dict):
        self.equation = equation
        self.target_variable = target
        self.variables = variables
        if target in variables.keys():
            del self.variables[target]

        #Preps Calculator to run calculate by running all other methods
        self.expressions = self.split()
        self.variables = {k: self.truncate_value(k, v) for k, v in self.variables.items()}
        self.variables = self.parse_variables()
        self.substitute(expressions=self.expressions)
        self.expressions = self.simplify(expressions=self.expressions)

    def split(self):
        """
        Splits the original equation into two sides, 'left' and 'right',
        if an operator is found in between them. Otherwise, entire equation is returned
        """
        left = self.equation
        pattern = re.compile(r"[<>]=?|!=|==|=")
        match = re.search(pattern, left)
        if match:
                right = left[match.end() + 1:]
                left = left[:match.start()]
                expressions = [left, right]
        else:
            expressions = [left]

        return expressions
    
    def truncate_value(self, key: str, value: str):
        """
        Searches inside the string, value, for the substring, key, and a trailing operator (example: 'key =')
        then substitutes the value with the substring found to the right of the operator
        """
        pattern = r'\b(' + re.escape(key) + r')\b\s*(=|<=|>=|<|>)\s*(.+)'
        value = re.sub(pattern, r'\3', value)
        return value

    def parse_variables(self):
        """
        Searches for any key-value pairs that contains the key as a substring within the value,
        then initializes new_key to variable_{key}. Any values with a substring matching
        the original key will replace the original key substring with new_key.
        """
        for key, value in self.variables.items():
            if key in value:
                new_key = f"variable_{key}"
                variables = {k: v.replace(key, new_key) if k != key else value for k, v in self.variables.items()}
                variables.update({new_key: variables.pop(key)})
                self.variables = variables

        return self.variables

    def substitute(self, expressions: list):
        """
        Recursively searches through all expressions for any substrings that match a key
        in self.variables. Then, replaces the substring with the key's value.
        """
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
        """
        Formats all expressions using sympify so it can be used by the simplify method
        to simplify the expression.
        """
        expressions_simplified = list()
        for expression in expressions:
            expressions_simplified.append(simplify(sympify(expression.lower())))

        return expressions_simplified

    def calulate(self):
        """
        Solves the equation, Eq(). If there is only one expression,
        the method checks if left is not an instance of Number (meaning it has a variable).
        In any other case, the situation is logged.
        """
        left = self.expressions[0]
        if len(self.expressions) > 1:
            right = self.expressions[1]
            equation = Eq(left, right)
        elif not isinstance(left, Number):
            equation = Eq(left, 0)
        else:
            with open("logs\\calculator_logs.txt", "a") as fp:
                fp.writelines(f"Calculate equation failed to calculate Type: {type(equation)}\n{'='*50}")
            equation = left

        #Joins the list returned by solve(equation)
        solution = ", ".join([f"{self.target_variable} = {s}" for s in solve(equation)])
        output = f"Calculated target variable \"{self.target_variable}\" in the equation \"{self.equation}\" as:\n{solution}"
        
        return output, solution

