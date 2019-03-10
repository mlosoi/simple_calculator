from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello from Python! {0}'.format(request.GET['query']))
    # return render(request, "index.html")