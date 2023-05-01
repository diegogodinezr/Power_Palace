from django.shortcuts import render
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages

#====================LOGIN====================
def login_ventas(request):
    if request.user.is_authenticated:
        return redirect('/ventas/interfaz_venta')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/ventas/interfaz_venta')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'loginv.html', context)
    
#====================VERIFICACION ID ====================
def interfaz_venta(request):
    template_to_return='interfaz_venta.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

#====================PRODUCTO====================
def registrar_producto(request):
    template_to_return='registrar_productos.html'
    formulario= productoform()
    consulta = producto.objects.all()
    context={ 
        'view_name': "landing1",
        'formulario': formulario,
        'consulta': consulta,
    }
    return render (request,template_to_return,context)
  
def post_producto(request):
    if request.method=="POST":
        form=productoform(request.POST,request.FILES)
        if form.is_valid():
            producto.objects.create(
                id_producto = request.POST["id_producto"],
                nombre = request.POST["nombre"],
                precio = request.POST["precio"],
                descripcion = request.POST["descripcion"],
                cantidad = request.POST["cantidad"],
                categoria = request.POST["categoria"],
            )
            return redirect('/ventas/registrar_producto')
        else:
            form = productoform()
        return render(request,'registrar_productos.html')
    
def sacar_datos_productor(request, id):
    objeto = producto.objects.get(id=id)
    id=id
    formulario = productoform(instance=objeto)
    datos = {'formulario': formulario}
    #falta agregar el updateproductor.html
    html_form = render_to_string('updateproducto.html', datos, request=request)
    return HttpResponse(html_form,id)

def removerproductor(request):
    idproductor = request.POST["idproducto"]
    consulta = producto.objects.get(id=idproductor)
    consulta.delete()
    return HttpResponse('producto eliminado correctamente')

#====================INVENTARIO====================
def inventario(request):
    template_to_return='inventario.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

def updateproducto(request,id):
    resultado=producto.objects.get(id=id)
    id=id
    form=productoform(instance=resultado)
    template_to_return = "inventario.html"
    if request.method=="POST":
        form=productoform(request.POST,request.FILES)
        if form.is_valid():
            resultado.id_producto = request.POST["id_producto"]
            resultado.nombre = request.POST["nombre"]
            resultado.precio = request.POST["precio"]
            resultado.descripcion = request.POST["descripcion"]
            resultado.cantidad = request.POST["cantidad"]
            resultado.categoria = request.POST["categoria"]
            resultado.save()
            return redirect("/ventas/updateproducto")

    context={
        'form':form,
        'resultado':resultado,
        'id':id,
    }
    return render (request, template_to_return,context)

#====================VENTAS====================
def ventas(request):
    template_to_return='ventas.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

def pago(request):
    template_to_return='pago.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

def metodo_pago(request):
    template_to_return='metodo_pago.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)

#====================HISTORIAL VENTAS====================
def historial_ventas(request):
    template_to_return='historial_ventas.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)
