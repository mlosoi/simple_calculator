import sys

from base64 import b64decode

from django.http import HttpResponse

sys.path.append('..')

from calculator import calculate_value

def calculus(request):
    infix_expression = b64decode(request.GET['query']).decode('UTF-8')

    value = calculate_value(infix_expression)

    return HttpResponse('{0}'.format(value))
