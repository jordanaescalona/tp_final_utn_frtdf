from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tienda.urls')),
    path('administracion/',include('administracion.urls')),
    path('productos/',include('productos.urls')),
    path('compras/',include("compras.urls")),
    path('carrito/',include("carritos.urls")),
    path('api/',include('api.urls')),
    path('correo/', include('correo.urls')),
    path('usuarios/',include('users.urls')),
    path('ventas/',include('ventas.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

