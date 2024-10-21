from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    login_email = forms.CharField(
        label='Login_Email', 
        required=True, 
        error_messages={'required': 'Это поле обязательно для заполнения'}
    )
    password = forms.CharField(
        label='Пароль:', 
        widget=forms.PasswordInput, 
        min_length=6, 
        max_length=20, 
        error_messages={'required': 'Это поле обязательно для заполнения'}
    )
    remember_me = forms.BooleanField(
        label='Запомнить меня', 
        required=False
    )

class RegisterForm(forms.Form):
    login = forms.CharField(
        label='Login', 
        required=True, 
        error_messages={'required': 'Это поле обязательно для заполнения'}
    )
    email = forms.EmailField(
        label='Email', 
        required=True, 
        error_messages={'required': 'Введите корректный email'}
    )
    password = forms.CharField(
        label='Пароль:', 
        widget=forms.PasswordInput, 
        min_length=6, 
        max_length=20, 
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения'}
    )
    repeat_password = forms.CharField(
        label='Повторите пароль:', 
        widget=forms.PasswordInput, 
        min_length=6, 
        max_length=20, 
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения'}
    )
    remember_me = forms.BooleanField(
        label='Запомнить меня', 
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password and repeat_password and password != repeat_password:
            raise ValidationError('Пароли не совпадают.')

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label='Email', 
        required=True, 
        error_messages={'required': 'Введите корректный email'}
    )

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Пароль:', 
        widget=forms.PasswordInput, 
        min_length=6, 
        max_length=20, 
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения'}
    )
    repeat_password = forms.CharField(
        label='Повторите пароль:', 
        widget=forms.PasswordInput, 
        min_length=6, 
        max_length=20, 
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения'}
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password and repeat_password and password != repeat_password:
            raise ValidationError('Пароли не совпадают.')

from captcha.fields import CaptchaField

class LoginFormWithCaptcha(AuthenticationForm):
    captcha = CaptchaField()