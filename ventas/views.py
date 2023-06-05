from django.shortcuts import render, redirect, get_object_or_404
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
    if request.method == 'POST':
        form = HistorialVentaForm(request.POST)
        print(form.errors)
        print(form.cleaned_data)

        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            id_producto = form.cleaned_data['id_producto']
            nombre = form.cleaned_data['nombre']
            cantidad = form.cleaned_data['cantidad']
            precio = form.cleaned_data['precio']
            subtotal = form.cleaned_data['subtotal']
            metodo_pago = form.cleaned_data['metodo_pago']
            total = form.cleaned_data['total']  # Corrección: utiliza "total" en lugar de "Total"
            
            venta = HistorialVenta(
                fecha=fecha,
                id_producto=id_producto,
                nombre=nombre,
                cantidad=cantidad,
                precio=precio,
                subtotal=subtotal,
                metodo_pago=metodo_pago,
                total=total
            )
            venta.save()
            return redirect('historial_ventas')  # Redirecciona a la página de historial de ventas
    else:
        form = HistorialVentaForm()
    
    return render(request, 'historial_ventas.html', {'form': form})

