from django.shortcuts import render
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.
def landing(request):
    template_to_return='prueba_m.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)