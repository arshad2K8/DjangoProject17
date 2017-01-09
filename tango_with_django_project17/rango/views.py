from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm, PageForm, NameForm, ContactForm, UserForm, UserProfileForm
from utils import send_email, run_query
from google_search import getSearchUrls
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
# Create your views here.


def index(request):
    #return HttpResponse("Rango Says Hello World")
    #request.session.set_test_cookie()
    #category_list = Category.objects.order_by('-likes')[:5]
    category_list = Category.objects.all()
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage':"I am bold arshad from the context",
                    'categories':category_list, 'pages':page_list}

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit = False
    last_visit = request.session.get('last_visit')
    #response = render(request, 'rango/index.html', context_dict)

    # does the cookie last_visit exists
    if last_visit:
        #if it does get the cookies value
        #cast it to python data time object
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # if its more than a day since the last visit
        if (datetime.now() - last_visit_time).seconds > 0:
            visits += 1
            reset_last_visit = True
    else:
        # last_visit cookie doesnt exist
        reset_last_visit = True

    if reset_last_visit:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits
    response = render(request, 'rango/index.html', context_dict)
    #return render(request, 'rango/index.html', context_dict)
    return response


def about(request):
    # If the visits session varible exists, take it and use it.
# If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    #return HttpResponse("About rango mmm lemme think")
    return render(request, 'rango/about.html', {'count':count})



def category(request, cat_name_slug):

    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            context_dict['query'] = query.strip()
            result_list = getSearchUrls(query)
            context_dict['result_list'] = result_list
    try:
        category = Category.objects.get(slug=cat_name_slug)
        context_dict['category'] = category
        context_dict['category_name'] = category.name
        context_dict['slug_category_name'] = cat_name_slug
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass
    if not context_dict['query']:
        context_dict['query'] = category.name
    return render(request, 'rango/category.html',context_dict)

@login_required
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

@login_required
def add_page(request, cat_name_slug):
    try:
        cat = Category.objects.get(slug=cat_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        pageForm = PageForm(request.POST)
        if pageForm.is_valid():
            print 'page form is valid'
            if cat:
                page = pageForm.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                #use a redirct here
                return category(request, cat_name_slug)
        elif request.POST.get('url') and request.POST.get('title'):
            if cat:
                title = request.POST.get('title').strip()
                url = request.POST.get('url').strip()
                newPage = Page.objects.get_or_create(category=cat, title=title)[0]
                newPage.url = url
                newPage.views = 0
                newPage.save()
                return category(request, cat_name_slug)
        else:
            print 'Errro in page form', pageForm.errors
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
        contactForm = ContactForm(request.POST)
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
        contactForm = ContactForm()
        context_dict = {}
        context_dict['form'] = contactForm
    return render(request, 'rango/contactus_form.html', {'form': contactForm})
        #return HttpResponse("Inside contact form")

# commenting out as we use django ap redux to manage login and logout
def register(request):

    registered = False
    context_dict = {}
    if request.method == 'POST':
        userForm = UserForm(data=request.POST)
        userProfileForm = UserProfileForm(data=request.POST)

        if userForm.is_valid() and userProfileForm.is_valid():
            user = userForm.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            #now sort out the profile form
            profile = userProfileForm.save(commit=False)
            profile.user = user
            #save use profile model instance
            profile.save()
            registered = True
        else:
            print userForm.errors, userProfileForm.errors
    else:
        userForm = UserForm()
        userProfileForm = UserProfileForm()
        #context_dict = {'user_form':userForm, 'profile_form':UserProfileForm, 'registered':registered}
    return render(request, 'rango/register.html', {'user_form':userForm, 'profile_form':UserProfileForm, 'registered':registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # Bad login details were provided. So we can't log the user in.
                print "Invalid login details: {0}, {1}".format(username, password)
                return HttpResponse("Invalid login details supplied.")

    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')


def search(request):
    print 'inside search'
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = getSearchUrls(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET.get('page_id')
            if page_id:
                page = Page.objects.get(id=int(page_id.strip()))
                if page:
                    page.views += 1
                    page.save()
                    return HttpResponseRedirect(page.url)
    return HttpResponseRedirect('/rango/')


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)