from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='почта')

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": 'логин',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        # Меняем label для паролей
        self.fields['password1'].label = 'пароль'
        self.fields['password2'].label = 'повтор'
        for field in ['password1', 'password2']:
            print(self.fields[field].error_messages)
            self.fields[field].error_messages = {
                'password_too_common': 'Этот пароль слишком простой!',
            }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label='логин')
    password = forms.CharField(widget=forms.PasswordInput, label='пароль')
