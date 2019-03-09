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

    def __init__(token, type, datum):
        token.type = type
        token.datum = datum

    def __repr__(token):
        return "(" + str(token.type) + ", " + str(token.datum) + ")"

def tokenized_expression_to_str(tokenized_expression):
    return reduce(lambda token_1_datum, token_2_datum: '{0} {1}'.format(token_1_datum, token_2_datum), map(lambda token: token.datum, tokenized_expression))
