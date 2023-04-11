from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from membresias.views import *
from .views import *
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'ventas'

urlpatterns = [
    url(r'^$',login_user, name="login"),
    path('login/', views.login_user, name='login'),
    path('login_user/', login_user, name="login_user"),
    path('interfaz_venta/', interfaz_venta, name="interfaz_venta"),
    path('logout/',LogoutView.as_view(next_page='/'), name='logout'),
]