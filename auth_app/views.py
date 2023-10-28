
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# input : requst, output : response == requst handler (input = httprequest, output = httpresponse)


def home(requests):
    return render(requests, 'auth_app/about.html')

def login_f(requests):

    # if login_f invoke while requests method is POST >> check if user can login.
    if requests.method == "POST":
        username= requests.POST["username"]
        password= requests.POST["password"]

        user = authenticate(username = username, password = password) # will return none if password and username doesn't match
        if user is not None:
            login(requests, user) # build in function from django for login
            fname = user.first_name
            return render(requests, "auth_app/about.html", {"fname": fname})# the last part is dictionary added to send data received from the 
        else: # if anything wrong with the login process
            messages.error(request=requests, message="Wrong username or password")

    return render(requests, 'auth_app/login_page.html')

def signup(requests):
    # if method is "POST", then retrieve the information from the user
    if requests.method == "POST":
        fname = requests.POST["fname"]
        lname= requests.POST["lname"]
        email= requests.POST["email"]
        #BD= requests.POST["BD"] not be able to add to user yet.
        username= requests.POST["username"]
        password= requests.POST["password"]
        cpassword= requests.POST["cpassword"]
        if (password == cpassword):# if the password is correct 
            #!!! still need to checck for copy of password and username. !!!
            user = User.objects.create_user(username = username, email = email , password = password)#create a user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request = requests, message = "Yay, succesfully create an account")#message.success is to 
            return redirect("/login")# change url to /login >> will be direct to login_page based on urls.py file.
        else:
            messages.info(request=requests, message= "Check the password")

    return render(requests, 'auth_app/signup_page.html')

def logout_f(requests):
    logout(requests)
    messages.success(requests, "logout successfully.")
    return redirect('home')
