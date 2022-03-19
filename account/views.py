# account.views.py

from django.urls import reverse
from django.conf import settings
from django.views.generic import View
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from validate_email import validate_email

from helpers.utilitary import get_client_ip, EmailThread, generate_token



class RegistrationView(View):

    template_name = "account/register.html"

    def get(self, request, *args, **kwargs):
        ctx = {
            "page_title": "Créer un compte"
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):

        data = request.POST

        context = {
            'data': data,
            'has_error': False
        }

        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')

        mail_to_lower = email.lower()

        if password != password2:
            messages.add_message(
                request, messages.ERROR,
                'Les mots de passe ne correspondent pas !'
            )
            context['has_error'] = True

        if not validate_email(mail_to_lower):
            messages.add_message(
                request, messages.ERROR,
                f"""
                Veuillez fournir une adresse électronique valide:
                {mail_to_lower}
                """
            )
            context['has_error'] = True

        try:
            if (
                get_user_model().objects.get(email=mail_to_lower)
            ):
                message = messages.add_message(
                    request, messages.ERROR,
                    f"Cette adresse email '{mail_to_lower}' est déjà utilisé !"
                )
                context['has_error'] = True
                context['page_title'] = message
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, self.template_name, context, status=400)

        user = get_user_model().objects.create_user(email=mail_to_lower)
        user.set_password(password)
        user.is_active = False
        user.ip_address = get_client_ip(request)
        user.save()

        current_site = get_current_site(request)
        email_subject = 'Activer votre compte'

        message = render_to_string(
            'account/activate.html',
            {
                'user': user,
                'scheme': request.scheme,
                'domain': '127.0.0.1:8000',
                'uuid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            }
        )
        email_message = EmailMessage(
            email_subject, message,
            settings.EMAIL_HOST_USER,
            [email]
        )
        EmailThread(email_message).start()
        messages.add_message(
            request, messages.SUCCESS,
            f"""
            Hello {user.email},
            nous vous avons envoyé un courriel à
            <strong>{user.email.lower()}</strong> contenant les
            instructions sur la façon d'activer votre compte.
            Consultez votre boîte de réception et cliquez sur le lien fourni.
            """
        )
        return redirect(settings.LOGIN_URL)


account_register_view = RegistrationView.as_view()


class LoginView(View):

    template_name = 'account/login.html'

    def get(self, request):
        ctx = {
            'page_title': "Page de connexion",
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == '':
            messages.error(request, "L'email est nécessaire !")
            context['has_error'] = True
        if password == '':
            messages.error(request, "Le mot de passe est requis !")
            context['has_error'] = True

        email_lower = email.lower()
        user = authenticate(request, email=email_lower, password=password)

        if not user and not context['has_error']:
            messages.error(request, 'Identifiants invalides.')
            context['has_error'] = True

        if context['has_error']:
            return render(request, self.template_name, status=401, context=context)

        login(request, user)
        messages.success(
            request, f"Vous êtes connecté en tant que { user.get_short_name() }"
        )
        return redirect(settings.LOGIN_REDIRECT_URL)


account_login_view = LoginView.as_view()


class ActivateAccountView(View):

    template_name = 'account/activate_failed.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if (
            user is not None
            and generate_token.check_token(user, token)
        ):
            user.is_active = True
            user.save()
            messages.add_message(
                request, messages.SUCCESS,
                f"Hello {user.get_short_name()}, Votre compte a été activé avec succès."
            )
            return redirect(settings.LOGIN_URL)
        return render(request, self.template_name, status=401)


account_activate_account_view = ActivateAccountView.as_view()


class ResetPasswordEmailView(View):

    template_name = 'account/password_reset_email.html'

    def get(self, request):
        ctx = {
            'page_title': "Aide avec le mot de passe",
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(
                request, 'Veuillez entrer une adresse email valide.')
            return render(request, self.template_name)

        user = get_user_model().objects.filter(email=email.lower())

        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Réinitialiser votre mot de passe.]'
            message = render_to_string(
                'account/reset_user_password.html',
                {
                    'domain': current_site,
                    'scheme': request.scheme,
                    'uuid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token': PasswordResetTokenGenerator().make_token(user[0])
                }
            )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            EmailThread(email_message).start()

        messages.success(
            request, f"""Nous vous avons envoyé un courriel à
            <strong>{email.lower()}</strong> contenant les
            instructions sur la façon de réinitialiser votre mot de passe.
            Consultez votre boîte de réception et cliquez sur le lien fourni.
            """)
        
        ctx = {
            'page_title': "Aide avec le mot de passe",
        }

        return render(request, self.template_name, ctx)


account_reset_password_view = ResetPasswordEmailView.as_view()


class SetNewPasswordView(View):

    template_name = "account/password_reset_email.html"

    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token,
            'page_title': "Aide avec le mot de passe",
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = get_user_model().objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request,
                    """Le lien de réinitialisation du mot de passe
                    n'est pas valide, veuillez en demander un nouveau."""
                )
                return render(request, self.template_name)

        except DjangoUnicodeDecodeError as identifier:
            messages.success(
                request, 'Lien invalide !')
            return render(request, self.template_name)

        return render(request, 'account/set_new_password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(
                request, messages.ERROR,
                'les mots de passe doivent comporter au moins 6 caractères.'
            )
            context['has_error'] = True
        if password != password2:
            messages.add_message(
                request, messages.ERROR,
                'les mots de passe ne correspondent pas.'
            )
            context['has_error'] = True

        if context['has_error'] == True:
            return render(
                request, 'account/set_new_password.html',
                context
            )

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = get_user_model().objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request,
                """
                    Réinitialisation du mot de passe réussie,
                    vous pouvez vous connecter avec un nouveau mot de passe.
                """)

            return redirect(reverse(settings.LOGIN_URL))

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Lien invalide.')
            return render(
                request,
                'account/set_new_password.html',
                context
            )

        return render(request, 'account/set_new_password.html', context)


account_set_new_password_view = SetNewPasswordView.as_view()


def logout_view(request):
    logout(request)
    messages.add_message(
        request, messages.SUCCESS,
        'Vous vous êtes déconnecté.'
    )
    return redirect(settings.LOGIN_URL)


account_logout_view = logout_view


@login_required
def dashboard(request):
    template = "index.html"
    context = {"page_title": "Dashboard"}
    return render(request, template, context)


account_dashboard = dashboard
