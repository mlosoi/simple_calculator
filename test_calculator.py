from unittest import TestCase
from unittest import main

import math

import calculator

calculator.print_debug_output = False

class TestCalculator(TestCase):
    test_expressions = [
        '-(-(-(-10)))',
        '-4',
        '-1*1234*(((-1)))*(-1)+1234',
        '-1*1234*(((-1)))*(-1)',
        '1+1+(1+3)+4*5',
        '-(2 * (23/(33))- 23 * (23))',
        '-2 * (23/(33))- 23 * (23)',
        '2 * (23/(33))- 23 * (23)',
        '1+1',
        '(((-3)))',
        '-(5+6)',
        '-(-1)',
        '(((-3)))',
        '-1*1234*(((-1)))*(-1)',
        '-1*1234*(((-1)))/(-1)',
        '-1*1234*(((-1)))',
        '1+1+1+3',
        '(1+1+1-(3+4)*5)/5',
        '1+1+1-(3+4)*5',
        '1 / 1 / 1 + 5'
    ]

    def test_calculator(self):
        all_values_correct = True

        for test_expression in self.test_expressions:
            print('Testing the expression: {0}...'.format(test_expression))

            calculated_value = calculator.calculate_value(test_expression)

            reference_value = float(eval(test_expression))

            if math.isclose(calculated_value, reference_value):
                print('PASS: The calculated value {0} and the reference value {0} are close enough'.format(calculated_value, reference_value))
            else:
                print('FAIL: The calculated value {0} and the reference value {0} are not close enough'.format(calculated_value, reference_value))

                all_values_correct = False

        self.assertTrue(all_values_correct)

    # Consider creating a test case that generates random test expressions

if __name__ == '__main__':
    main()
