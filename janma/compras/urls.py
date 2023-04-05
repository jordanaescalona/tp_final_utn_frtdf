from django.urls import path
from .views import (
    subir_catalogo,catalogo_delete,
    importar_productos,nueva_compra,get_proveedor,
    CatalogoListView,buscar_producto_catalogo,PedidosListView,
    catalogo_productos_proveedor,eliminar_pedido,eliminar_detalle_pedido,
    PedidosPendientesListView,PedidoUpdateView,pdf_pedido,PedidoEditar
   
)

app_name = "compras"

urlpatterns = [
    path("subir_catalogo/",subir_catalogo,name="subir_catalogo"),
    path('catalogos/',CatalogoListView.as_view(),name="catalogos"),
    path('catalogo-delete/<int:pk>',catalogo_delete,name="catalogo_delete"),
    path("catalogo/<int:pk>/importar-productos",importar_productos,name="importar_productos"),
    path("catalogo/<int:catalogo_id>/productos",catalogo_productos_proveedor,name="productos_catalogo"),
    path("nuevo_pedido/",nueva_compra,name="nuevo_pedido"),
    path('nuevo_pedido/edit/<int:id>',nueva_compra,name="nuevo_pedido_edit"),
    path("proveedor/AJAX/<int:catalogo_id>",get_proveedor,name="get_proveedor"),
    path('catalogo/seleccionar_producto/<int:catalogo_id>',buscar_producto_catalogo,name="producto_catalogo"),
    path('pedidos/',PedidosListView.as_view(),name="listado_pedidos"),
    path('pedido/delete/<int:pk>',eliminar_pedido,name="eliminar_pedido"),
    path('pedido/detalle/delete/<int:pk>',eliminar_detalle_pedido,name="eliminar_detalle_pedido"),
    path('pedido/pdf/<int:pk>',pdf_pedido,name="pdf_pedido"),
    path('pedido/editar/<int:pk>', PedidoEditar.as_view(), name="pedido_editar" )
,    #PEdidos recibidos
    path('pedidos/pendientes/',PedidosPendientesListView.as_view(),name="pedidos_pendientes"),
    path('pedidos/pendientes/pedido/<int:pk>',PedidoUpdateView.as_view(),name="pedido_pendiente"),
    
]