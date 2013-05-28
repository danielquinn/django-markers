from django.conf.urls import patterns, url

from .views import MarkerView

urlpatterns = patterns("markers.views",
    url(r"^(?P<template>.+)$", MarkerView.as_view(), name="django-markers-marker"),
)

