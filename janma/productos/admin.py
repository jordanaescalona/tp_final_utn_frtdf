from django.contrib import admin
from .models import Product,Variant,Image
# Register your models here.
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Image)