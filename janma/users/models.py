from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
#-----------------usuarios-------------

""" Cuando peoxy model o la relacion OneToOne no son suficientes
Podemos sobre escribir el modelo User
Para crear nuestro propio modelo nos apoyamos de la clase AbstractUser
o AbstractBaseUser
"""

class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    fecha_nacimiento = models.DateField()
    
    REQUIRED_FIELDS = []
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Administrador(User):
    class Meta:
        proxy = True        
""" Hacemos uso de proxy model cuando tenemos la necesidad de extender
nuevas funcionalidades """
class Usuario(User):
    
    class Meta:
        proxy=True


    def get_products(self):
        return []

""" Hacemos uso de la relacion 1 a 1 cuando tenemos la necesidad de generar
nuevos atributos hacia nuestro modelo, en este caso queremos agregar
el atributo biografia a User
 """
class Cliente(models.Model):
    first_name = models.CharField('Nombre',max_length=150)
    last_name = models.CharField('Apellido',max_length=150)
    fecha_nacimiento = models.DateField(null=True,blank=True)
    telefono = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)
    
class Perfil(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    biografia = models.TextField()
    fecha_nacimiento  = models.DateField()


