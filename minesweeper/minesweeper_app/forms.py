from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='почта',
                             error_messages={
                                 'required': 'Поле email обязательно для заполнения',
                                 'invalid': 'Введите корректный адрес электронной почты',
                                 'unique': 'Пользователь с таким email уже зарегистрирован'
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
                'min_length': 'Имя пользователя должно содержать минимум 3 символа',
                'invalid': 'Имя пользователя содержит недопустимые символы'
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Убираем подсказки
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


        self.fields['password1'].label = 'пароль'
        self.fields['password2'].label = 'повтор пароля'

        #Полностью переопределяем сообщения об ошибках для паролей
        self.fields['password1'].error_messages = {
            'required': 'Необходимо ввести пароль',
            'password_too_common': 'Этот пароль слишком распространён',
            'password_too_short': 'Пароль должен содержать минимум 8 символов',
            'password_entirely_numeric': 'Пароль не может состоять только из цифр',
            'password_similar': 'Пароль слишком похож на имя пользователя'
        }

        self.fields['password2'].error_messages = {
            'required': 'Необходимо подтвердить пароль',
            'password_mismatch': 'Введённые пароли не совпадают'  # Это исправляет стандартное сообщение
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput, label='логин')
    password = forms.CharField(widget=forms.PasswordInput, label='пароль')

    error_messages = {
        'invalid_login': "Неверный логин или пароль",
        'inactive': "Этот аккаунт неактивен",
    }