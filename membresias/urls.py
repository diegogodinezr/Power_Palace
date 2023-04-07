from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from membresias.views import *
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^$',landing, name="landing"),

]