from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from ventas.views import *
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'ventas'

urlpatterns = [
    url(r'^$',login_ventas, name="login"),
    path("loginv/", login_ventas, name="login_ventas"),
    path('interfaz_venta/', interfaz_venta, name="interfaz_venta"),
    path('logout/',LogoutView.as_view(next_page='/'), name='logout'),
    path('registrar_producto/',registrar_producto, name="registrar_producto"),
    path('registrar_producto/post_producto/',post_producto, name="post_producto"),
    path('registrar_producto/post_producto/registrar_producto/',post_producto, name="post_producto"),
    path('inventario/',inventario, name="inventario"),
    path('updateproducto/',updateproducto, name="updateproducto"),
    path('ventas/',ventas, name="ventas"),
    path('buscar_productos/',buscar_productos, name="buscar_productos"),
    path('pago/',pago, name="pago"),
    path('pago/metodo_pago/',metodo_pago, name="metodo_pago"),
    path('metodo_pago/',metodo_pago, name="metodo_pago"),
    path('historial_ventas/',historial_ventas, name="historial_ventas"),
]