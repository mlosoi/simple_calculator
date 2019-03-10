import re
import sys

from enum import *

from token import *

print_debug_output = True

# input_expression = '2 * (23/(33))- 23 * (23)'



# Parameters:
#   expression:
#     A mathematical expression that is allowed to contain addition, subtraction, multiplication, division and parenthesis for grouping. All characters other than digits, +, -, *, / and parenthesis are filtered out

def calculate_value(infix_expression):
    # Normalize input
    infix_expression = normalize_input(infix_expression)

    if print_debug_output:
        print('Normalized infix expression: {0}'.format(infix_expression))

    if not validate_input(infix_expression):
        return None

    # Tokenize infix expression
    tokenized_infix_expression = tokenize_expression(infix_expression)

    if print_debug_output:
        print('Tokenized infix expression: {0}'.format(tokenized_infix_expression))

    # Convert infix expression to postfix expression
    tokenized_postfix_expression = infix_to_postfix(tokenized_infix_expression)

    if print_debug_output:
        print('Postfix expression: {0}'.format(tokenized_expression_to_str(tokenized_postfix_expression)))

    return evaluate_postfix(tokenized_postfix_expression)

def normalize_input(expression):
    # Filter out characters other than digits, +, -, *, / and parenthesis
    return re.sub('[^0-9|\\+|\\-|\\*|\\/|\\(|\\)]', '', expression)

def validate_input(expression):
    # Check that the number of opening parenthesis match with the number of closing parenthesis
    if expression.count('(') != expression.count(')'):
        print('The number of opening parenthesis does not match with the number of closing parenthesis')

        return False

    return True

def tokenize_expression(expression):
    tokens = []
    reading_number = False
    current_number = None

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
                tokens.append(Token(Token.Type.OPERATOR, character))
            elif character == Token.Identifier.OPENING_PARENTHESIS:
                tokens.append(Token(Token.Type.OPENING_PARENTHESIS, character))
            elif character == Token.Identifier.CLOSING_PARENTHESIS:
                tokens.append(Token(Token.Type.CLOSING_PARENTHESIS, character))

    if reading_number:
        tokens.append(Token(Token.Type.NUMBER, float(current_number)))
    
    return tokens

# http://csis.pace.edu/~wolf/CS122/infix-postfix.htm
def infix_to_postfix(infix_expression):
    postfix_expression = []
    operator_stack = []

    for token in infix_expression:
        if token.type == Token.Type.NUMBER:
            postfix_expression.append(token)
        elif token.type == Token.Type.OPERATOR:
            top_operator = None

            if len(operator_stack) > 0:
                top_operator = operator_stack[-1]

                if (top_operator.datum == Token.Identifier.OPERATOR_MULTIPLICATION or top_operator.datum == Token.Identifier.OPERATOR_DIVISION) and (token.datum == Token.Identifier.OPERATOR_ADDITION or token.datum == Token.Identifier.OPERATOR_SUBTRACTION):
                    # The previous operator precedes the current one. Thus, it should be taken out of the operator stack and appended to the postfix expression
                    postfix_expression.append(operator_stack.pop())

            operator_stack.append(token)

        elif token.type == Token.Type.OPENING_PARENTHESIS:
            operator_stack.append(token)
        elif token.type == Token.Type.CLOSING_PARENTHESIS:
            top_operator = operator_stack.pop()

            while top_operator.type != Token.Type.OPENING_PARENTHESIS:
                postfix_expression.append(top_operator)

                top_operator = operator_stack.pop()

    # The remaining operators in the stack should be appended to the postfix expression
    while len(operator_stack) > 0:
        postfix_expression.append(operator_stack.pop())

    return postfix_expression

def evaluate_postfix(postfix_expression):
    number_stack = []

    for token in postfix_expression:
        if token.type == Token.Type.NUMBER:
            number_stack.append(token)
        elif token.type == Token.Type.OPERATOR:
            operand_2 = number_stack.pop()
            operand_1 = number_stack.pop()

            result = None

            if token.datum == Token.Identifier.OPERATOR_ADDITION:
                result = Token(Token.Type.NUMBER, operand_1.datum + operand_2.datum)
            elif token.datum == Token.Identifier.OPERATOR_SUBTRACTION:
                result = Token(Token.Type.NUMBER, operand_1.datum - operand_2.datum)
            elif token.datum == Token.Identifier.OPERATOR_MULTIPLICATION:
                result = Token(Token.Type.NUMBER, operand_1.datum * operand_2.datum)
            elif token.datum == Token.Identifier.OPERATOR_DIVISION:
                result = Token(Token.Type.NUMBER, operand_1.datum / operand_2.datum)

            number_stack.append(result)

    return number_stack.pop().datum

input_expression = sys.argv[1]

print(calculate_value(input_expression))
