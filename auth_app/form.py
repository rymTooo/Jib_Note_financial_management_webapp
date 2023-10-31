from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    fname = forms.CharField(max_length=50)
    lname = forms.CharField(max_length=50)
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)   
    email = forms.EmailField(max_length=100)

    

class RegisterForm(UserCreationForm):
    class Meta:# like a setting page for the form: choose element to display, what kind of obejct to create from a form, cosmetic stuff.
        model=User# this form will create user
        fields = ['username','email','password1','password2'] #which field is needed to craete user