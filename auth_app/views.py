
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterForm,RegisForm2

# input : requst, output : response == requst handler (input = httprequest, output = httpresponse)


def home(request):
    return render(request, 'auth_app/about.html')

def login_f(request):

    # if login_f invoke while requests method is POST >> check if user can login.
    if request.method == "POST":
        username= request.POST["username"]
        password= request.POST["password"]
        user = authenticate(username = username, password = password) # will return none if password and username doesn't match
        if user is not None:
            login(request, user) # build in function from django for login
            fname = user.first_name
            return render(request, "auth_app/about.html", {"fname": fname})# the last part is dictionary added to send data received from the 
        else: # if anything wrong with the login process
            messages.error(request=request, message="Wrong username or password")

    return render(request, 'auth_app/login_page.html')

def signup(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'auth_app/signup_page.html', {"form": form})
    
    # if method is "POST", then retrieve the information from the user
    if request.method == "POST":
        fname = request.POST["fname"]
        lname= request.POST["lname"]
        email= request.POST["email"]
        #BD= requests.POST["BD"] not be able to add to user yet.
        username= request.POST["username"]
        password= request.POST["password"]
        cpassword= request.POST["cpassword"]
        if User.objects.filter(username = username).exists():# equal to running sql command as "select * from user(table) where username = {given username}" >> so it return a row if it username already exsit and .exist() change result to boolean.
            messages.error(request, "Username already exist. Please try another one")
            
        
        if User.objects.filter(password = password).exist():
            messages.error(request, "Password already exist. Please try another one")

        
        if (password == cpassword):# if the password is correct 
            #!!! still need to checck for copy of password and username. !!!
            user = User.objects.create_user(username,email ,password)#create a user input: username, email, password
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request = request, message = "Yay, succesfully create an account")#message.success is to 
            return redirect("/login")# change url to /login >> will be direct to login_page based on urls.py file.
        else:
            messages.info(request=request, message= "Your password is not the same.")

    return render(request, 'auth_app/signup_page.html')




def logout_f(request):
    logout(request)
    messages.success(request, "logout successfully.")
    return redirect("/")




def signup2(request): # this method is a test signup model, but now it is a reference of input value into DB.
    args = {}# use to pass error message and form information incase of any error occur and user have to refill form.
    info = {}
    if request.method == "POST":
        regis_form = RegisForm2(request.POST, request.FILES)
        if regis_form.is_valid():
            regis_form.save()
            info = regis_form.cleaned_data # get a dict of variable from the form. to parse to next page(actually unneccesary but just trying to parse)
            return redirect("/login", message = info)#{username : "username", password : "password", fname : "fname", lname : "lname", email : "email"})
    else:
        regis_form = RegisForm2()
    args['form'] = regis_form # args in action

    return render(request,'auth_app/signup_page.html', args)
