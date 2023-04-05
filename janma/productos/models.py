from django.db import models

from administracion.models import Categoria,Proveedor
import uuid
#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

class Product(models.Model):
    title = models.CharField("Título",max_length=150)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE,related_name="product_proveedor")
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE,related_name="product_categoria")
    GENEROS =(
        ("HOMBRE","Hombre"),
        ("MUJER","Mujer"),
        ("UNISEX","Unisex")
    )
    genero = models.CharField(max_length=6,choices=GENEROS,default="UNISEX")
    fecha_compra = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    descripcion = models.TextField(max_length=400,null=True,blank=True)
    oferta = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)
    slug = models.SlugField(null=True,blank=True,unique=True,max_length=255)
    codigo_barras = models.CharField(max_length=255,null=True,blank=True)
    precio_compra = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)
    precio_venta = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True,default=0.0)

    def __str__(self):
        return self.title

    def save(self):
        ganancia = int(self.categoria.ganancia)
        p_compra = self.precio_compra
        p_ganancia = (ganancia * p_compra)/100
        if p_ganancia >= 0:
            if self.precio_venta <= 0.00:
                self.precio_venta = p_ganancia + p_compra
        super(Product,self).save()

    
class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True
        )
    image = models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return self.product.title


class Variant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
        )
    color = models.CharField("Color",max_length=128)
    TALLES =(
        ("XS","XS"),
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL"),
        ("XXL","XXL")
    )

    talle = models.CharField(max_length=3,choices=TALLES)
    
    stock = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return self.product.title

@receiver(pre_save,sender=Product)
def set_slug(sender,instance,*args,**kwargs):
    if instance.title and not instance.slug:
        slug = slugify('{}'.format(instance.title))

        while Product.objects.filter(slug=slug).exists():
            slug = (
                '{}-{}'.format(instance.title,str(uuid.uuid4())[:8])
            )
        instance.slug = slug


