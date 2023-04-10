from django.db import models

# Create your models here.
class cliente (models.Model):
    nombre = models.CharField(max_length=20, blank=False, default=None)
    primer_apellido = models.CharField(max_length=70, blank=False, default=None)
    segundo_apellido = models.CharField(max_length=70, blank=False, default=None)
    correo = models.CharField(max_length=70, blank=False, default=None)
    telefono = models.CharField(max_length=10, null=False, blank=False)