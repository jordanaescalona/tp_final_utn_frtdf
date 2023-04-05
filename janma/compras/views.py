from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from tablib import Dataset 
from .resources import ProductoResource
from django.views.generic import CreateView, DeleteView, UpdateView, View
from ventas.venta import Venta
#modelos
from .models import Catalogo,Producto,Pedido,DetallePedido
from productos.models import Variant
from administracion.models import Proveedor
from tienda.models import Tienda
#Formularios
from .forms import CatalogoForm,ProductoForm,PedidoNewForm,PedidoForm
#Vistas basadas en clase
from django.views.generic.list import ListView
#decoradores
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#mensajes
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#buscar objetos
from django.shortcuts import get_object_or_404
#respuesta
from django.http import HttpResponse
#
import csv
from django.http import JsonResponse
from datetime import datetime
#pdf - xhtml2pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.contrib.staticfiles import finders
# Create your views here.

def subir_catalogo(request):
    form = CatalogoForm(request.POST or None, request.FILES or None)
    template_name = "compras/upload.html"
    venta = Venta(request)
    variants = Variant.objects.all().filter(stock__lte=3)
        
    if form.is_valid():
        form.save()
        
        messages.success(request,'Catálogo cargado exitosamente')
        return redirect('compras:catalogos')
    
    return render(request,template_name,{"form":form,'variants':variants,'venta':venta})

class CatalogoListView(LoginRequiredMixin,ListView):
    template_name = "compras/catalogos.html"
    model = Catalogo
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['venta'] = Venta(self.request)
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        return context

@login_required(login_url='users:administracion_login')
def catalogo_delete(request,pk):
    template_name ="compras/delete.html"
    catalogo = get_object_or_404(Catalogo,id=pk)
    venta = Venta(request) 
    variants = Variant.objects.all().filter(stock__lte=3)
    
    if request.method == 'GET':
        context = {"catalogo":catalogo,'variants':variants,'venta':venta}
            
    if request.method == 'POST':      
        catalogo.delete()
        messages.success(request,"Catálogo eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)

def importar_productos(request,pk):

    catalogo = get_object_or_404(Catalogo,id=pk)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    if catalogo.activo == False:
        producto_resource = ProductoResource()
        dataset = Dataset()
        new_catalogo = catalogo.archivo
        imported_data = dataset.load(new_catalogo.read(),format="xlsx")

        for data in imported_data:
            producto = [
                catalogo,
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6]                
            ]
            Producto.objects.create(
                catalogo = producto[0],
                codigo_producto = producto[1],
                titulo = producto[2],
                descripcion = producto[3],
                talle = producto[4],
                precio_menor = producto[5],
                precio_mayor = producto[6],
                cant_minima = producto[7]
            )
           
        catalogo.activo = True
        
        catalogo.save()
        return redirect('compras:catalogos')
        
    return render(request,"compras/catalogos.html",{
        "catalogo":catalogo,
        'variants':variants,
        'venta':venta
    })

def catalogo_productos_proveedor(request,catalogo_id):
    template_name = "compras/catalogo/productos_catalogo.html"
    catalogo = get_object_or_404(Catalogo,id=catalogo_id)
    productos = Producto.objects.all().filter(catalogo=catalogo_id)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    return render(request,template_name,{
        'catalogo':catalogo,
        'productos':productos,
        'variants':variants,
        'venta':venta
    })

#--------------Compras--------------------
def get_proveedor(request,catalogo_id):
    proveedores = list(Proveedor.objects.filter(catalogo=catalogo_id).values())
    if(len(proveedores)>0):
        data = {"message":'success',"proveedores":proveedores}
    else:
        data = {'message': "Not Found"}
    
    return JsonResponse(data)


def nueva_compra(request,id=None):
    template_name = "compras/pedido.html"
    detalle= {}
    catalogos = Catalogo.objects.all().filter(activo=True)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    if request.method == "GET":
        enc = Pedido.objects.filter(pk=id).first()
        if not enc:
            encabezado = {
                'id':0,
                'fecha':datetime.today(),
                'catalogo':0,
                'total':0.00
            }
            detalle = None
        else:
            encabezado = {
                'id': enc.id,
                'total':enc.total,
                'catalogo':enc.catalogo,
                'fecha':enc.fecha_pedido
            }
            detalle = DetallePedido.objects.filter(pedido=enc)
        contexto = {"enc":encabezado,"det":detalle,'catalogos':catalogos,'variants':variants,'venta':venta}

    if request.method == "POST":
        catalogo = request.POST.get("id_catalogo")
        catalogo = Catalogo.objects.get(id=catalogo)
        
        if not id:
            #si no hay id es proque la factura es nueva
            enc = Pedido(
                catalogo = catalogo
            )
            if enc:
                enc.save()
                id=enc.id #el encabezado es igual al id que se acaba de crear
        else:
            #Si ya existe el id
            enc = Pedido.objects.filter(pk=id).first()
            if enc:
                enc.catalogo = catalogo
                enc.save()
        
        #si llegamos a este punto y no esta inicializado vamos a mandar mensaje de error
        if not id:
            messages.error(request,"No puedo continuar, no puedo detectar número de factura")
            return redirect('compras:listado_pedidos')
        
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cant")
        
        prod = Producto.objects.get(codigo_producto=codigo,catalogo=catalogo)

        det = DetallePedido(
            pedido = enc,
            producto = prod,
            cantidad=cantidad
        )
        if det:
            det.save()
        
        return redirect("compras:nuevo_pedido_edit",id=id)

    
    return render(request,template_name,{
        'catalogos':catalogos,
        'enc':encabezado,
        'det':detalle,
        'variants':variants,
        'venta':venta
    })

def buscar_producto_catalogo(request,catalogo_id):
    template_name = "compras/buscar_producto.html"
    catalogo = get_object_or_404(Catalogo,id=catalogo_id)
    productos = Producto.objects.all().filter(catalogo=catalogo)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    return render(request,template_name,{
        'catalogo':catalogo,
        "productos":productos,
        'variants':variants,
        'venta':venta
    })

@login_required(login_url='users:administracion_login')
def eliminar_detalle_pedido(request,pk):
    template_name ="compras/pedido/delete.html"
    detalle = get_object_or_404(DetallePedido,pk=pk)
    
    variants = Variant.objects.all().filter(stock__lte=3)
        
    if request.method == 'GET':
        
        context = {"detalle":detalle,'variants':variants}
            
    if request.method == 'POST':
        detalle.delete()
        
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)

class PedidosListView(LoginRequiredMixin,ListView):
    template_name = "compras/listado_pedidos.html"
    model = Pedido
    login_url = 'users:administracion_login'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['venta'] = Venta(self.request)
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        return context

@login_required(login_url='administracion:login')
def eliminar_pedido(request,pk):
    template_name ="compras/catalogo/delete.html"
    pedido = get_object_or_404(Pedido,pk=pk)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    
    if request.method == 'GET':
        context = {"pedido":pedido,'variants':variants,'venta':venta}
            
    if request.method == 'POST':
        pedido.delete()
        
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)

class PedidoUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Pedido
    form_class = PedidoNewForm
    template_name = "compras/pedido/pedido.html"   
    success_url = reverse_lazy("compras:pedidos_pendientes")
    success_message = "Registro modificado exitosamente!"
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Pedido pendiente de entrega"
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context
    
class PedidoEditar(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "compras/pedido/pedido.html"
    success_url = reverse_lazy('compras:listado_pedidos')
    success_message = "Registro modificado exitosamente!"
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar datos de pedido"
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

class PedidosPendientesListView(LoginRequiredMixin,ListView):
    template_name = "compras/pedido/pedidos.html"
    model = Pedido
    login_url = 'users:administracion_login'
    success_message = "Registro modificado exitosamente!"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['venta'] = Venta(self.request)
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        return context
    
@login_required(login_url='users:administracion_login')
def pdf_pedido(request,pk):
    template_path = 'compras/pedido/pdf.html'
    venta = Venta(request)
    pedido = Pedido.objects.get(pk=pk)
    detalle = DetallePedido.objects.all().filter(pedido=pedido)
    proveedor = pedido.catalogo.proveedor
    tienda = Tienda.objects.get(id=1)
    context = {
        'pedido':pedido,
        'detalle':detalle,
        'proveedor':proveedor,
        'tienda':tienda,
        'venta':venta    
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