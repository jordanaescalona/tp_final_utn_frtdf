from django.db import models
#from django.contrib.auth.models import User



class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=50)
    cp = models.CharField(max_length=10)
    email = models.EmailField()
    web = models.CharField(max_length=50,null=True,blank=True) 
    observaciones = models.TextField(null=True,blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100,unique=True)
    ganancia = models.PositiveIntegerField("Porcentaje de ganancia",default=0)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.PROTECT,related_name="subcategorias") #categoria.subcategorias desde Categorias
    
    def __str__(self):
        return self.nombre

    class Meta:
        #subcategoria unique
        unique_together = ('categoria','nombre')



