import json
import sys

from base64 import b64decode

from django.http import HttpResponse

sys.path.append('..')

from calculator import calculate_value

query_url_parameter_identifier = 'query'

response_error_identifier = 'error'

response_message_identifier = 'message'

response_value_identifier = 'value'

def calculus(request):

    query_url_parameter_value = None

    try:
        query_url_parameter_value = request.GET[query_url_parameter_identifier]
    except KeyError:
        return HttpResponse(json.dumps({response_error_identifier: True, response_message_identifier: 'No {0} URL parameter was given. Supply the parameter'.format(query_url_parameter_identifier)}), content_type = 'application/json')

    infix_exprssion = None

    try:
        infix_expression = b64decode(query_url_parameter_value).decode('UTF-8')
    except:
        return HttpResponse(json.dumps({'error': True, 'message': 'Failed to decode input expression from the {0} URL parameter. Check the parameter'.format(query_url_parameter_identifier)}), content_type = 'application/json')

    value = None

    try:
        value = calculate_value(infix_expression)
    except:
        return HttpResponse(json.dumps({'error': True, 'message': 'Failed to calculate the expression {0}'.format(infix_expression)}), content_type = 'application/json')

    return HttpResponse(json.dumps({'error': False, 'value': value}), content_type = 'application/json')
