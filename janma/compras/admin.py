from django.contrib import admin
from .models import Producto,Catalogo,Pedido,DetallePedido
# Register your models here.
admin.site.register(Producto)
admin.site.register(Catalogo)
admin.site.register(Pedido)
admin.site.register(DetallePedido)