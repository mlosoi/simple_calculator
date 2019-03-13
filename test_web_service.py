import base64
import json
import math

from unittest import TestCase
from unittest import main
from urllib.request import urlopen

import test_calculator

class TestWebService(TestCase):

    web_service_endpoint = 'https://mlosoi-simple-calculator.herokuapp.com/calculus'

    query_url_parameter_identifier = 'query'

    response_error_identifier = 'error'

    response_value_identifier = 'value'

    def test_missing_query_parameter(self):
        print()
        print()
        print('*** Missing query parameter test ***')

        print('Calling the endpoint {0} without a URL parameter'.format(self.web_service_endpoint))

        response = json.loads(urlopen(self.web_service_endpoint).read().decode('utf-8'))

        print('Response: {0}'.format(response))

        self.assertTrue(response['error'])

    def test_invalid_base64_encoding(self):
        print()
        print()
        print('*** Invalid base64 encoding test ***')

        invalid_base64_encoding_string = '12345'

        # Construct the API call URL
        api_call_url = '{0}?{1}={2}'.format(self.web_service_endpoint, self.query_url_parameter_identifier, invalid_base64_encoding_string)

        print('Calling the API in the URL: {0}'.format(api_call_url))

        # Transform the JSON response string into a Python dictionary
        response = json.loads(urlopen(api_call_url).read().decode('utf-8'))

        print('Response: {0}'.format(response))

        self.assertTrue(response['error'])

    def test_correct_expressions(self):
        print()
        print('*** Web service test ***')
        print()

        all_values_correct = True

        for test_expression in test_calculator.all_test_expressions:
            print('Testing the expression: {0}...'.format(test_expression))

            # Transform the expression into a base64-encoded string
            base64_encoded_test_expression = base64.b64encode(bytes(test_expression, 'utf-8')).decode('utf-8')

            print('Base64-encoded expression: {0}'.format(base64_encoded_test_expression))

            # Construct the API call URL
            api_call_url = '{0}?{1}={2}'.format(self.web_service_endpoint, self.query_url_parameter_identifier, base64_encoded_test_expression)

            print('Calling the API in the URL: {0}'.format(api_call_url))

            # Transform the JSON response string into a Python dictionary
            response = json.loads(urlopen(api_call_url).read().decode('utf-8'))

            print('Response: {0}'.format(response))

            if not response[self.response_error_identifier]:
                calculated_value = response[self.response_value_identifier]

                reference_value = float(eval(test_expression))

                # Avoid naive floating point comparison by allowing the calculated and the reference value to be 'close enough'. Otherwise, the accumulation of  floating point errors may lead to incorrect deduction
                if math.isclose(calculated_value, reference_value):
                    print('PASS: The calculated value {0} and the reference value {1} are close enough'.format(calculated_value, reference_value))
                else:
                    print('FAIL: The calculated value {0} and the reference value {1} are not close enough'.format(calculated_value, reference_value))

                    all_values_correct = False

            else:
                print('FAIL: There was an error evaluating the expression')

                all_values_correct = False

        self.assertTrue(all_values_correct)

        print()

if __name__ == '__main__':
    main()
