from django import forms
from django.core.exceptions import ValidationError
from main.models import Product
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import ConfirmCode
import secrets

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name description price is_active category tags'.split()
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введи названия товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'заполните описания'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'введите цн=ену товара'
            }),
            'is_active': forms.CheckboxInput(attrs={
                # 'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form=control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control'
            })
        }



class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(username=username)
        if users:
            raise ValidationError('User already exists')
        return username

    def clean_password1(self):
        print(self.changed_data)
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password != password1:
            raise ValidationError('Passwords not match')
        return password

    @property
    def save(self):
        ''' Create User'''
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email,
                                        is_active=False)
        code = secrets.token_bytes(10)
        ConfirmCode.objects.create(user=user, code=code)
        from django.conf import settings
        send_mail(subject='Confirmation Subject',
                  message=f'http://127.0.01:8000/activate/{code}/',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[email],
                  fail_silently=True)
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))