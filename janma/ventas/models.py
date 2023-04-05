from django.db import models
from users.models import Cliente
from productos.models import Variant
#Para los signals
from django.db.models.signals import post_save, post_delete,pre_delete

from django.dispatch import receiver
from django.db.models import Sum
from django.shortcuts import get_object_or_404
# Create your models here.
class MedioPago(models.Model):
    tipo = models.CharField(max_length=255)
    
    def __str_(self):
        return self.tipo
    
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE,default="Consumidor final",null=True,blank=True)
    
    MEDIO_PAGO = (
        ("EFECTIVO","EFECTIVO"),
        ("CREDITO","CREDITO"),
        ("DEBITO","DEBITO")
    )
    medio_pago =models.CharField(max_length=9,choices=MEDIO_PAGO,default="EFECTIVO")
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    ESTADO = (
        ("CREADO","CREADO"),
        ("PAGADO","PAGADO"),
        ("COMPLETADO","COMPLETADO"),
        ("CANCELADO","CANCELADO")
    )
    estado = models.CharField(max_length=10,choices=ESTADO,default="CREADO")
    def __str__(self):
        return  "Id venta: {} - Cliente: {}".format(self.id,self.cliente)
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta,on_delete=models.CASCADE)
    producto = models.ForeignKey(Variant,on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    total = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    
    def __str__(self):
        return 'Venta: {}'.format(self.venta)
    
    def save(self):
        producto = get_object_or_404(Variant,id=self.producto.id)
        
        cantidad = int(self.cantidad)
        cant_max = int(producto.stock)
        if cantidad <= cant_max:
            self.total = float(int(cantidad)) * float(self.producto.product.precio_venta)
            producto.stock = cant_max - cantidad
            producto.save()
                    
        super(DetalleVenta,self).save()

@receiver(post_save,sender=DetalleVenta)
def detalle_venta_guardar(sender,instance,**kwargs):
    venta_id = instance.venta.id 
    venta = Venta.objects.get(pk=venta_id)

    if venta:
        total = DetalleVenta.objects.filter(venta=venta_id).aggregate(total=Sum('total')).get('total','0.00')
        venta.total = total
        venta.save()

""" @receiver(pre_delete,sender=DetalleVenta)
def detalle_venta_delete(sender,instance,**kwargs):    
    producto = get_object_or_404(Variant,product=instance.producto.id)        
    stock = int(producto.stock)
    print("****stock")
    print(stock)
    cantidad = int(instance.cantidad)
    print("****cantidad")
    print(cantidad)
    producto.stock = stock + cantidad
    producto.save()    """


