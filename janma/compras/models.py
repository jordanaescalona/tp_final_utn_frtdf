from django.db import models
from administracion.models import Proveedor
#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
# Create your models here.
class Catalogo(models.Model):
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    archivo = models.FileField(upload_to="catalogos/")
    fecha_carga = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return f"Archivo id: {self.id} nombre: {self.archivo}"


class Producto(models.Model):
    catalogo = models.ForeignKey(Catalogo,on_delete=models.CASCADE)
    codigo_producto = models.CharField(max_length=255,null=True,blank=True)
    
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    talle = models.CharField(max_length=50)
    precio_menor = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    precio_mayor = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    cant_minima = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.titulo

class Pedido(models.Model):
    fecha_pedido = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True,null=True)
    catalogo = models.ForeignKey(Catalogo,on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    recibido = models.BooleanField(default=False)
    envio = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    pagar = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    fecha_factura = models.DateField(null=True,blank=True)
    factura = models.FileField(upload_to="facturas",blank=True)

    def __str__(self):
        return f"Pedido Num:{self.id}|Fecha:{self.fecha_pedido}|Catálogo Num:{self.catalogo.id}"
    
    def save(self):
        self.pagar = float(self.total) + float(self.envio)
        super(Pedido,self).save()
    


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad= models.PositiveBigIntegerField(default=0)
    total = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)

    def __str__(self):
        return f"N°de pedido:{self.pedido.id}|Producto:{self.producto}|Cantidad:{self.cantidad}|Total:${self.total}"

    def save(self):
        cantidad = int(self.cantidad)
        cant_min = int(self.producto.cant_minima)
        if cantidad <= cant_min:
            self.total = float(int(cantidad)) * float(self.producto.precio_menor)
        else:
             self.total = float(int(self.cantidad)) * float(self.producto.precio_mayor)
            
        super(DetallePedido,self).save()

    
@receiver(post_save,sender=DetallePedido)
def detalle_pedido_guardar(sender,instance,**kwargs):
    pedido_id = instance.pedido.id 
    producto_id = instance.producto.id 
    pedido = Pedido.objects.get(pk=pedido_id)

    if pedido:
        total = DetallePedido.objects.filter(pedido=pedido_id).aggregate(total=Sum('total')).get('total','0.00')
        pedido.total = total
        pedido.save()

@receiver(post_delete,sender=DetallePedido)
def detalle_pedido_delete(sender,instance,**kwargs):
    pedido_id = instance.pedido.id 
    producto_id = instance.producto.id 
    pedido = Pedido.objects.get(pk=pedido_id)

    if pedido:
        total = DetallePedido.objects.filter(pedido=pedido_id).aggregate(total=Sum('total')).get('total','0.00')
        pedido.total = total
        pedido.save()

