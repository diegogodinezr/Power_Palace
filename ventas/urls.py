from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from ventas.views import *
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^$',login_usuario, name="login"),
    path('interfaz_venta/', interfaz_venta, name="interfaz_venta"),
    path('logout/',LogoutView.as_view(next_page='/'), name='logout'),
]