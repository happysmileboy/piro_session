from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'email', 'placeholder': '이메일'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': '비밀번호'}))