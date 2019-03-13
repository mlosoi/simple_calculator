import json
import sys

from base64 import b64decode

from django.http import HttpResponse

sys.path.append('..')

from calculator import calculate_value

# Response JSON attribute names {

query_url_parameter_identifier = 'query'

response_error_identifier = 'error'

response_message_identifier = 'message'

response_value_identifier = 'value'

# Response JSON attribute names }

def calculus(request):

    query_url_parameter_value = None

    try:
        # Extract the URL parameter value
        query_url_parameter_value = request.GET[query_url_parameter_identifier]

    except KeyError:
        return HttpResponse(json.dumps({response_error_identifier: True, response_message_identifier: 'No \'{0}\' URL parameter was given. Supply the parameter'.format(query_url_parameter_identifier)}), content_type = 'application/json')

    infix_exprssion = None

    try:
        # Base64 decode the URL parameter value to an infix expresion
        infix_expression = b64decode(query_url_parameter_value).decode('UTF-8')

    except:
        return HttpResponse(json.dumps({response_error_identifier: True, response_message_identifier: 'Failed to decode an input expression from the \'{0}\' URL parameter. Check the parameter value {1}'.format(query_url_parameter_identifier, query_url_parameter_value)}), content_type = 'application/json')

    value = None

    # Consider whether it's possible to give so lengthy expression as input that the HTTP server timeouts the request. Supposedly, there's a max length for a URL as it's discussed here: https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers 

    try:
        # Calculate the given expression
        value = calculate_value(infix_expression)

    except:
        return HttpResponse(json.dumps({response_error_identifier: True, response_message_identifier: 'Failed to calculate the expression {0}'.format(infix_expression)}), content_type = 'application/json')

    return HttpResponse(json.dumps({response_error_identifier: False, response_value_identifier: value}), content_type = 'application/json')
