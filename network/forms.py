from .models import User
from django import forms

class RegisterForm(forms.ModelForm):
    username = forms.TextInput()
    email = forms.EmailField()
    attrs = { 
        "type" : 'password'
    }
    password = forms.CharField(widget=forms.TextInput(attrs=attrs))
    confirm = forms.CharField(widget=forms.TextInput(attrs=attrs))
    class Meta:
        model = User
        fields = ['username','email','password']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    attrs = {
        "type": "password"
    }
    password = forms.CharField(widget=forms.TextInput(attrs=attrs))