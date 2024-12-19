from django import forms
from django.contrib.auth.forms import AuthenticationForm
from api.models import CustomUser


# Registration form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label='Password',
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label='Confirm Password',
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'grade', 'category', 'school']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Enter username'}),
        label='Username',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label='Password',
    )
