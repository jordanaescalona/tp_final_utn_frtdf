from django.urls import path
from .views import cart,vaciar_carrito,eliminar_producto_carrito,agregar_producto,actualizar_carrito
app_name = "cart"

urlpatterns = [
    path('',cart,name="cart"),
    path('vaciar',vaciar_carrito,name="vaciar"),
    path('eliminar/<int:id>',eliminar_producto_carrito,name="eliminar_producto"),
    path('agregar/<int:variant_id>/<int:cantidad>',agregar_producto,name="agregar_producto"),
    path('actualizar/<int:variant_id>/<int:cantidad>',actualizar_carrito,name="actualizar"),

]