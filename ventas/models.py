from django.db import models

# Create your models here.
class producto(models.Model):
    id = models.AutoField(primary_key=True) # Campo para el ID del producto, con auto-incremento
    id_producto = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)
    precio = models.FloatField()
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    categoria = models.CharField(max_length=70)