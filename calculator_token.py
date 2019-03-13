from enum import *
from functools import *

class Token:
    class Type(Enum):
        NUMBER = 1
        ARITHMETIC_OPERATOR = 2
        OPENING_PARENTHESIS = 3
        CLOSING_PARENTHESIS = 4

    class Identifier:
        ADDITION = '+'
        SUBTRACTION = '-'
        MULTIPLICATION = '*'
        DIVISION = '/'
        OPENING_PARENTHESIS = '('
        CLOSING_PARENTHESIS = ')'

    type = None
    datum = None

    @classmethod
    def number(cls, number):
        return cls(cls.Type.NUMBER, number)

    @classmethod
    def arithmetic_operator(cls, operator):
        return cls(cls.Type.ARITHMETIC_OPERATOR, operator)

    @classmethod
    def addition_operator(cls):
        return cls(cls.Type.ARITHMETIC_OPERATOR, cls.Identifier.ADDITION)

    @classmethod
    def subtraction_operator(cls):
        return cls(cls.Type.ARITHMETIC_OPERATOR, cls.Identifier.SUBTRACTION)

    @classmethod
    def multiplication_operator(cls):
        return cls(cls.Type.ARITHMETIC_OPERATOR, cls.Identifier.MULTIPLICATION)

    @classmethod
    def division_operator(cls):
        return cls(cls.Type.ARITHMETIC_OPERATOR, cls.Identifier.DIVISION)

    @classmethod
    def opening_parenthesis(cls):
        return cls(cls.Type.OPENING_PARENTHESIS, cls.Identifier.OPENING_PARENTHESIS)

    @classmethod
    def closing_parenthesis(cls):
        return cls(cls.Type.CLOSING_PARENTHESIS, cls.Identifier.CLOSING_PARENTHESIS)

    def __init__(self, type, datum):
        self.type = type
        self.datum = datum

    def __repr__(self):
        return "(" + str(self.type) + ", " + str(self.datum) + ")"

    def __eq__(self, token):
        return self.type == token.type and self.datum == token.datum

    # Note that there's no need to override the inequality operator (!= / __ne__) because in Python 3 the inequality operator returns the inverse of the equality operator (== / __eq__)

    def __add__(self, token):
        if self.is_number() and token.is_number():
            return self.number(self.datum + token.datum)
        else:
            return None

    def __sub__(self, token):
        if self.is_number() and token.is_number():
            return self.number(self.datum - token.datum)
        else:
            return None

    def __mul__(self, token):
        if self.is_number() and token.is_number():
            return self.number(self.datum * token.datum)
        else:
            return None

    def __truediv__(self, token):
        if self.is_number() and token.is_number():
            return self.number(self.datum / token.datum)
        else:
            return None

    def is_number(self):
        return self.type == self.Type.NUMBER

    def is_arithmetic_operator(self):
        return self.type == self.Type.ARITHMETIC_OPERATOR

    def is_addition_operator(self):
        return self.type == self.Type.ARITHMETIC_OPERATOR and self.datum == Token.Identifier.ADDITION

    def is_subtraction_operator(self):
        return self.type == self.Type.ARITHMETIC_OPERATOR and self.datum == self.Identifier.SUBTRACTION

    def is_multiplication_operator(self):
        return self.type == self.Type.ARITHMETIC_OPERATOR and self.datum == self.Identifier.MULTIPLICATION

    def is_division_operator(self):
        return self.type == self.Type.ARITHMETIC_OPERATOR and self.datum == self.Identifier.DIVISION

    def is_opening_parenthesis(self):
        return self.type == self.Type.OPENING_PARENTHESIS

    def is_closing_parenthesis(self):
        return self.type == self.Type.CLOSING_PARENTHESIS

    def value(self):
        if self.is_number():
            return self.datum

        return None

    # Operator precedence level:
    #   0: number, i.e., not an operator at all
    #   1: opening or closing parenthesis, i.e., grouping operator_stack
    #   2: addition or subtraction
    #   3: multiplication or division
    def get_operator_precedence_level(self):
        if self.is_number():
            return 0

        if self.is_opening_parenthesis() or self.is_closing_parenthesis():
            return 1

        if self.is_addition_operator() or self.is_subtraction_operator():
            return 2

        if self.is_multiplication_operator() or self.is_division_operator():
            return 3

# Reads an expression as a string and transforms it into a tokenized expression, i.e., a list of Token instances
def tokenize_expression(expression):
    tokens = []

    reading_number = False
    current_number = None

    i_current_character = 0

    for character in expression:
        if character.isdigit():
            reading_number = True

            if current_number == None:
                current_number = character
            else:
                current_number += character

        else:
            if reading_number:
                tokens.append(Token.number(float(current_number)))

                reading_number = False
                current_number = None

            if character == Token.Identifier.ADDITION or character == Token.Identifier.SUBTRACTION or character == Token.Identifier.MULTIPLICATION or character == Token.Identifier.DIVISION:
                # Consider the special case in which a subexpression begins with negation. In such cases, the minus operator should be converted to -1 and a multiplication tokens
                if character == Token.Identifier.SUBTRACTION and (i_current_character == 0 or (i_current_character > 0 and expression[i_current_character - 1] == Token.Identifier.OPENING_PARENTHESIS)):
                    tokens.append(Token.number(-1))
                    tokens.append(Token.multiplication_operator())

                else:
                    tokens.append(Token.arithmetic_operator(character))
            elif character == Token.Identifier.OPENING_PARENTHESIS:
                tokens.append(Token.opening_parenthesis())
            elif character == Token.Identifier.CLOSING_PARENTHESIS:
                tokens.append(Token.closing_parenthesis())

        i_current_character += 1

    if reading_number:
        tokens.append(Token.number(float(current_number)))

    return tokens

# Converts a tokenized expresion into a string for pretty print
def tokenized_expression_to_str(tokenized_expression):
    if len(tokenized_expression) == 0:
        return ''

    return reduce(lambda token_1_datum, token_2_datum: '{0} {1}'.format(token_1_datum, token_2_datum), map(lambda token: token.datum, tokenized_expression))
