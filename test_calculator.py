import math

from unittest import TestCase
from unittest import main

import calculator

from calculator_token import *

# Disable intermediate log output from the calculator module to enhance readability of console output
calculator.print_debug_output = False

# Test data {

# Tokenizer test {

test_expression_set_for_tokenizer_test = [
    '1+1',
    '-1',
    '3*(-10)',
    '1/3-1/3'
]

tokenized_expressions_of_tokenizer_test = [
    [Token.number(1),
     Token.addition_operator(),
     Token.number(1)],
    [Token.number(-1),
     Token.multiplication_operator(),
     Token.number(1)],
    [Token.number(3),
     Token.multiplication_operator(),
     Token.opening_parenthesis(),
     Token.number(-1),
     Token.multiplication_operator(),
     Token.number(10),
     Token.closing_parenthesis()],
    [Token.number(1),
     Token.division_operator(),
     Token.number(3),
     Token.subtraction_operator(),
     Token.number(1),
     Token.division_operator(),
     Token.number(3)]
]

# Tokenizer test }

# Infix to postfix test {

# Examples from http://csis.pace.edu/~wolf/CS122/infix-postfix.htm {

test_expression_set_for_infix_to_postfix_test = [
    # "A * B + C becomes A B * C +"
    '1 * 5 + 3',
    # "A + B * C becomes A B C * +"
    '9 + 10 * 3',
    # "A * (B + C) becomes A B C + *"
    '3 * (1 + 1)',
    # "A - B + C becomes A B - C +"
    '1 - 2 + 1',
    # "A * (B + C * D) + E becomes A B C D * + * E +"
    '1 * (2 + 3 * 4) + 5'
]

tokenized_expressions_of_infix_to_postfix_test = [
    # 1 5 * 3 +
    [Token.number(1),
     Token.number(5),
     Token.multiplication_operator(),
     Token.number(3),
     Token.addition_operator()],
    # 9 10 3 * +
    [Token.number(9),
     Token.number(10),
     Token.number(3),
     Token.multiplication_operator(),
     Token.addition_operator()],
    # 3 1 1 + *
    [Token.number(3),
     Token.number(1),
     Token.number(1),
     Token.addition_operator(),
     Token.multiplication_operator()],
    # 1 2 - 1 +
    [Token.number(1),
     Token.number(2),
     Token.subtraction_operator(),
     Token.number(1),
     Token.addition_operator()],
    # 1 2 3 4 * + * 5 +
    [Token.number(1),
     Token.number(2),
     Token.number(3),
     Token.number(4),
     Token.multiplication_operator(),
     Token.addition_operator(),
     Token.multiplication_operator(),
     Token.number(5),
     Token.addition_operator()]
]

# Examples from http://csis.pace.edu/~wolf/CS122/infix-postfix.htm }

# Infix to postfix test }

all_test_expressions = test_expression_set_for_tokenizer_test.copy()

all_test_expressions.extend(test_expression_set_for_infix_to_postfix_test)

all_test_expressions.extend([
    '-(-(-(-10)))',
    '-4',
    '-1*1234*(((-1)))*(-1)+1234',
    '-1*1234*(((-1)))*(-1)',
    '1+1+(1+3)+4*5',
    '-(2 * (23/(33))- 23 * (23))',
    '-2 * (23/(33))- 23 * (23)',
    '2 * (23/(33))- 23 * (23)',
    '(((-3)))',
    '-(5+6)',
    '-(-1)',
    '(((3)))',
    '-1*1234*(((-1)))*(-1)',
    '-1*1234*(((-1)))/(-1)',
    '-1*1234*(((-1)))',
    '1+1+1+3',
    '(1+1+1-(3+4)*5)/5',
    '1+1+1-(3+4)*5',
    '1 / 1 / 1 + 5',
    '1+2+3+4-4-3-2-1',
    '1*2*3*4/4/3/2/1',
    '10 + (2 * (7 + ((4 + 1 + 3) * 3) / 9)) * 1',
    '10 + 1 * (((3 * (1 + 3 + 4)) / 9 + 7) * 2)',
    '10 + ((7 + (3 * (1 + 3 + 4)) / 9) * 2) * 1'
])

# Test data }

class TestCalculator(TestCase):
    def test_tokenizer(self):
        print()
        print()
        print('*** Tokenizer test ***')

        all_tokenized_expressions_correct = True

        for i_test_expression in range(0, len(test_expression_set_for_tokenizer_test)):
            test_expression = test_expression_set_for_tokenizer_test[i_test_expression]

            print('Testing the expression: {0}...'.format(test_expression))

            tokenized_expression = tokenize_expression(test_expression)

            print('Tokenized expression: {0}'.format(tokenized_expression_to_str(tokenized_expression)))

            correct_tokenized_expression = tokenized_expressions_of_tokenizer_test[i_test_expression]

            if tokenized_expression == correct_tokenized_expression:
                print('PASS: The tokenized expression is equal to the correct tokenized expression {0}'.format(tokenized_expression_to_str(correct_tokenized_expression)))
            else:
                print('FAIL: The tokenized expression is not equal to the correct tokenized expression {0}'.format(tokenized_expression_to_str(correct_tokenized_expression)))

                all_tokenized_expressions_correct = False

        self.assertTrue(all_tokenized_expressions_correct)

        print()

    def test_infix_to_postfix(self):
        print()
        print()
        print('*** Infix to postfix test ***')

        all_postfix_expressions_correct = True

        for i_test_expression in range(0, len(test_expression_set_for_infix_to_postfix_test)):
            test_expression = test_expression_set_for_infix_to_postfix_test[i_test_expression]

            print('Testing the infix expression: {0}...'.format(test_expression))

            postfix_expression = calculator.infix_to_postfix(tokenize_expression(test_expression))

            print('Postfix expression: {0}'.format(tokenized_expression_to_str(postfix_expression)))

            correct_tokenized_expression = tokenized_expressions_of_infix_to_postfix_test[i_test_expression]

            if postfix_expression == correct_tokenized_expression:
                print('PASS: The postfix expression is equal to the correct postfix expression {0}'.format(tokenized_expression_to_str(correct_tokenized_expression)))
            else:
                print('FAIL: The postfix expression is not equal to the correct postfix expression {0}'.format(tokenized_expression_to_str(correct_tokenized_expression)))

                all_postfix_expressions_correct = False

        self.assertTrue(all_postfix_expressions_correct)

        print()

    def test_calculator(self):
        print()
        print()
        print('*** Calculator test ***')

        all_values_correct = True

        for test_expression in all_test_expressions:
            print('Testing the expression: {0}...'.format(test_expression))

            calculated_value = calculator.calculate_value(test_expression)

            reference_value = float(eval(test_expression))

            # Avoid naive floating point comparison by allowing the calculated and the reference value to be 'close enough'. Otherwise, the accumulation of floating point errors may lead to incorrect deduction
            if math.isclose(calculated_value, reference_value):
                print('PASS: The calculated value {0} and the reference value {1} are close enough'.format(calculated_value, reference_value))
            else:
                print('FAIL: The calculated value {0} and the reference value {1} are not close enough'.format(calculated_value, reference_value))

                all_values_correct = False

        self.assertTrue(all_values_correct)

        print()

    # Consider creating a test case that generates random test expressions and saves the generated test expressions into a file. Examples:
    #   https://softwareengineering.stackexchange.com/questions/195813/generating-random-math-expression
    #   https://www.perlmonks.org/bare/?node_id=6114

if __name__ == '__main__':
    main()
