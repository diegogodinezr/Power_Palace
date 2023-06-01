from django.db import models

# Create your models here.
class Producto(models.Model):
    id = models.AutoField(primary_key=True) # Campo para el ID del producto, con auto-incremento
    id_producto = models.CharField(max_length=20,unique=True)
    nombre = models.CharField(max_length=20)
    precio = models.FloatField()
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    categoria = models.CharField(max_length=70)   

class Venta(models.Model):
    id_producto = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)
    precio = models.FloatField()
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    # Agrega más campos según tus necesidades

    def __str__(self):
        return f"Venta {self.id}"
