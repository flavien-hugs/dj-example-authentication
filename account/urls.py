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

    path(
        route='logout/',
        view=views.account_logout_view,
        name='logout_url'
    )
]
