from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    #return HttpResponse("Rango Says Hello World")
    context_dict = {'boldmessage':"I am bold from the context"}
    return render(request, 'rango/index.html', context_dict)

