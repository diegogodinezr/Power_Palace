from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from membresias.views import *
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'membresias'

urlpatterns = [
    url(r'^$',home, name="home"),
    path('membresias/', login_usuario, name="login_usuario"),
    path('login_usuario/', login_usuario, name="login_usuario"),
    path('verificacionID/', verificacionID, name="verificacionID"),
    path('logout/',LogoutView.as_view(next_page='/home/'), name='logout'),
]