from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm, PageForm, NameForm, ContactForm
from utils import send_email
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


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # have we been provided with valid form
        if form.is_valid():
            form.save(commit=True)
            #call index view which is home page
            return index(request)
        else:
            print form.errors
    else:
        #if not post request display the form again
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form':form})
#add page view

def add_page(request, cat_name_slug):
    try:
        cat = Category.objects.get(slug=cat_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        pageForm = PageForm(request.POST)
        if pageForm.is_valid():
            if cat:
                page = pageForm.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                #use a redirct here
                return category(request, cat_name_slug)
        else:
            print pageForm.errors
    else:
        pageForm = PageForm()
    context_dict = {'form':pageForm, 'category':cat}
    return render(request, 'rango/add_page.html', context_dict)



def your_name(request):
    if request.method == 'POST':
        nameForm = NameForm(request.POST)
        if nameForm.is_valid():
            category_list = Category.objects.order_by('-likes')[:5]
            context_dict = {'boldmessage':"I am bold arshad from the context",
                    'categories':category_list}
            yourName = nameForm.cleaned_data['your_nam'].encode('UTF-8')
            context_dict['yourName'] = yourName
            return render(request, 'rango/index.html', context_dict)

            #print nameForm.cleaned_data
            #print 'Content ', nameForm.cleaned_data['your_nam'].encode('UTF-8')
            #process the data in form.cleaned_data
            return HttpResponse("Thanks for submitting a form")
    else:
        form = NameForm()
        context_dict = {}
        #category_list = Category.objects.order_by('-likes')[:5]
        #context_dict = {'boldmessage':"I am bold arshad from the context",'categories':category_list}
        context_dict['form'] = form
    return render(request, 'rango/your_name.html', context_dict)


def contactFormView(request):
    if request.method == 'POST':
        contactForm = ContactForm
        if contactForm.is_valid():
            subject = contactForm.cleaned_data['subject']
            message = contactForm.cleaned_data['message']
            sender = contactForm.cleaned_date['sender']
            cc_myself = contactForm.cleaned_data['cc_myself']
            recipients = ['arshad2k7@gmail.com']
            if cc_myself:
                recipients.append(sender)
            #send_email(recipients)
            return HttpResponse("Inside contact form")
    else:
        form = ContactForm()
        context_dict = {}
        context_dict['form'] = form
        return render(request, 'rango/contactus_form.html', context_dict)
        #return HttpResponse("Inside contact form")