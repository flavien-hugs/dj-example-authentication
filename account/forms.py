# account.forms.py

from django import forms


class LoginForm(forms.Form):

    email = forms.EmailField(
        max_length=80,
        label="Adresse email"
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email and not password:
            raise forms.ValidationError("user does not exist.")
