# Generated by Django 3.2.3 on 2023-04-10 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default=None, max_length=20)),
                ('primer_apellido', models.CharField(default=None, max_length=70)),
                ('segundo_apellido', models.CharField(default=None, max_length=70)),
                ('correo', models.CharField(default=None, max_length=70)),
                ('telefono', models.IntegerField(max_length=10)),
            ],
        ),
    ]
