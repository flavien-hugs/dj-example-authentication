# account.forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=80,
        label="Nom d'utilisateur"
    )
    password = forms.CharField(
        max_length=128,
        label="Mot de passe",
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control shadow-none'}
            )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control shadow-none'}
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email and not password:
            raise forms.ValidationError("Adresse email is exist.")
