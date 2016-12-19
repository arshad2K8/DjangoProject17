from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
# Create your views here.


def index(request):
    #return HttpResponse("Rango Says Hello World")

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'boldmessage':"I am bold arshad from the context",
                    'categories':category_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("About rango mmm lemme think")

