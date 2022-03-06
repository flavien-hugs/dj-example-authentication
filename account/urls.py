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
        view=views.accoun_login_page,
        name='login_url'
    )
]
