from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from membresias.views import *
from django.contrib.auth.views import LogoutView

app_name = 'membresias'

urlpatterns = [
    url(r'^$',home, name="home"),
    path('loginm/', login_membresias, name="login_membresias"),
    path('verificacionID/', verificacionID, name="verificacionID"),
    path('logout/',LogoutView.as_view(next_page='/'), name='logout'),
    path('registrar_usuarios/',registrar_usuarios, name="registrar_usuarios"),
    path('post_usuarios/',post_usuarios, name="post_usuarios"),
    path('pagar/',pagar, name="pagar"),
]