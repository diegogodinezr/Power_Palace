from multiprocessing.sharedctypes import Value
from django import forms
from .models import *

class productoform(forms.ModelForm):
    class Meta:
        model = producto
        fields = '__all__'