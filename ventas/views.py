from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q

#====================LOGIN====================
def login_ventas(request):
    if request.user.is_authenticated:
        return redirect('/interfaz_venta')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/interfaz_venta')
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
    if request.method == 'POST':
        formulario = Productoform(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('registrar_producto')
    else:
        formulario = Productoform()
    consulta = Producto.objects.all()
    context = {
        'view_name': "landing1",
        'formulario': formulario,
        'consulta': consulta,
    }
    return render(request, 'registrar_productos.html', context)

def post_producto(request):
    if request.method == "POST":
        form = Productoform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_producto/')
    else:
        form = Productoform()
    return render(request, 'registrar_productos.html', {'form': form})
    
def sacar_datos_productor(request, id):
    objeto = producto.objects.get(id=id)
    id=id
    formulario = Productoform(instance=objeto)
    datos = {'formulario': formulario}
    #falta agregar el updateproductor.html
    html_form = render_to_string('updateproducto.html', datos, request=request)
    return HttpResponse(html_form,id)

def removerproductor(request):
    idproductor = request.POST["idproducto"]
    consulta = Producto.objects.get(id=idproductor)
    consulta.delete()
    return HttpResponse('producto eliminado correctamente')

#====================INVENTARIO====================

def inventario(request):
    productos = Producto.objects.all()
    context={ 
        'view_name': "landing1",
        'productos': productos
    }
    return render (request,'inventario.html',context)

def updateproducto(request,id):
    resultado=Producto.objects.get(id=id)
    id=id
    form=Productoform(instance=resultado)
    template_to_return = "inventario.html"
    if request.method=="POST":
        form=Productoform(request.POST,request.FILES)
        if form.is_valid():
            resultado.id_producto = request.POST["id_producto"]
            resultado.nombre = request.POST["nombre"]
            resultado.precio = request.POST["precio"]
            resultado.descripcion = request.POST["descripcion"]
            resultado.cantidad = request.POST["cantidad"]
            resultado.categoria = request.POST["categoria"]
            resultado.save()
            return redirect("/updateproducto")

    context={
        'form':form,
        'resultado':resultado,
        'id':id,
    }
    return render (request, template_to_return,context)

#Buscador
def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(Q(nombre__icontains=query) | Q(id_producto=query))
    response_data = {'productos': []}
    for producto in productos:
        response_data['productos'].append({
            'id': producto.id_producto,
            'nombre': producto.nombre,
            'precio': producto.precio,
        })
    return JsonResponse(response_data)

#====================VENTAS====================
def ventas(request):
    # Lógica para calcular el subtotal
    subtotal = 0.0

    # Obtener los productos del carrito utilizando la función obtener_productos_del_carrito
    carrito = obtener_productos_del_carrito()

    for producto in carrito:
        subtotal += producto.precio

    

    context = {
        'view_name': "landing1",
        'subtotal': subtotal,
    }

    return render(request, 'ventas.html', context)

def obtener_productos_del_carrito():
    carrito = []  

    return carrito


def pago(request):
    template_to_return='pago.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)
    

def metodo_pago(request):
    metodo_pago = request.GET.get('metodo_pago')
    context = {
        'view_name': "landing1",
        'metodo_pago': metodo_pago,
    }
    return render(request, 'metodo_pago.html', context)

#====================HISTORIAL VENTAS====================
def historial_ventas(request):
    template_to_return='historial_ventas.html'
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)
