import re
import sys

from enum import *

from token import *

print_debug_output = True

# calculate_value():
#   Parameters:
#     expression:
#       An infix expression that is allowed to contain addition, subtraction, multiplication, division and parenthesis for grouping. All characters other than digits, +, -, *, / and parenthesis are filtered out

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
        print('Pretty print: {0}'.format(tokenized_expression_to_str(tokenized_infix_expression)))

    # Convert infix expression to postfix expression
    tokenized_postfix_expression = infix_to_postfix(tokenized_infix_expression)

    if print_debug_output:
        print('Postfix expression: {0}'.format(tokenized_expression_to_str(tokenized_postfix_expression)))

    return evaluate_postfix(tokenized_postfix_expression)

def normalize_input(expression):
    # Filter out characters other than digits, +, -, *, / and parenthesis
    return re.sub('[^0-9|\\+|\\-|\\*|\\/|\\(|\\)]', '', expression)

def validate_input(expression):
    # Validate that the input expression is not empty
    if len(expression) == 0:
        print('The input expression is empty')

        return False

    # Validate that the number of opening parenthesis match with the number of closing parenthesis
    if expression.count('(') != expression.count(')'):
        print('The number of opening parenthesis does not match with the number of closing parenthesis')

        return False

    return True

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

# http://csis.pace.edu/~wolf/CS122/infix-postfix.htm
def infix_to_postfix(infix_expression):
    postfix_expression = []
    operator_stack = []

    for token in infix_expression:
        if token.type == Token.Type.NUMBER:
            postfix_expression.append(token)
        elif token.type == Token.Type.OPERATOR:
            if token.datum == Token.Identifier.OPERATOR_ADDITION or token.datum == Token.Identifier.OPERATOR_SUBTRACTION:
                # Pop operators from the stack and append them to the postfix expression until the top operator is either an addition or subtraction operator, i.e., has the same precedence level as the current operator
                if len(operator_stack) > 0:
                    top_operator = operator_stack[-1]

                    while top_operator != None and (top_operator.datum == Token.Identifier.OPERATOR_MULTIPLICATION or top_operator.datum == Token.Identifier.OPERATOR_SUBTRACTION):
                        postfix_expression.append(operator_stack.pop())

                        if len(operator_stack) > 0:
                            top_operator = operator_stack[-1]
                        else:
                            top_operator = None

            operator_stack.append(token)

        elif token.type == Token.Type.OPENING_PARENTHESIS:
            operator_stack.append(token)
        elif token.type == Token.Type.CLOSING_PARENTHESIS:
            top_operator = operator_stack.pop()

            while top_operator.type != Token.Type.OPENING_PARENTHESIS:
                postfix_expression.append(top_operator)

                top_operator = operator_stack.pop()

    # The remaining operators in the stack must be appended to the postfix expression
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
