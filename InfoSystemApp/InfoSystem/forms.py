from .models import User, DeviceGroup
from .models import Device, Parameter, SentData, DataFrame
from django import forms
from django.contrib.auth.hashers import make_password
from phonenumber_field.formfields import PhoneNumberField

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес электронной почты'
    }))
    password1 = forms.CharField(max_length=254, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(max_length=254, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите пароль'
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким именем уже существует.')
        password1 = cleaned_data.get('password1')   
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            self.add_error('password1', 'Пароли не совпадают.')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(max_length=254, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'Неправильное имя пользователя или пароль.')
            return
        password = cleaned_data.get('password')
        user = User.objects.get(username=username)
        salt = user.salt
        hashed_password = make_password(password=password, salt=salt)
        if hashed_password != user.password:
            self.add_error('password', 'Неправильное имя пользователя или пароль.')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254,  widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес электронной почты'
    }))


class DevicesGroupAddForm(forms.Form):
    device_group_name = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя группы устройств'
    }))
    description = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Описание'
    }), required=False)

class DevicesGroupEditForm(forms.Form):
    device_group_name = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя группы устройств'
    }))
    description = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Описание'
    }), required=False)

class DeviceAddForm(forms.Form):
    device_name = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя устройства'
    }))

    location_name =  forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя местоположения'
    }))

    description = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Описание'
    }), required=False)

class DeviceEditForm(forms.Form):
    device_name = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя устройства'
    }))

    location_name =  forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя местоположения'
    }))
    
    description = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Описание'
    }), required=False)