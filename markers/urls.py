from django.conf.urls import url

from .views import MarkerView

urlpatterns = [
    url(r"^(?P<template>.+)$", MarkerView.as_view(), name="django-markers-marker"),
]
