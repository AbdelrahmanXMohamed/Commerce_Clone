from  django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='',widget=forms.TextInput(attrs={
        "placeholder":"Username"
    }))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={
        "placeholder":"Password"
    }))

class RegisterForm(forms.Form):
    username = forms.CharField(label='',widget=forms.TextInput(attrs={
        "placeholder":"Username"
    }))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={"placeholder":"Email Address"}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={
        "placeholder":"Password"
    }))
    confirmation = forms.CharField(label='',widget=forms.PasswordInput(attrs={
        "placeholder":"Confirm Password"
    }))
