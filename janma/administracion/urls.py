from django.urls import path
from .views import index

from .views import ProveedorCreateView,ProveedorListView,ProveedorUpdateView
from .views import eliminar_proveedor,editar_estado_proveedor,pdf_proveedor
from .views import CategoriaListView,CategoriaCreateView,CategoriaUpdateView,eliminar_categoria
from .views import SubcategoriaListView,SubcategoriaCreateView,SubcategoriaUpdateView,eliminar_subcategoria
from .views import (
    TiendaCreateView,TiendaUpdateView,tienda_datos,
    CarouselListView,CarouselCreateView,CarouselUpdateView,eliminar_carousel,
    alerta_stock,alerta_stock_menu
)

app_name = 'administracion'
urlpatterns = [
    path('',index.as_view(),name="index"),
    

    path('proveedor/nuevo',ProveedorCreateView.as_view(),name="proveedor_new"),
    path('proveedores/',ProveedorListView.as_view(),name="proveedor_listado"),
    path('proveedor/edit/<int:pk>',ProveedorUpdateView.as_view(),name="proveedor_edit"),
    path('proveedor/delete/<int:pk>',eliminar_proveedor,name="proveedor_delete"),
    path('proveedor/cambiar_estado/<int:pk>',editar_estado_proveedor,name="proveedor_estado"),
    path('proveedor/pdf/<int:pk>',pdf_proveedor,name="proveedor_pdf"),

    path('categorias/',CategoriaListView.as_view(),name="categorias"),
    path('categoria/new',CategoriaCreateView.as_view(),name="categoria_new"),
    path('categoria/edit/<int:pk>',CategoriaUpdateView.as_view(),name="categoria_edit"),
    path('categoria/delete/<int:pk>',eliminar_categoria,name="categoria_delete"),

    path('subcategorias/',SubcategoriaListView.as_view(),name="subcategorias"),
    path('subcategoria/new',SubcategoriaCreateView.as_view(),name="subcategoria_new"),
    path('subcategoria/edit/<int:pk>',SubcategoriaUpdateView.as_view(),name="subcategoria_edit"),
    path('subcategoria/delete/<int:pk>',eliminar_subcategoria,name="subcategoria_delete"),

    path('tienda/datos/',tienda_datos,name="tienda_datos"),
    path('tienda/',TiendaCreateView.as_view(),name="tienda"),
    path('tienda/<int:pk>',TiendaUpdateView.as_view(),name="tienda_update"),

    path('tienda/carousel/',CarouselListView.as_view(),name="carousel_list"),
    path('tienda/carousel/new',CarouselCreateView.as_view(),name="carousel_new"),
    path('tienda/carousel/edit/<int:pk>',CarouselUpdateView.as_view(),name="carousel_update"),
    path('tienda/carousel/delete/<int:pk>',eliminar_carousel,name="carousel_delete"),

    path('alerta_stock',alerta_stock,name="alerta_stock"),
    path('menu/alerta_stock',alerta_stock_menu,name="alerta_stock_menu"),
   
]