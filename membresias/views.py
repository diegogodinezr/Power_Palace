from django.shortcuts import render
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages

#====================HOME====================
def home(request):
    template_to_return='home.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

#====================LOGIN====================
def login_membresias(request):
    if request.user.is_authenticated:
        return redirect('/verificacionID')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/verificacionID')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)
    
#====================VERIFICACION ID ====================
def verificacionID(request):
    template_to_return='verificacionID.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

