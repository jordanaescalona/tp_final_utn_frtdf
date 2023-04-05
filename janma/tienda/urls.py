from django.urls import path

from .views import (
    index,BuscadorProductos,BuscadorProductos2,producto_categoria_genero,producto_detalle,
    get_variants,get_products
)

app_name = 'tienda'

urlpatterns = [
    path('',index.as_view(),name="index"),
    
    path('search', BuscadorProductos.as_view(), name='search'),
    path('buscador/',BuscadorProductos2,name="buscador2"),
    path('producto/detalle/<int:pk>',producto_detalle,name="producto_detalle"),
    path('productos/',get_products,name="get_products"),
    path('productos/<str:genero>/<str:categoria>',producto_categoria_genero,name="producto_categoria_genero"),
    path('variants/AJAX/<str:talle>',get_variants,name="get_variants"),

    
    
    
]