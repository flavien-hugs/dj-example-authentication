# account.views.py

from django.shortcuts import render


from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login

from account.forms import LoginForm


class AccountRegisterView(View):

    template_name = "account/register.html"

    def get(self, request):
        context = {"page_title": "Registration"}
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        email = data.get('email')

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, "Please provide a valid email")

        context = {"data": data}
        return render(request, self.template_name, context)


account_register_view = AccountRegisterView.as_view()


def login_page(request):
    form = LoginForm()
    message = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            f_email = form.cleaned_data['email']
            f_password = form.cleaned_data['password']
            user = authenticate(email=f_email, password=f_password)

            if user is not None:
                login(request, user)
                message = f"Hello, {user.first_name.title()} ! Vous êtes connecté."
            else:
                message = "Identifiants invalides."


    context = {
        "form": form,
        "message": message,
        "page_title": "Login your account"
    }
    template = 'account/login.html'
    return render(request, template, context)


accoun_login_page = login_page
