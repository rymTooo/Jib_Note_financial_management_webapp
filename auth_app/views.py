
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterForm,LoginForm

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

def signup2(requests):
    if requests.method == "GET":
        form = RegisterForm()
        return render(requests, 'auth_app/signup_page.html', {"form": form})
    
    # if method is "POST", then retrieve the information from the user
    if requests.method == "POST":
        fname = requests.POST["fname"]
        lname= requests.POST["lname"]
        email= requests.POST["email"]
        #BD= requests.POST["BD"] not be able to add to user yet.
        username= requests.POST["username"]
        password= requests.POST["password"]
        cpassword= requests.POST["cpassword"]
        if User.objects.filter(username = username).exists():# equal to running sql command as "select * from user(table) where username = {given username}" >> so it return a row if it username already exsit and .exist() change result to boolean.
            messages.error(requests, "Username already exist. Please try another one")
            # need to continue with this : https://stackoverflow.com/questions/4482392/how-do-i-raise-a-validationerror-or-do-something-similar-in-views-py-of-my-dja
        
        if User.objects.filter(password = password).exist():
            messages.error(requests, "Password already exist. Please try another one")

        
        if (password == cpassword):# if the password is correct 
            #!!! still need to checck for copy of password and username. !!!
            user = User.objects.create_user(username = username, email = email , password = password)#create a user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request = requests, message = "Yay, succesfully create an account")#message.success is to 
            return redirect("/login")# change url to /login >> will be direct to login_page based on urls.py file.
        else:
            messages.info(request=requests, message= "Your password is not the same.")

    return render(requests, 'auth_app/signup_page.html')

def logout_f(requests):
    logout(requests)
    messages.success(requests, "logout successfully.")
    return redirect("/")

def signup(requests):
    args = {}
    info = {}
    if requests.method == "POST":
        form = LoginForm(requests.POST)
        print(form.non_field_errors)
        if form.is_valid():
            info = form.cleaned_data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            fname = form.cleaned_data["fname"]
            lname = form.cleaned_data["lname"]
            email = form.cleaned_data["email"]
            return redirect("/login", message = info)#{username : "username", password : "password", fname : "fname", lname : "lname", email : "email"})
    else:
        form = LoginForm()
    args['form'] = form

    return render(requests,'auth_app/signup_page.html', args)
