from django.urls import path
from .views import (
    ProductoList,ProductoDetalle,VariantList,
    ClienteList
)
app_name = "api"

urlpatterns = [
    path('productos/',ProductoList.as_view(),name="productos"),
    path('producto/<str:codigo>',ProductoDetalle.as_view(),name="producto"),
    path('producto/detalle/<str:codigo>',VariantList.as_view(),name="producto_detalle"),
    path('clientes/',ClienteList.as_view(),name="clientes"),
]

