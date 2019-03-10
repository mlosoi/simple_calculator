# Sources of ideas:
#  https://en.wikipedia.org/wiki/Reverse_Polish_notation
#  http://csis.pace.edu/~wolf/CS122/infix-postfix.htm

import re
import sys

from enum import *

from calculator_token import *

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

def infix_to_postfix(infix_expression):
    postfix_expression = []
    operator_stack = []

    for token in infix_expression:
        if token.is_number():
            postfix_expression.append(token)
        elif token.is_operator():
            operator_processed = False

            while not operator_processed:
                if len(operator_stack) == 0:
                    # The operator stack is empty. Thus, the current operator is pushed onto the stack
                    operator_stack.append(token)

                    operator_processed = True

                    continue

                top_operator = operator_stack[-1]

                if top_operator.is_opening_parenthesis():
                    # The top operator is an opening parenthesis, i.e., has the lowest possible precedence level. Thus, the current operator can be pushed onto the stack without further deductions
                    operator_stack.append(token)

                    operator_processed = True

                    continue

                # Check if the current operator has higher precedence than the top of the stack
                if ((token.is_multiplication_operator() or token.is_division_operator()) and (top_operator.is_addition_operator() or top_operator.is_subtraction_operator() or top_operator.is_opening_parenthesis())) or ((token.is_addition_operator() or token.is_subtraction_operator()) and top_operator.is_opening_parenthesis()):
                    # Push the current operator onto the stack because it should be executed earlier than the previous top operator
                    operator_stack.append(token)

                    operator_processed = True

                    continue

                # Check if the current operator has equal precedence with the top of the stack
                if ((token.is_multiplication_operator() or token.is_division_operator()) and (top_operator.is_multiplication_operator() or top_operator.is_division_operator())) or ((token.is_addition_operator() or token.is_subtraction_operator()) and (top_operator.is_addition_operator() or top_operator.is_subtraction_operator())):
                    # The top operator is popped from the stack and the current operator is pushed onto the stack
                    postfix_expression.append(operator_stack.pop())

                    operator_stack.append(token)

                    operator_processed = True

                    continue

                # Check if the top operator has higher precedence thatn the current operator
                if (token.is_addition_operator() or token.is_subtraction_operator()) and (top_operator.is_multiplication_operator() or top_operator.is_division_operator()):
                    # The top operator is popped out of the stack because it should be executed earlier than the current operator which will be tested again against the top of the stack
                    postfix_expression.append(operator_stack.pop())

                    continue

        elif token.is_opening_parenthesis():
            operator_stack.append(token)
        elif token.is_closing_parenthesis():
            top_operator = operator_stack.pop()

            while not top_operator.is_opening_parenthesis():
                postfix_expression.append(top_operator)

                top_operator = operator_stack.pop()

        # print('{0}; {1}; {2}'.format(token, tokenized_expression_to_str(operator_stack), tokenized_expression_to_str(postfix_expression)))

    # The remaining operators in the stack must be appended to the postfix expression
    while len(operator_stack) > 0:
        postfix_expression.append(operator_stack.pop())

    return postfix_expression

def evaluate_postfix(postfix_expression):
    number_stack = []

    for token in postfix_expression:
        if token.is_number():
            number_stack.append(token)
        elif token.is_operator():
            operand_2 = number_stack.pop()
            operand_1 = number_stack.pop()

            result = None

            if token.is_addition_operator():
                result = Token(Token.Type.NUMBER, operand_1.datum + operand_2.datum)
            elif token.is_subtraction_operator():
                result = Token(Token.Type.NUMBER, operand_1.datum - operand_2.datum)
            elif token.is_multiplication_operator():
                result = Token(Token.Type.NUMBER, operand_1.datum * operand_2.datum)
            elif token.is_division_operator():
                result = Token(Token.Type.NUMBER, operand_1.datum / operand_2.datum)

            number_stack.append(result)

    return number_stack.pop().datum

if __name__ == '__main__':
    input_expression = sys.argv[1]

    print(calculate_value(input_expression))
