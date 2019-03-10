from enum import *
from functools import *

class Token:
    class Type(Enum):
        NUMBER = 1
        OPERATOR = 2
        OPENING_PARENTHESIS = 3
        CLOSING_PARENTHESIS = 4

    class Identifier:
        OPERATOR_ADDITION = '+'
        OPERATOR_SUBTRACTION = '-'
        OPERATOR_MULTIPLICATION = '*'
        OPERATOR_DIVISION = '/'
        OPENING_PARENTHESIS = '('
        CLOSING_PARENTHESIS = ')'

    type = None
    datum = None

    def __init__(self, type, datum):
        self.type = type
        self.datum = datum

    def __repr__(self):
        return "(" + str(self.type) + ", " + str(self.datum) + ")"

    def is_number(self):
        return self.type == Token.Type.NUMBER

    def is_operator(self):
        return self.type == Token.Type.OPERATOR

    def is_addition_operator(self):
        return self.type == Token.Type.OPERATOR and self.datum == Token.Identifier.OPERATOR_ADDITION

    def is_subtraction_operator(self):
        return self.type == Token.Type.OPERATOR and self.datum == Token.Identifier.OPERATOR_SUBTRACTION

    def is_multiplication_operator(self):
        return self.type == Token.Type.OPERATOR and self.datum == Token.Identifier.OPERATOR_MULTIPLICATION

    def is_division_operator(self):
        return self.type == Token.Type.OPERATOR and self.datum == Token.Identifier.OPERATOR_DIVISION

    def is_opening_parenthesis(self):
        return self.type == Token.Type.OPENING_PARENTHESIS

    def is_closing_parenthesis(self):
        return self.type == Token.Type.CLOSING_PARENTHESIS

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
                tokens.append(Token(Token.Type.NUMBER, float(current_number)))

                reading_number = False
                current_number = None

            if character == Token.Identifier.OPERATOR_ADDITION or character == Token.Identifier.OPERATOR_SUBTRACTION or character == Token.Identifier.OPERATOR_MULTIPLICATION or character == Token.Identifier.OPERATOR_DIVISION:
                # Consider the special case in which a subexpression begins with negation. In such cases, the minus operator should be converted to -1 and a multiplication tokens
                if character == Token.Identifier.OPERATOR_SUBTRACTION and (i_current_character == 0 or (i_current_character > 0 and expression[i_current_character - 1] == Token.Identifier.OPENING_PARENTHESIS)):
                    tokens.append(Token(Token.Type.NUMBER, -1))
                    tokens.append(Token(Token.Type.OPERATOR, Token.Identifier.OPERATOR_MULTIPLICATION))

                else:
                    tokens.append(Token(Token.Type.OPERATOR, character))
            elif character == Token.Identifier.OPENING_PARENTHESIS:
                tokens.append(Token(Token.Type.OPENING_PARENTHESIS, character))
            elif character == Token.Identifier.CLOSING_PARENTHESIS:
                tokens.append(Token(Token.Type.CLOSING_PARENTHESIS, character))

        i_current_character += 1

    if reading_number:
        tokens.append(Token(Token.Type.NUMBER, float(current_number)))

    return tokens

def tokenized_expression_to_str(tokenized_expression):
    if len(tokenized_expression) == 0:
        return ''

    return reduce(lambda token_1_datum, token_2_datum: '{0} {1}'.format(token_1_datum, token_2_datum), map(lambda token: token.datum, tokenized_expression))
