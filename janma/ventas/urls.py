from django.urls import path
from .views import (agregar_producto,detalle_venta,eliminar_productos,
                    vaciar_detalle,detalle_producto,confirmar_venta,confirmar_productos,confirmacion,
                    listado_ventas,eliminar_venta,pdf_venta
)
app_name = "ventas"

urlpatterns = [
    path('agregar_producto/<int:pk>',agregar_producto,name="agregar_producto"),
    path('detalle/',detalle_venta,name="detalle_venta"),
    path('eliminar_productos/<int:pk>',eliminar_productos,name="eliminar_productos"),
    path('detalle_producto/<int:pk>/<str:cantidad_venta>',detalle_producto,name="detalle_producto"),
    path('vaciar_detalle',vaciar_detalle,name="vaciar_detalle"),
    path('confirmacion/venta',confirmar_venta,name="confirmar_venta"),
    path('confirmacion/productos/',confirmar_productos,name="confirmar_productos"),
    path('confirmacion/finalizar_transaccion',confirmacion,name="confirmacion"),
    path('listado_ventas',listado_ventas,name="ventas"),
    path('eliminar/venta/<int:pk>',eliminar_venta,name="eliminar_venta"),
    path('pdf/<int:pk>',pdf_venta,name="pdf"),
]