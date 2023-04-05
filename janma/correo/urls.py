from django.urls import path
from .views import correo
app_name="correo"

urlpatterns = [
    path('enviar/email/<int:pedido_id>',correo,name="send"),
]