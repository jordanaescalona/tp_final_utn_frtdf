from django.db import models

# Create your models here.
class Tienda(models.Model):
    razon_social = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    cp = models.CharField("Código postal",max_length=20,default="9420")
    ciudad = models.CharField(max_length=150,default="Río Grande")
    provincia = models.CharField(max_length=200,default="Tierra del Fuego")
    pais = models.CharField(max_length=200)
    telefono = models.CharField(max_length=255)
    email = models.EmailField(null=True,blank=True)
    facebook = models.CharField(max_length=255,null=True,blank=True)
    instagram = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.razon_social


class Carousel(models.Model):
    titulo = models.CharField(max_length=150,null=True,blank=True)
    subtitulo = models.CharField(max_length=200,null=True,blank=True)
    contenido = models.TextField(null=True,blank=True)
    precio =  models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    imagen = models.ImageField(upload_to='carousel/',null=True,blank=True)

    def __str__(self):
        return self.titulo


