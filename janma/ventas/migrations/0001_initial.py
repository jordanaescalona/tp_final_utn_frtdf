# Generated by Django 4.1.5 on 2023-03-04 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0006_cliente_telefono_alter_cliente_first_name_and_more'),
        ('productos', '0003_remove_variant_precio_compra_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedioPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('cliente', models.ForeignKey(blank=True, default='No especifica', null=True, on_delete=django.db.models.deletion.CASCADE, to='users.cliente')),
                ('medio_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.mediopago')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.variant')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.venta')),
            ],
        ),
    ]
