# blog.urls.py

from django.urls import path

from account import views


app_name = "account"
urlpatterns = [
    path(
        route='register/',
        view=views.account_register_view,
        name='register_url'
    ),

    path(
        route='login/',
        view=views.account_login_view,
        name='login_url'
    ),

    path(route='activate/<uidb64>/<token>/',
        view=views.account_activate_account_view,
        name='activate'),

    path(route='set-new-password/<uidb64>/<token>/',
        view=views.account_set_new_password_view,
        name='set_new_password'),

    path(route='reset-password/',
        view=views.account_reset_password_view,
        name='reset_password'),

    path(
        route='logout/',
        view=views.account_logout_view,
        name='logout_url'
    ),

    path(
        route='',
        view=views.account_dashboard,
        name="profile_url"
    )
]
