# Generated by Django 3.2.3 on 2023-06-01 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_alter_producto_id_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='id_producto',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
