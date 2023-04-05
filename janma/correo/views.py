from django.shortcuts import render
from compras.models import Pedido,DetallePedido,Catalogo
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from productos.models import Variant
from tienda.models import Tienda
from ventas.venta import Venta
# Create your views here.
def send_email(pedido_id):
    pedido = get_object_or_404(Pedido,id=pedido_id)
    proveedor = pedido.catalogo.proveedor.nombre
    correo = pedido.catalogo.proveedor.email
    detalle = DetallePedido.objects.all().filter(pedido=pedido_id)
    tienda = get_object_or_404(Tienda,id=1)
    context = {
        'proveedor':proveedor,
        'detalle':detalle,
        'pedido':pedido,
        'tienda':tienda
    }
    template = get_template('correo/correo.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Orden de pedido Janma Store',
        'Hola hemos realizado el pedido de los artículos que se detallan',
        settings.EMAIL_HOST_USER,
        [correo]
    )
    email.attach_alternative(content,'text/html')
    email.send()
    

def correo(request,pedido_id):
    template_name = 'compras/pedido/send_mail.html'
    pedido = get_object_or_404(Pedido,id=pedido_id)
    detalle = DetallePedido.objects.all().filter(pedido=pedido)
    variants = Variant.objects.all().filter(stock__lte=3)
    tienda = get_object_or_404(Tienda,id=1)
    venta = Venta(request)
    if request.method == "GET":
        
        proveedor = pedido.catalogo.proveedor.nombre
        correo = pedido.catalogo.proveedor.email
        

    if request.method == "POST":
        pedido_id = pedido.id
        send_email(pedido_id)
        messages.success(request,"Correo enviado exitosamente")
        return redirect('compras:listado_pedidos')
    
    return render(request,template_name,{
        'pedido':pedido,
        'proveedor':proveedor,
        'correo':correo,
        'detalle':detalle,
        'variants':variants,
        'tienda':tienda,
        'venta':venta
    })