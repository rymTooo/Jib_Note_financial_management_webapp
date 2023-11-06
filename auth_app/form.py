from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import signup_model

"""
to save a form to DB
1. create model(table) to store data in DB
2. make a form class link to that model by using [class Meta >> model = {model name}]
3. use form.save() to save data to DB
"""
class RegisForm2(forms.ModelForm):
    fname = forms.CharField(max_length=50)
    lname = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    con_password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    class Meta:
        model = signup_model
        fields = ["fname", "lname", "email", "username","password"]
    
    def clean(self):
        
        cleaned_data = self.cleaned_data # get a input from user
        username = cleaned_data["username"]
        password = cleaned_data["password"]
        con_password = cleaned_data["con_password"]

        if signup_model.objects.filter(username = username).exists(): # check if the username already exist
            error_message = "Username '%s' is already exist. Please enter a new one." % username
            raise forms.ValidationError(error_message)
        else:
            if password != con_password: # check if password match
                error_message = "Passwords do not match."
                raise forms.ValidationError(error_message)
            else:
                return cleaned_data
    

class RegisterForm(UserCreationForm):
    class Meta:# like a setting page for the form: choose element to display, what kind of obejct to create from a form, cosmetic stuff.
        model=User# this form will create user
        fields = ['username','email','password1','password2'] #which field is needed to craete user