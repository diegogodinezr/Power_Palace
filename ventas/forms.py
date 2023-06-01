from multiprocessing.sharedctypes import Value
from django import forms
from .models import *

class Productoform(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        