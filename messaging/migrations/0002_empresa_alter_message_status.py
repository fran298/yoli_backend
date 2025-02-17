# Generated by Django 5.1.1 on 2024-10-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('servicios', 'Servicios'), ('productos', 'Productos')], max_length=50)),
                ('numero_whatsapp', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('sent', 'Enviado'), ('received', 'Recibido'), ('pending', 'Pendiente')], default='pending', max_length=50),
        ),
    ]
