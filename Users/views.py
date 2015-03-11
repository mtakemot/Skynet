from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from Users.models import Category, Page, UserProfile, UserFactory
from Users.forms import CategoryForm, UserForm, UserProfileForm, RepForm, ServiceForm, DisplayForm, BillForm, BundleForm as bForm, BundleServForm, CustomerForm, CustomerInfoForm
from Packages.models import Service, Bundle
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.
from django.contrib.auth.models import User



def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key bold message is the same as {{ boldmessage }} in the template!
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    user_form = UserProfileForm()

    #profile_form = UserProfileForm(data=request.POST)

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    #adding requirement 10, autoemail. We need to allow user to set a threshold.
    if request.method == 'POST':

        user_form = UserProfileForm(data=request.POST)
        #print("user_form first: ", user_form)

        value = request.POST['maxVal']
        #not sure what it means BUT,
        current_user = UserProfile.objects.get(user=request.user)
        print(current_user.username)
        print("testing last login date", current_user.user.last_login)
        if(value):
            if(int(value)>=0):
                temp = int(value)
                current_user.threshold = temp
                threshold = temp
                current_user.save()
        print("threshold in DB is: " ,current_user.threshold)
        # print("User: ", current_user.user, " threshold is now: ", current_user.threshold)
        # if current_user.balance > current_user.threshold:
        #     print("comparing int str??")

    if request.method == 'GET':
        print("loading index.html from GET")

    try:
        threshold = (UserProfile.objects.get(user=request.user)).threshold
        custType =(UserProfile.objects.get(user=request.user)).custType
    except TypeError:
        threshold = 0
        custType=''


    # return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
    #                                                      'bundle_form': bundle_form.bundle_services.all()})

    return render(request, 'Users/index.html', {'categories': category_list, 'user_form': user_form, 'thresholdvalue':threshold, 'custType': custType})

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
        if user_form.is_valid() and profile_form.is_valid() and registered == False:
            # Save the user's form data to the database.
            user = user_form.save()

            #call the userFactory

            user.first_name = request.POST['fname']
            user.last_name = request.POST['lname']
            user.email = request.POST['email']
            user.website = request.POST['website']
            user.custType = request.POST['custType']
            user.phoneNumber = request.POST['phoneNumber']


            try:
                user.address = request.POST['address']
            except:
                print("address not correct")





            print(user.first_name)
            print(user.last_name)

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = UserFactory(user)
            #profile.custType=custType
            # profile = UserFactory(user)

            print("in views, exited factory call")
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            # profile = profile_form.save(commit=False)
            # profile.user = user
            # profile.username = user
            # profile.fname = user.first_name
            # profile.lname = user.last_name
            # profile.userEmail = user.email
            # profile.website=user.website
            #profile.picture = request.POST['picture']



            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            #profile.is_Market = False

            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        #elif user_form.is_valid() and profile_form.is_valid() and registered == False:
            #return render(request, '/Users/login.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
            return redirect('/Users/login/')

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
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})



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
                # debug to see user information


                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                print(request.user)
                current_user = UserProfile.objects.get(user=request.user)
                current_user.save()
                print(current_user.is_Market)

                if current_user.is_Market:
                    return HttpResponseRedirect('/Users/market_rep')
                if current_user.is_Service:
                    return HttpResponseRedirect('/Users/cust_serv')

                else:
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
    current_user = UserProfile.objects.get(user=request.user)

    #only allow access to customers, redirect market rep and cust serv reps
    redirect = check_permission(current_user)
    if redirect!=False:
        return redirect
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    #current_user = UserProfile.objects.get(user=request.user)


    #only allow access to customers, redirect market rep and cust serv reps
    #redirect = check_permission(current_user)
    #if redirect!=False:
    #   return redirect
     # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    # CHANGE THIS EVENTUALLY TO HOME PAGE
    return HttpResponseRedirect('/Users/')

@login_required
def add_bundle(request):
    current_user = UserProfile.objects.get(user=request.user)
    redirect = check_permission(current_user)
    if redirect!=False:
        return redirect


    if request.method == 'POST':
        try:
            bundle_name = request.POST.getlist('bundle')
            print(bundle_name)
        except MultiValueDictKeyError:
            return HttpResponseRedirect("/Users/add_bundles/")
        bundle_form2=RepForm()
        bundle_form2.bundle_services = bundle_name
        for services in current_user.bundles.all():
            for y in bundle_form2.bundle_services:
                if services.name == y:
                    print("Can't add duplicate services")
                   # return HttpResponseRedirect("/Users/cust_serv/")

        for x in Bundle.objects.all():
            for y in bundle_form2.bundle_services:
                if x.name == y:
                    current_user.bundles.add(x)
                    current_user.balance += x.price
                    current_user.save()


     #   for bundle in current_user.bundles.all():
      #      if bundle.name == bundle_name:
      #          print("Can't add duplicate bundles")
      #          return HttpResponseRedirect("/Users/add_bundles/")

      #  for bundle in Bundle.objects.all():
      #      if bundle.name == bundle_name:
      #          current_user.balance+=bundle.price
      #          current_user.bundles.add(bundle)
      #          current_user.save()
      #          print ("added bundle successfully")

        return HttpResponseRedirect('/Users/view_bill')

    else:

        bundle_form = bForm();
        bundle_form.bundles = Bundle.objects.all()

        for bundles in bundle_form.bundles:
            if bundles.deleted==False:
                print(bundles)


        return render(request, 'Users/add_bundles.html', {'bundle_form': bundle_form.bundles.filter(deleted=False)})


@login_required
def add_services(request):
    #if the request on this page coming after loading and from a user input:
    current_user = UserProfile.objects.get(user=request.user)


    #only allow access to customers, redirect market rep and cust serv reps
    redirect = check_permission(current_user)
    if redirect!=False:
        return redirect


    if request.method == 'POST':
        #from our HTML, the button selected is passed here in terms of the Service
        #object's name field from the html code: value="{{service.name}}"
        #this will just copy the name locally so that we can iterate through the
        #Service database and find the object with matching name.
        try:
            service_name = request.POST.getlist('service')
            print(service_name)
        except MultiValueDictKeyError:
            return HttpResponseRedirect("/Users/add_services/")

        bundle_form2=BundleServForm()
        bundle_form2.bundle_services = service_name
        for services in current_user.services.all():
            for y in bundle_form2.bundle_services:
                if services.name == y:
                    print("Can't add duplicate services")
                    #return HttpResponseRedirect("/Users/cust_serv/")

        for x in Service.objects.all():
            for y in bundle_form2.bundle_services:
                if x.name == y:
                    current_user.services.add(x)
                    current_user.balance += x.price
                    current_user.save()
        print("0")
        # for services in Service.objects.all():
        #     if services.name == service_name:
        #         current_user.balance+=services.price
        #         current_user.services.add(services)
        #         current_user.save()
        #     else:
        #         print("invalid service. Cannot add to your account")

        # if the service exists in user package, render page
       # for services in current_user.services.all():
       #     if services.name == service_name:
       #         print("Can't add duplicate services")
       #         return HttpResponseRedirect("/Users/add_services/")

       # for services in Service.objects.all():
       #     if services.name == service_name:
       #         current_user.balance+=services.price
       #         current_user.services.add(services)
       #         current_user.save()
       #         print ("added service successfully")



        # redirect = check_permission(current_user)
        # if redirect:
        #     return redirect

        current_user.save()

        # current_user.services.add(service)
        # current_user.services.balance = service.price

        print("HEHE")
        print (current_user.user)
        print("HAHAH")

        #updates current user's list of services, and
        return HttpResponseRedirect('/Users/view_bill')


        #this grabs which package the user chose
    else:
        #just render the page the first time
        print("hello")
        service_form = DisplayForm()

        #passing to the HTML ALL the contents in the Service database
        service_form.services = Service.objects.all()

        #bundle_form = bForm();
        #bundle_form.bundles = Bundle.objects.all()
        for service in service_form.services:
            if service.deleted==False:
                print(service)
        #print(service_form.services.filter(deleted=False))

        return render(request, 'Users/add_services.html', {'service_form': service_form.services.filter(deleted=False)})

@login_required
def display_services(request):
    current_user = UserProfile.objects.get(user=request.user)

    #only allow access to customers, redirect market rep and cust serv reps
    redirect = check_permission(current_user)
    if redirect!=False:
        return redirect


    #print (current_user.user)
    #print (current_user.services.all())
    service_form = DisplayForm()
    service_form.services = current_user.services
    return render(request, 'Users/display_services.html', {'display_services': service_form.services.all()})

@login_required
def view_bill(request):
    current_user = UserProfile.objects.get(user=request.user)


    #only allow access to customers, redirect market rep and cust serv reps
    redirect = check_permission(current_user)
    if redirect!=False:
        return redirect

    current_user = UserProfile.objects.get(user=request.user)


    #only allow access to customers, redirect market rep and cust serv reps
    redirect = check_permission(current_user)
    if redirect:
        return redirect


    bill_form = BillForm()
    bill_form.services = current_user.services.all()
    bundle_form = bForm()
    bundle_form.bundles = current_user.bundles.all()
    cost = 0
    for service in current_user.services.all():
        print(service)
        cost += service.price
    for bundle in current_user.bundles.all():
        cost += bundle.price

    if request.method == 'POST':
        value = request.POST['maxVal']
        #not sure what it means BUT,
        if(value):
            if(int(value)>=0):
                temp = int(value)
                current_user.threshold = temp
                current_user.save()

    return render(request, 'Users/view_bill.html', {'threshold':current_user.threshold, 'term_fees': current_user.term_fees, 'display_bundles': bundle_form.bundles.all(), 'display_services': bill_form.services, 'total':current_user.balance})

@login_required
def delete_bundles(request):
    current_user = UserProfile.objects.get(user=request.user)

    #only allow access to customers, redirect market rep and cust serv reps
    redirect = check_permission(current_user)
    if redirect!=False:
        return redirect

    if request.method == 'POST':
        try:
            bundle = request.POST.getlist('bundle')
        except MultiValueDictKeyError:
            return HttpResponseRedirect("/Users/delete_bundle/")

        bundle_form2=RepForm()
        bundle_form2.bundles = bundle
        for x in Bundle.objects.all():
            for y in bundle_form2.bundles:
                if x.name == y:
                    current_user.balance -= x.price
                    current_user.term_fees += x.term_fee
                    current_user.bundles.remove(x)
                    current_user.save()



        #updates current users new attribute
        return HttpResponseRedirect('/Users/view_bill')


        #this grabs which package the user chose
    else:

        bundle_form = bForm()
        bundle_form.bundles = current_user.bundles.all()
        return render(request, 'Users/delete_bundles.html', {'bundle_form': bundle_form.bundles.all()})

@login_required
def delete_services(request):
    current_user = UserProfile.objects.get(user=request.user)

    #only allow access to customers, redirect market rep and cust serv reps
    redirect = check_permission(current_user)
    if redirect!=False:
        return redirect

    if request.method == 'POST':
        try:
            package = request.POST.getlist('service')
        except MultiValueDictKeyError:
            return HttpResponseRedirect("/Users/delete_services/")


        bundle_form2=BundleServForm()
        bundle_form2.bundle_services = package
            #for services in userToChange.services.all():
            #    for y in bundle_form2.bundle_services:
            #         if services.name == y:
            #             print("Can't add duplicate services")
            #             return HttpResponseRedirect("/Users/cust_serv/")

        for x in Service.objects.all():
            for y in bundle_form2.bundle_services:
                if x.name == y:
                    
                    current_user.services.remove(x)
                    current_user.balance -= x.price
                    current_user.term_fees += x.term_fee
                    current_user.save()


        #updates current users new attribute
        return HttpResponseRedirect('/Users/view_bill')


        #this grabs which package the user chose
    else:

        service_form = DisplayForm()
        service_form.services = current_user.services.all()
        return render(request, 'Users/delete_services.html', {'service_form': service_form.services})

@login_required
def market_rep(request):

    current_user = UserProfile.objects.get(user=request.user)

    #only allow access to customers, redirect market rep and cust serv reps
    if current_user.is_Market == False:
        redirect = check_permission(current_user)
        if(not redirect):
            return HttpResponseRedirect("/Users/")

        return redirect

    print(current_user.is_Market)
    service_form = DisplayForm()
    service_form.services = Service.objects.all()
    bundle_form = ServiceForm()
    bundle_form.bundle_services = Bundle.objects.all()

    if request.method == 'POST':

        button = request.POST['submit']

        if button == 'Create Service':

            service_name = request.POST['name']
            if service_name == '':
                return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                         'bundle_form': bundle_form.bundle_services.all()})

                #if render!='':
                    #return render

            service_description = request.POST['description']
            if service_description == '':
                return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                         'bundle_form': bundle_form.bundle_services.all()})

            service_price = request.POST['price']
            if service_price == '':
                return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                         'bundle_form': bundle_form.bundle_services.all()})

            service_term = request.POST['term']
            if service_term == '':
                return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                         'bundle_form': bundle_form.bundle_services.all()})


            service_duration = request.POST['duration']
            if service_term =='':
                return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                         'bundle_form': bundle_form.bundle_services.all()})

            newService = Service(name=service_name,description=service_description,
                                 price=service_price,term_fee=service_term, duration=service_duration)

            newService.save()

            service_form = DisplayForm()
            service_form.services = Service.objects.all()
            bundle_form = ServiceForm()
            bundle_form.bundle_services = Bundle.objects.all()

            return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                         'bundle_form': bundle_form.bundle_services.all()})


        elif button == 'Delete Service':

            #from our HTML, the button selected is passed here in terms of the Service
            #object's name field from the html code: value="{{service.name}}"
            #this will just copy the name locally so that we can iterate through the
            #Service database and find the object with matching name.
            try:
                package_name = request.POST['service']
            except MultiValueDictKeyError:
                return HttpResponseRedirect("/Users/market_rep/")

            print(package_name)

            for services in Service.objects.all():
                if services.name == package_name:
                    package = services
                    if((checkUsersforSubscribedService(services.name))):
                        for service in (Service.objects.filter(name=package_name)):
                            service.deleted=True
                            print(service)
                            service.save()
                    else:
                        print(package)
                        Service.objects.filter(name=package_name).delete()
                        print("deleting Service object with name: ", package_name)



            print("testing package name after searching in Service table: ", package.name)
            print (request.user)

            current_user = UserProfile.objects.get(user=request.user)
            current_user.save()

            #current_user.services.add(package)
            return HttpResponseRedirect('/Users/market_rep')

        elif button == 'Delete Bundle':

            try:
                bundle_name = request.POST['bundle']
            except MultiValueDictKeyError:
                return HttpResponseRedirect("/Users/market_rep/")
            print("deleting bundle: ", bundle_name)
            for bundle in Bundle.objects.all():
                if bundle.name == bundle_name:
                    if((checkUserforSuscbibedBundle(bundle.name))):
                        for bundles in (Bundle.objects.filter(name=bundle_name)):
                            bundles.deleted=True
                            print(bundles)
                            bundles.save()
                    else:
                        Bundle.objects.filter(name=bundle_name).delete()
                        print("deleting bundle object with name: ", bundle_name)

            current_user = UserProfile.objects.get(user=request.user)
            current_user.save()
            return HttpResponseRedirect('/Users/market_rep')

        elif button == 'Add Bundle Service':
            try:
                bundle_name = request.POST['bundle']
            except MultiValueDictKeyError:
                return HttpResponseRedirect("/Users/market_rep/")
            for bundle in Bundle.objects.all():
                if bundle.name == bundle_name:
                    #package = bundle
                    bundle_form2 = BundleServForm()
                    bundle_form2.bundle_services = request.POST.getlist('bservice')
                    newBundle = Bundle.objects.get(name=bundle_name)
                    for x in Service.objects.all():
                        for y in bundle_form2.bundle_services:
                            if x.name == y:
                                print (x.name)
                                newBundle.bundle_services.add(x)


            for x in Service.objects.all():
                for y in bundle_form2.bundle_services:
                    if x.name == y:
                            #bundle.save()
                        #print("match")
                        #print(x.name)
                        #print(y)

                        newBundle.bundle_services.add(x)

            service_form = DisplayForm()
            service_form.services = Service.objects.all()
            bundle_form = ServiceForm()
            bundle_form.bundle_services = Bundle.objects.all()


            return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                             'bundle_form': bundle_form.bundle_services.all()})
            # Bundle.objects.filter(name=bundle_name).add()
            #print("deleting bundle object with name: ", bundle_name)

        elif button == 'Create Bundle':
            bundle_form2=BundleServForm()

            try:
                bundle_name = request.POST['name']
                bundle_description = request.POST['description']
                bundle_price = request.POST['price']
                bundle_term = request.POST['term']
                bundle_duration = request.POST['duration']
            except:
                HttpResponseRedirect('Users/market_rep.html')

            print(bundle_name)

            bundle_form2.bundle_services = request.POST.getlist('bservice')

            try:
                newBundle = Bundle(name = bundle_name, description=bundle_description,price=bundle_price,
                               term_fee=bundle_term, duration=bundle_duration)

                newBundle.save()
            except ValueError:
                HttpResponseRedirect('Users/market_rep.html')


            for x in Service.objects.all():
                for y in bundle_form2.bundle_services:

                    if x.name == y:

                        print("match")
                        print(x.name)
                        print(y)
                        newBundle.bundle_services.add(x)


            service_form = DisplayForm()
            service_form.services = Service.objects.all()
            bundle_form = ServiceForm()
            bundle_form.bundle_services = Bundle.objects.all()

            return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                         'bundle_form': bundle_form.bundle_services.all()})
    else:

        return render(request, 'Users/market_rep.html', {'service_form': service_form.services.all(),
                                                         'bundle_form': bundle_form.bundle_services.all()})
@login_required                                                    #.bundle_services.all()})
def cust_serv(request):
    current_user = UserProfile.objects.get(user=request.user)
    if current_user.is_Service == False:
        redirect = check_permission(current_user)
        if(not redirect):
            return HttpResponseRedirect("/Users/")
        return redirect

    customer_form = CustomerForm()
    customer_form.users = UserProfile.objects.all().filter(is_Market=False, is_Service=False)
    service_form = DisplayForm()
    service_form.services = Service.objects.all()
    bundle_form = ServiceForm()
    bundle_form.bundle_services = Bundle.objects.all()

    if request.method == 'POST':

        try:
            button = request.POST['submit']
            customer = request.POST['customer']
        except MultiValueDictKeyError:
            return HttpResponseRedirect("/Users/cust_serv")

        userToChange = UserProfile.objects.get(username=customer)

        print(userToChange)
        print(userToChange.balance)

        if button == 'Delete Service':
            bundle_form2=BundleServForm()
            bundle_form2.bundle_services = request.POST.getlist('service')
            #for services in userToChange.services.all():
            #    for y in bundle_form2.bundle_services:
            #         if services.name == y:
            #             print("Can't add duplicate services")
            #             return HttpResponseRedirect("/Users/cust_serv/")

            for x in Service.objects.all():
                for y in bundle_form2.bundle_services:
                    if x.name == y:
                        try:
                            userToChange.services.get(name=y)
                        except:
                            continue

                        print(userToChange.balance)
                        userToChange.services.remove(x)
                        userToChange.balance -= x.price
                        userToChange.term_fees += x.term_fee
                        userToChange.save()
                        print(userToChange.balance)


        elif button == 'Add Service':
            bundle_form2=BundleServForm()
            bundle_form2.bundle_services = request.POST.getlist('service')
            for services in userToChange.services.all():
                for y in bundle_form2.bundle_services:
                    if services.name == y:
                        print("Can't add duplicate services")
                        #return HttpResponseRedirect("/Users/cust_serv/")

            for x in Service.objects.all():
                for y in bundle_form2.bundle_services:
                    if x.name == y and  not x.deleted:
                        userToChange.services.add(x)
                        userToChange.balance += x.price
                        userToChange.save()

        elif button == 'Delete Bundle':
            bundle_form2=RepForm()
            bundle_form2.bundles=request.POST.getlist('bundle')

            #for services in userToChange.services.all():
            #    for y in bundle_form2.bundle_services:
            #         if services.name == y:
            #             print("Can't add duplicate services")
            #             return HttpResponseRedirect("/Users/cust_serv/")

            for x in Bundle.objects.all():
                for y in bundle_form2.bundles:
                    if x.name == y:
                        try:
                            userToChange.bundles.get(name=y)
                        except:
                            continue
                        userToChange.bundles.remove(x)
                        userToChange.balance -= x.price
                        userToChange.term_fees   += x.term_fee
                        userToChange.save()

        elif button == 'Add Bundle':
            bundle_form2=RepForm()
            bundle_form2.bundles=request.POST.getlist('bundle')


            for bundle in userToChange.bundles.all():
                for y in bundle_form2.bundles:
                    if bundle.name == y:
                        print("Can't add duplicate bundles")
                        #return HttpResponseRedirect("/Users/cust_serv/")

            for x in Bundle.objects.all():
                for y in bundle_form2.bundles:
                    if x.name == y and not x.deleted:
                        userToChange.bundles.add(x)
                        userToChange.balance += x.price
                        userToChange.save()

        return render(request, 'Users/cust_serv.html', {'bundle_form': bundle_form.bundle_services.all(), 'customer_form': customer_form.users.all(), 'service_form': service_form.services.all()})








    else:
        return render(request, 'Users/cust_serv.html', {'bundle_form': bundle_form.bundle_services.all(), 'customer_form': customer_form.users.all(), 'service_form': service_form.services.all()})


def customer_page(request, customer):
    current_user = UserProfile.objects.get(username=customer)
    print(customer)
    if request.method == 'POST':
        button = request.POST['submit']


        if button == 'Delete Service':
            service_name = request.POST['service']
            print("service being deleted")
            for service in current_user.services.all():
                if (service.name == service_name):
                    current_user.services.remove(service)
                    current_user.balance-=service.price
                    current_user.save()
                    return customer_page(request, current_user.username)


    return render(request, 'Users/customer_page.html', {'Customer': current_user.username, 'services_form': current_user.services.all()})
    #only allow access to customers, redirect market rep and cust serv reps

@login_required
def customerInfoPage(request):

    current_user = UserProfile.objects.get(user=request.user)
    if current_user.is_Service == True or current_user.is_Market == True:
        redirect = check_permission(current_user)
        if(not redirect):
            return HttpResponseRedirect("/Users/")
        return redirect

    if request.method=='GET':

        customer_form = CustomerInfoForm
        customer_form.user = current_user
      #  customer_form.fname = current_user.fname
      #  customer_form.lname = current_user.lname
      #  customer_form.address = current_user.address
      #  customer_form.phoneNumber = current_user.phoneNumber

        return render(request, 'customer_info.html', {'customer_form': current_user})
    else:
        return HttpResponseRedirect('/Users/')
    #return render(request, '/Users/customer_info.html',{'Customer': customer_form})




def check_permission(UserProfile):

    if UserProfile.is_Market:
        return HttpResponseRedirect('/Users/market_rep')

    elif UserProfile.is_Service:
        return HttpResponseRedirect('/Users/cust_serv')

    else:
        return False

def checkUsersforSubscribedService(ServicesName):
    allUsers = UserProfile.objects.all().filter(is_Market=False, is_Service=False)
    for user in allUsers:
        for service in user.services.all():
            if(service.name == ServicesName):
                #service.deleted=True
                return True

    return False

def checkUserforSuscbibedBundle(BundleName):
    allUsers = UserProfile.objects.all().filter(is_Market=False, is_Service=False)
    for user in allUsers:
        for bundles in user.bundles.all():
            if(bundles.name == BundleName):
                #service.deleted=True
                return True

    return False
#def validate_views(obj, ):
    #if render_loc!='':
        #return render_loc

