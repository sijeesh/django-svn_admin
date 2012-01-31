from django import forms


class login_form(forms.Form):
    username=forms.CharField(label='Username',error_messages={'required':'Enter your username'} ,widget=forms.TextInput(attrs={'size':'15'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'size':'15'}),label='Password',error_messages={'required':' Enter your password'})
