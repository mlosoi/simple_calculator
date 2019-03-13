import json
import sys

from base64 import b64decode

from django.http import HttpResponse

sys.path.append('..')

from calculator import calculate_value

def calculus(request):
    infix_exprssion = None

    try:
        infix_expression = b64decode(request.GET['query']).decode('UTF-8')
    except:
        return HttpResponse(json.dumps({'error': True, 'message': 'Failed to decode input expression from the \'query\' URL parameter. Check the parameter'}), content_type = 'application/json')

    try:
        value = calculate_value(infix_expression)

        return HttpResponse(json.dumps({'error': False, 'value': value}), content_type = 'application/json')

    except:
        return HttpResponse(json.dumps({'error': True, 'message': 'Failed to calculate {0}'.format(infix_expression)}), content_type = 'application/json')
