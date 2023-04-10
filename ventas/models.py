from django.db import models

# Create your models here.
class producto(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=False, default=None)
    precio = models.CharField(max_length=70, blank=False, default=None)
    descripcion = models.CharField(max_length=70, blank=False, default=None)
    cantidad = models.CharField(max_length=70, blank=False, default=None)
    categoria = models.CharField(max_length=70, blank=False, default=None)