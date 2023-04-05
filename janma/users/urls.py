from django.urls import path
from .views import (
    ClienteCreateView,ClienteListView,eliminar_cliente,ClienteUpdateView,
    administracion_login,administracion_logout,
    AdministradorUpdateView,CambiarPasswordView,
    tienda_login,tienda_logout,nuevo_cliente,VolverClienteVentaView
    
)
app_name ="users"

urlpatterns = [
    path('administracion/cliente/new',ClienteCreateView.as_view(),name="new_cliente"),
    path('administracion/clientes', ClienteListView.as_view(),name="clientes" ),
    path('administracion/cliente/delete/<int:pk>',eliminar_cliente,name="delete_cliente"),
    path('administracion/cliente/update/<int:pk>',ClienteUpdateView.as_view(),name="update_cliente" ),
    path('administracion/cliente/new/venta',VolverClienteVentaView.as_view(),name="new_cliente_venta"),
    #tienda
    path('registro',nuevo_cliente,name="registro"),
    path('usuario/logout',tienda_logout,name="logout"),
    path('usuario/login',tienda_login,name="login"),
    #administracion
    path('administracion/login/',administracion_login,name="administracion_login"),
    path('administracion/logout/',administracion_logout,name="administracion_logout"),
    path('administracion/perfil/<int:pk>',AdministradorUpdateView.as_view(),name="administracion_perfil"),
    path('administracion/cambiar_password', CambiarPasswordView.as_view(),name="administracion_cambiar_password" ),
    
]