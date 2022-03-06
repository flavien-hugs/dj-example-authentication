"""
core URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

import logging

from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from django.conf.urls.static import static
from django.contrib.auth.models import Group

admin.site.unregister(Group)


urlpatterns = [
    path("", include("account.urls", namespace="account")),
    path(settings.ADMIN_URL, admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
