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



def category(request, cat_name_slug):
    try:
        context_dict = {}
        category = Category.objects.get(slug=cat_name_slug)
        context_dict['category'] = category
        context_dict['category_name'] = category.name
        context_dict['slug_category_name'] = cat_name_slug
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html',context_dict)