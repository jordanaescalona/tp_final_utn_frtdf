from django.urls import path

from .views import (
    ProductList, ProductCreate, ProductUpdate,
    delete_image, delete_variant,producto_editar_estado,producto_delete
)

app_name = 'products'

urlpatterns = [
    path('administracion', ProductList.as_view(), name='list_products'),
    path('administracion/create/', ProductCreate.as_view(), name='create_product'),
    path('administracion/update/<int:pk>/', ProductUpdate.as_view(), name='update_product'),
    path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('delete-variant/<int:pk>/', delete_variant, name='delete_variant'),
    path('update/estado/<int:pk>',producto_editar_estado,name="estado_update"),
    path('administracion/delete-product/<int:pk>',producto_delete,name="delete_product"),
]