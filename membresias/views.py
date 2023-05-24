from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe


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
    request.session['id_cliente'] = nombre_o_id
    if nombre_o_id:
        # Separar los términos de búsqueda por espacios
        terminos = nombre_o_id.split()
        # Buscar por ID o por coincidencias en los campos de nombre y apellido
        if len(terminos) == 1:
            try:
                usuario = cliente.objects.get(id=terminos[0])
                infpago = pago.objects.get(id_cliente = usuario.id)
                diaantes = infpago.fecha_limite- timedelta(days=1)
            except cliente.DoesNotExist:
                usuario = None
                
        if usuario:
            if (datetime.now()).date() >= infpago.fecha_limite:
                mensaje = '<div class="datos" style="background-color: #BF8807; border-radius:15px; padding:5px 25px; color: white;">Correcto</div>'
                context = {'mensaje': mensaje}  

            elif (datetime.now()).date() == (infpago.fecha_limite- timedelta(days=1)):
                mensaje = '<div class="datos" style="background-color:#099506; border-radius:15px; padding:5px 25px; color: white;">Correcto</div>'
                aviso = 'Mañana es el dia de pago'
                context = {'mensaje': mensaje, 'aviso': aviso}
                print(diaantes)
            else:
                mensaje = '<div class="datos" style="background-color:#099506; border-radius:15px; padding:5px 25px; color: white;">Correcto</div>'
                context = {'mensaje': mensaje}
                
        else:
            mensaje = '<div class="datos" style="background-color: #BE0404; border-radius:15px; padding:5px 25px; color: white;">Incorrecto</div>'
            context = {'mensaje': mensaje}  
        
        return render(request, 'verificacionID.html', context)
    else:
        return render(request, 'verificacionID.html')

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
           

            return redirect('/pagar')
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

def pagar_r(request):
    template_to_return='pagar_r.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

def pago_membresia(request):
    metodo_pago = request.GET.get('metodo_pago')
    context = {
        'view_name': "landing1",
        'metodo_pago': metodo_pago,
    }
    return render(request, 'pago_membresia.html', context)

def renovar(request):
    metodo_pago = request.GET.get('metodo_pago')
    context = {
        'view_name': "landing1",
        'metodo_pago': metodo_pago,
    }
    return render(request, 'renovar.html', context)

def post_pago(request):
    if request.method=="POST":
        fpago = datetime.now()
        fecha_siguiente = fpago + timedelta(days=30)
        ultimo_cliente = cliente.objects.latest('id')
        ultimo_cliente_id = ultimo_cliente.id
        formato_fecha = fpago.strftime("%d/%m/%Y")
        pago.objects.create(
            id_cliente = ultimo_cliente_id,
            fecha_pago = fpago,
            fecha_limite = fecha_siguiente,
            precio_pago = request.POST["precio_pago"],
            iva = request.POST["iva"],
            subtotal = request.POST["subtotal"],
            metodo = request.POST["metodo"],
        )
        
        messages.info(request, mark_safe('Usuario añadido correctamente.<br>Su ID es:<br><a>' + str(ultimo_cliente_id) + '</a><br><a>' + str(formato_fecha) + '</a>'))
        return render(request,'registrar_usuarios.html')
    else:
        render(request,'pago_membresia.html')
    
def regresar(request):
    ultimo_cliente = cliente.objects.latest('id')
    ultimo_cliente.delete()
    template_to_return='verificacionID.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

def modificar_pago(request):
    cliente = request.session.get('id_cliente')  # Obtener el ID del cliente desde la sesión
    # Aquí puedes realizar la lógica para modificar el pago utilizando el id_cliente
    if request.method=="POST":
        fpago = datetime.now()
        fecha_siguiente = fpago + timedelta(days=30)
        pago_existente = get_object_or_404(pago, id_cliente=cliente)
        formato_fecha = fpago.strftime("%d/%m/%Y")
        # Actualizar los campos del pago existente
        pago_existente.fecha_pago = fpago
        pago_existente.fecha_limite = fecha_siguiente
        pago_existente.precio_pago = request.POST["precio_pago"]
        pago_existente.iva = request.POST["iva"]
        pago_existente.subtotal = request.POST["subtotal"]
        pago_existente.metodo = request.POST["metodo"]
        pago_existente.save()

        messages.info(request, mark_safe('Renovación exitosa del usuario!<br>Su ID es:<br><a>' + str(cliente) + '</a><br><a>' + str(formato_fecha) + '</a>'))
        return render(request,'registrar_usuarios.html')
    else:
        render(request,'pago_membresia.html')
    # Eliminar el ID del cliente de la sesión después de utilizarlo, si es necesario

    del request.session['id_cliente']

    return render(request, 'pago_membresia.html')

def historial(request):
    pagos = pago.objects.all()
    context={ 
        'view_name': "landing1",
        'pagos': pagos
    }
    return render (request,'historial_membresias.html',context)