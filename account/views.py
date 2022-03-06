# account.views.py


from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

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


def login_view(request):
    form = LoginForm()
    message = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None and user.is_active:
                login(request, user)
                message = messages.success(request, f"Hello, {user.first_name.title()} ! Vous êtes connecté.")
                return redirect('account:profile')
            else:
                message = "Identifiants invalides."


    context = {
        "form": form,
        "message": message,
        "page_title": "Login your account"
    }
    template = 'account/login.html'
    return render(request, template, context)


account_login_view = login_view


def logout_view(request):
    logout(request)
    return redirect('account:login')


account_logout_view = logout_view
