from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta

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
    
    context = {
        'view_name': "landing1",
        'formulario': formulario,
    }
    return render(request, 'registrar_productos.html', context)


def post_producto(request):
    if request.method == "POST":
        form = Productoform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/registrar_producto/')  # Redirigir a la misma URL para mostrar el formulario vacío
    else:
        form = Productoform()
    return render(request, 'registrar_productos.html', {'form': form})

#====================INVENTARIO====================

def inventario(request):
    productos = Producto.objects.all()
    context={ 
        'view_name': "landing1",
        'productos': productos
    }
    return render(request, 'inventario.html', context)

def updateproducto(request):
    resultado = Producto.objects.get(id=producto_id)
    form = Productoform(instance=resultado)
    
    if request.method == "POST":
        form = Productoform(request.POST, request.FILES, instance=resultado)
        if form.is_valid():
            form.save()
            return redirect("/inventario")
            return HttpResponse("Producto actualizado correctamente")
    
    context = {
        'form': form,
        'resultado': resultado,
        'id': producto_id,
    }
    return render(request, 'updateproducto.html', context)



def obtener_producto(request, id):
    try:
        producto = Producto.objects.get(id=id)
        response = {
            'producto': {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'cantidad': producto.cantidad,
                'descripcion': producto.descripcion,
                'categoria': producto.categoria
            }
        }
        return JsonResponse(response)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#eliminar
def eliminar_producto(request):
    if request.method == "POST":
        producto_id = request.POST.get("id_producto")

        # Obtener el producto a eliminar
        producto = get_object_or_404(Producto, id=producto_id)

        # Eliminar el producto de la base de datos
        producto.delete()

        # Redirigir a la página de inventario
        return redirect("/inventario")

    # Si la petición no es POST, devolver una respuesta de error
    return JsonResponse({"error": "Método no permitido"}, status=405)

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


import json
def pago(request):
    template_to_return='pago.html'
    total = request.GET.get('total')
    info = request.GET.get('info')

    if info:
        info_dict = json.loads(info)  # Convierte la cadena JSON en un diccionario

        compra_total = info_dict['compra']['total']
        productos = info_dict['productos']
        request.session['compra'] = compra_total
        request.session['productosc'] = productos

        print("hola")
        print(str(compra_total))
        print(str(productos))
    context={ 
        'view_name': "landing1",
    }
    return render (request,template_to_return,context)
    
def post_pagov(request):
    if request.method == "POST":
        fechap = datetime.now()
        vendido = ''
        productos = request.session.get('productosc')
        for producto in productos:
            id_productoa = producto['id_producto']
            nombrea = producto['nombre']
            precioa = producto['precio']
            cantidada = producto['cantidad']
            subtotala = producto['subtotal']
            vendido = vendido + ' ' + nombrea + ' cantidad: ' + str(cantidada) + ', '

        HistorialVenta.objects.create(
            fecha = fechap,
            metodo_pago=request.POST["metodo_pago"],
            iva=request.POST["iva"],
            subtotal=request.POST["subtotal"],
            total=request.POST["total"],
            productosv = vendido,
        )
        compra = request.session.get('compra')
        ultimaventa = HistorialVenta.objects.latest('id')
        idhventa = ultimaventa.id
        for producto in productos:
            id_productoa = producto['id_producto']
            nombrea = producto['nombre']
            precioa = producto['precio']
            cantidada = producto['cantidad']
            subtotala = producto['subtotal']

            Venta.objects.create(
                idhistorial = idhventa,
                id_producto = id_productoa,
                nombre = nombrea,
                precio = precioa,
                cantidad = cantidada,
                subtotal = subtotala
            )

        del request.session['compra']
        del request.session['productosc']
        try:
            print("venta completada")
            messages.info(request,'Venta realizada correctamente!')
            return render(request, 'metodo_pago.html')
        except:
            messages.info(request,'Error venta no realizada!')
            return render(request, 'metodo_pago.html')

    else:
        return render(request, 'metodo_pago.html')
    
def metodo_pago(request):
    metodo_pago = request.GET.get('metodo_pago')
    
    context = {
        'view_name': "landing1",
        'metodo_pago': metodo_pago,
    }
    return render(request, 'metodo_pago.html', context)

#====================HISTORIAL VENTAS====================
def historial_ventas(request):
    historial = HistorialVenta.objects.all()
    context = {
        'view_name': "landing1",
        'ventas': historial
    }
    return render(request, 'historial_ventas.html', context)

def filtrosv(request):
    formulario = HistorialVentaForm()
    consulta = HistorialVenta.objects.all()
    if request.method == 'GET':
        idc = request.GET.get('id')
        fechac = request.GET.get('fecha')
        productosc = request.GET.get('productosv')
        subtotalc = request.GET.get('subtotal')
        ivac = request.GET.get('iva')
        totalc = request.GET.get('total')
        metodo_pagoc = request.GET.get('metodo_pago')

        if idc:
            consulta = consulta.filter(id=idc)
        if fechac:
            consulta = consulta.filter(fecha=fechac)
        if productosc:
            consulta = consulta.filter(productosv=productosc)
        if subtotalc:
            consulta = consulta.filter(subtotal=subtotalc)
        if ivac:
            consulta = consulta.filter(iva=ivac)
        if totalc:
            consulta = consulta.filter(total=totalc)
        if metodo_pagoc:
            consulta = consulta.filter(metodo_pago=metodo_pagoc)

    if not consulta.exists():
        messages.info(request, 'No se encontraron resultados.')

    context = {
        "formulario": formulario,
        "ventas": consulta,
    }

    return render(request, 'historial_ventas.html', context)

