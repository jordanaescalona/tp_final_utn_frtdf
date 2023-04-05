from django.shortcuts import render
from .venta import Venta
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from productos.models import Product,Variant
from tienda.models import Tienda
from django.contrib import messages 
from .forms import VentaForm
from .utils import breadcrumb
from .models import Venta as VentaM
from .models import DetalleVenta
from decimal import Decimal
import simplejson as json
#pdf - xhtml2pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from janma.settings import sdk
from django.contrib.staticfiles import finders
#decoradores
from django.contrib.auth.decorators import login_required
#respuesta
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='users:administracion_login')
def detalle_venta(request):
    template_name= "ventas/administracion/venta.html"
    venta = Venta(request)
    productos = Product.objects.all().filter(disponible=True)
    variants = Variant.objects.all().filter(stock__lte=3)

    return render(request,template_name,{
        'venta':venta,
        'productos':productos,
        'variants':variants
    })

@login_required(login_url='users:administracion_login')
def buscar_producto_catalogo(request):
    template_name = "ventas/buscar_producto.html"
    productos = Product.objects.all().filter(disponible=True)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    return render(request,template_name,{
        "productos":productos,
        'variants':variants,
        'venta':venta
    })

@login_required(login_url='users:administracion_login')
def agregar_producto(request,pk):
    product = get_object_or_404(Variant,id=pk,product__disponible=True)
    venta = Venta(request) #No puedo serealizar: TypeError('Object of type %s is not JSON serializable'
    
    venta.add(product)                
    messages.success(request,"Producto agregado exitosamente")
    return redirect('administracion:index')

@login_required(login_url='users:administracion_login')   
def eliminar_productos(request,pk):
    product = get_object_or_404(Variant,id=pk,product__disponible=True)
    venta = Venta(request)
    venta.remove(product)
    messages.success(request,"Productos eliminados exitosamente")
    return redirect('ventas:detalle_venta')

def vaciar_detalle(request):
    venta = Venta(request)
    venta.clear()
    messages.success(request,"El detalle de venta se vacio exitosamente")
    return redirect('ventas:detalle_venta')



#Does quasi the same things as json.loads from here: https://pypi.org/project/dynamodb-json/
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

@login_required(login_url='users:administracion_login')
def detalle_producto(request,pk,cantidad_venta=None):
    template_name = 'ventas/administracion/detalle_producto.html'
    venta = Venta(request)
    
    variants = Variant.objects.all().filter(stock__lte=3)
    product = get_object_or_404(Variant,id=pk,product__disponible=True)

    stock = product.stock
    if cantidad_venta:
        cantidad_disponible = stock - int(cantidad_venta)

    else:
        cantidad_disponible = stock

    
    if request.method == 'GET' and request.GET.get('cantidad'):
        cantidad = request.GET.get('cantidad')
        cant = str(int(cantidad_venta)+int(cantidad))
        venta.add(product,int(cantidad))      
        messages.success(request,"Producto agregado exitosamente")
        return redirect('ventas:detalle_producto',pk,cant)
    
    return render(request,template_name,{
        'venta':venta,
        'variants':variants,
        'product':product,
        'cantidad_disponible':cantidad_disponible
    })

@login_required(login_url='users:administracion_login')
def confirmar_venta(request):
    template_name = "ventas/administracion/confirmacion_datos.html"
    venta = Venta(request)
    variants = Variant.objects.all().filter(stock__lte=3)
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()            
            
            return redirect('ventas:confirmar_productos')
        else:
            messages.error(request,'Error')
    else:
        form = VentaForm()
    return render(request,template_name,{
        'form':form,
        'venta':venta,
        'breadcrumb':breadcrumb(),
        'variants':variants
    })

@login_required(login_url='users:administracion_login')
def confirmar_productos(request):
    template_name = 'ventas/administracion/confirmacion_productos.html'
    datos_venta = VentaM.objects.latest('id')    
    venta = Venta(request)
    variants = Variant.objects.all().filter(stock__lte=3)
    i = 0
    for v in venta:
        
        producto = get_object_or_404(Variant,id=v['variant_id'])
        detalle_venta= DetalleVenta(venta=datos_venta,producto=producto,cantidad=v['cantidad'],precio=producto.product.precio_venta,total=v['precio_total'])
        detalle_venta.save()
        i = i + 1
            
    venta.clear()
    if not venta:
         return redirect('ventas:confirmacion')
    
    return render(request,template_name,{
        'venta':venta,
        'breadcrumb':breadcrumb(datos=False,products=True),
        'datos_venta':datos_venta,
        'variants':variants
    })

@login_required(login_url='users:administracion_login')
def confirmacion(request):
    template_name = 'ventas/administracion/confirmacion.html'
    datos_venta = VentaM.objects.latest('id')
    #datos_venta_lista = VentaM.objects.values().latest('id')
    #productos_lista = DetalleVenta.objects.values().filter(venta=datos_venta)
    productos = DetalleVenta.objects.all().filter(venta=datos_venta)
    
    lista = []
    venta = Venta(request)
    variants = Variant.objects.all().filter(stock__lte=3)
    
    for p in productos:
        lista.append({
            'id' : int(p.producto.id),
            'category_id' : int(p.producto.product.categoria.id),
            'currency_id' :'ARS',
            'description' : str(p.producto.product.descripcion),
            'title' : str(p.producto.product.title),
            'quantity' : int(p.cantidad), 
            'unit_price': float(p.precio)
        })
    
    print(lista)

    if datos_venta.medio_pago == 'EFECTIVO':
        messages.success(request,"EL pago se realizó en efectivo!")
    else:
        messages.success(request,"Para continuar presione el botón de mercado pago!")
        preference_data = {
            
            'items': lista,
            "back_urls": {
            "success": "http://127.0.0.1:8000/ventas/listado_ventas", 
            "failure": "http://127.0.0.1:8000/ventas/listado_ventas",
            "pending": "http://127.0.0.1:8000/ventas/listado_ventas"
            },
            "auto_return": "approved"
        }    
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        print(preference) 
        # Crea un ítem en la preferencia
    

    return render(request,template_name,{
        'venta':venta,
        'breadcrumb':breadcrumb(datos=False,products=False,confirmacion=True),
        'datos_venta':datos_venta,
        'variants':variants,
        'preference':preference
    })

@login_required(login_url='users:administracion_login')
def listado_ventas(request):
    template_name = 'ventas/listado_ventas.html'
    venta = Venta(request)
    variants = Variant.objects.all().filter(stock__lte=3)
    listado_ventas = VentaM.objects.all()

    return render(request,template_name,{
        'venta':venta,
        'variants':variants,
        'listado_ventas':listado_ventas
    })

@login_required(login_url='users:administracion_login')
def eliminar_venta(request,pk):
    template_name ="ventas/delete.html"
    id_venta = get_object_or_404(VentaM,pk=pk)
    #detalle_venta = DetalleVenta.objects.all().filter(venta=id_venta)
    detalle_venta = DetalleVenta.objects.filter(venta=id_venta)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)

    if request.method == 'GET':
        context = {"id_venta":id_venta,'variants':variants,'venta':venta}
            
    if request.method == 'POST':
        for v in detalle_venta:
            producto = get_object_or_404(Variant,id=v.producto.id)
            producto.stock = int(producto.stock) + int(v.cantidad)
            producto.save()
        id_venta.delete()
        
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)       

@login_required(login_url='users:administracion_login')
def pdf_venta(request,pk):
    template_path = 'ventas/pdf.html'
    venta = Venta(request)
    datos_venta = get_object_or_404(VentaM,pk=pk)
    detalle_venta = DetalleVenta.objects.all().filter(venta=datos_venta)
    tienda = get_object_or_404(Tienda,pk=1)
    context = {
        'datos_venta':datos_venta,
        'detalle_venta':detalle_venta,
        'venta':venta,
        'tienda':tienda    
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="archivo.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response