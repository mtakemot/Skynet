from django.shortcuts import render
from django.http import HttpResponse
from Users.models import Category, Page, UserProfile
from Users.forms import CategoryForm, UserForm, UserProfileForm, ServiceForm, DisplayForm, BillForm
from Packages.models import Service
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.



def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'Users/index.html', context_dict)

def about(request):
    return HttpResponse("Skynet says this is the about page for users <br/> <a href = '/Users/'>Back to Users</a>")

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'Users/category.html', context_dict)


def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'Users/add_category.html', {'form': form})


def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)

            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.username = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True


        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.

    return render(request,
            'Users/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    print (request.user)
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)


        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/Users/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your User account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'Users/login.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
     # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    # CHANGE THIS EVENTUALLY TO HOME PAGE
    return HttpResponseRedirect('/Users/')

@login_required
def add_package(request):
    #if the request on this page coming after loading and from a user input:
    if request.method == 'POST':
        #from our HTML, the button selected is passed here in terms of the Service
        #object's name field from the html code: value="{{service.name}}"
        #this will just copy the name locally so that we can iterate through the
        #Service database and find the object with matching name.
        package_name = request.POST['service']

        print("testing service's name from user selection: ",package_name)

        for services in Service.objects.all():
            if services.name == package_name:
                package = services

        print("testing package name after searching in Service table: ", package.name)
        print (request.user)

        current_user = UserProfile.objects.get(user=request.user)
        current_user.save()

        current_user.services.add(package)

        print("HEHE")
        print (current_user.user)
        print("HAHAH")

        #updates current user's list of services, and
        return HttpResponseRedirect('/Users/display_services')


        #this grabs which package the user chose
    else:
        #just render the page the first time
        print("hello")
        service_form = DisplayForm()
        #passing to the HTML ALL the contents in the Service database
        service_form.services = Service.objects.all()
        return render(request, 'Users/add_package.html', {'service_form': service_form.services.all()})

@login_required
def display_services(request):

        current_user = UserProfile.objects.get(user=request.user)
        print (current_user.user)
        print (current_user.services.all())
        #for service in current_user.services.all():
          #  print service.name
        service_form = DisplayForm()
        service_form.services = current_user.services
        return render(request, 'Users/display_services.html', {'display_services': service_form.services.all()})

@login_required
def view_bill(request):
    current_user = UserProfile.objects.get(user=request.user)
    bill_form = BillForm()
    bill_form.services = current_user.services.all()
    cost = 0
    for service in current_user.services.all():
        cost += service.price
    return render(request, 'Users/view_bill.html', {'display_services': bill_form.services, 'total': cost})

@login_required
def delete_services(request):
    if request.method == 'POST':
        package = request.POST['package']
        #access current user
        current_user = UserProfile.objects.get(user=request.user)
        newPackage = Service(name=package, description='', price=0, term_fee=0)
        print ("test deleting package name: ")
        print (newPackage.name)
        #adds package to users list of services
         # current_user.services.add(newPackage)

        for service in current_user.services.all():
            if (service.name == newPackage.name):
                #print "testing search for package to delete"
                current_user.services.remove(service)
                #print ("testing IN DELETE: %s", newPackage.name)
                current_user.save()



        #updates current users new attribute
        return HttpResponseRedirect('/Users/display_services')


        #this grabs which package the user chose
    else:
        #just render the page the first time
        #print("hello")
        service_form = ServiceForm()
        return render(request, 'Users/delete_services.html', {'service_form': service_form})