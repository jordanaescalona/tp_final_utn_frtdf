# Generated by Django 4.1.5 on 2023-03-05 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='envio',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='pedido',
            name='pagar',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
