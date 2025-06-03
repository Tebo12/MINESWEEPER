from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='почта',
                             error_messages={
                                 'required': 'Поле email обязательно для заполнения',
                                 'invalid': 'Введите корректный адрес электронной почты',
                             })

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": 'логин',
        }
        error_messages = {
            'username': {
                'required': 'Необходимо указать имя пользователя',
                'unique': 'Это имя пользователя уже занято',
                'max_length': 'Имя пользователя не должно превышать 150 символов',
                'invalid': 'Имя пользователя содержит недопустимые символы'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['password1'].label = 'пароль'
        self.fields['password2'].label = 'повтор пароля'


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput, label='логин')
    password = forms.CharField(widget=forms.PasswordInput, label='пароль')

    error_messages = {
        'invalid_login': "Неверный логин или пароль",
        'inactive': "Этот аккаунт неактивен",
    }