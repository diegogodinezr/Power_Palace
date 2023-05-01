from django.shortcuts import render
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q


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

def verificar_usuario(request):
    nombre_o_id = request.GET.get('nombre_o_id', None)
    if nombre_o_id:
        # Separar los términos de búsqueda por espacios
        terminos = nombre_o_id.split()
        # Buscar por ID o por coincidencias en los campos de nombre y apellido
        if len(terminos) == 1:
            try:
                usuario = cliente.objects.get(id=terminos[0])
            except cliente.DoesNotExist:
                usuario = None
        else:
            usuario = cliente.objects.filter(
                Q(nombre__icontains=terminos[0]) & Q(primer_apellido__icontains=terminos[1])
            ).first()
        if usuario:
            mensaje = f"Usuario encontrado: {usuario.nombre} {usuario.primer_apellido}"
        else:
            mensaje = "No se encontró ningún usuario con los datos ingresados."
        context = {'mensaje': mensaje}
        return render(request, 'verificar_usuario.html', context)
    else:
        return render(request, 'verificar_usuario.html')

#====================REGISTRO USUARIOS====================
def registrar_usuarios(request):
    template_to_return='registrar_usuarios.html'
    formulario= clienteform()
    consulta = cliente.objects.all()
    context={ 
        'view_name': "landing1",
        'formulario': formulario,
        'consulta': consulta,
    }
    return render (request,template_to_return,context)

def post_usuarios(request):
    if request.method=="POST":
        form=clienteform(request.POST,request.FILES)
        if form.is_valid():
            cliente.objects.create(
                nombre = request.POST["nombre"],
                primer_apellido = request.POST["primer_apellido"],
                segundo_apellido = request.POST["segundo_apellido"],
                correo = request.POST["correo"],
                telefono = request.POST["telefono"],
            )
            return redirect('/registrar_usuarios')
        else:
            form = clienteform()
        return render(request,'registrar_usuarios.html')
    
def sacar_datos_usuarios(request, id):
    objeto = cliente.objects.get(id=id)
    id=id
    formulario = clienteform(instance=objeto)
    datos = {'formulario': formulario}
    #falta agregar el updateproductor.html
    html_form = render_to_string('updateusuarios.html', datos, request=request)
    return HttpResponse(html_form,id)

def removerusuarios(request):
    idusuarios = request.POST["idusuarios"]
    consulta = clienteform.objects.get(id=idusuarios)
    consulta.delete()
    return HttpResponse('usuario eliminado correctamente')

#====================Pago====================
def pagar(request):
    template_to_return='pagar.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)