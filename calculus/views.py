import json
import sys

from base64 import b64decode

from django.http import HttpResponse

sys.path.append('..')

from calculator import calculate_value

def calculus(request):
    try:
        infix_expression = b64decode(request.GET['query']).decode('UTF-8')

        value = calculate_value(infix_expression)

        return HttpResponse(json.dumps({'error': False, 'value': value}), content_type = 'application/json')

    except:
        return HttpResponse(json.dumps({'error': True, 'message': 'Failed'}), content_type = 'application/json')
