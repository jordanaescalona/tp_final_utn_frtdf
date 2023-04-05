#redireccionamiento
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
#vistas basadas en clase
from django.views.generic import TemplateView
from django.views.generic import CreateView, DeleteView, UpdateView, View
from django.views.generic.list import ListView
#mensajes
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


#decoradores
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#formularios
from .forms import ProveedorForm,EstadoProveedorForm
from .forms import SubcategoriaForm,CategoriaForm,TiendaForm,CarouselForm

#modelos
from .models import Proveedor

from .models import Categoria,Subcategoria
from tienda.models import Tienda,Carousel
from productos.models import Product,Variant
#buscar objetos
from django.shortcuts import get_object_or_404
from django.http import Http404
#respuesta
from django.http import HttpResponse
#pdf - xhtml2pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.contrib.staticfiles import finders

from ventas.venta import Venta

""" pagina principal """
class index(LoginRequiredMixin,TemplateView):
    template_name = 'administracion/index.html'
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super(index,self).get_context_data(**kwargs)
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['productos'] = Variant.objects.all().filter(product__disponible=True)
        context['venta'] = Venta(self.request)

        return context
    def dispath(self,request,*args,**kwargs):
        if request.user.is_superuser:
            return super().dispatch(request,*args,**kwargs)
        return redirect('administracion:index')

#---------------diseño página-----------------
@login_required(login_url='users:administracion_login')
def tienda_datos(request):
    if not request.user.is_superuser:
        return redirect('users:administracion_login')
    venta = Venta(request)
    variants = Variant.objects.all().filter(stock__lte=3)
    try:
        tienda = Tienda.objects.get(id=1)
    except Tienda.DoesNotExist:
        tienda = None
        
    template_name = "administracion/tienda/tienda_datos.html"
    return render(request,template_name,{"tienda":tienda,'variants':variants,'venta':venta})
    
class TiendaUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Tienda
    template_name = "administracion/tienda/tienda.html"
    form_class = TiendaForm
    success_url = reverse_lazy("administracion:index")
    success_message = "Registro modificado exitosamente!"

    def get_context_data(self,**kwargs):
        context = super(TiendaUpdateView,self).get_context_data(**kwargs)
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['title'] = 'Datos de la tienda'
        context['venta'] = Venta(self.request)
        return context

class TiendaCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Tienda
    template_name = "administracion/tienda/tienda.html"
    form_class = TiendaForm
    success_url = reverse_lazy("administracion:index")
    success_message = "Datos cargados exitosamente"
    error_message = "Error"
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Datos de la Tienda'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)        
        return context

class CarouselListView(ListView):
    template_name = "administracion/tienda/carousel_list.html"
    model = Carousel
    form_class = CarouselForm

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contenido Carousel'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

class CarouselCreateView(CreateView):
    model = Carousel
    template_name = "administracion/tienda/carousel.html"
    form_class = CarouselForm
    #cuando se le de submit
    success_url = reverse_lazy("administracion:carousel_list")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo contenido'
        context['boton'] = 'Agregar'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

class CarouselUpdateView(UpdateView):
    model = Carousel
    template_name = "administracion/tienda/carousel.html"
    form_class = CarouselForm
    success_url = reverse_lazy("administracion:carousel_list")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar contenido'
        context['boton'] = 'Modificar'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

class CarouselDelete(DeleteView):
    model = Carousel
    template_name = "administracion/carousel_delete.html"
    success_url = reverse_lazy("administracion:carousel")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Carousel'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

@login_required(login_url='users:administracion_login')
def eliminar_carousel(request,pk):
    template_name ="administracion/tienda/carousel_delete.html"
    carousel = get_object_or_404(Carousel,pk=pk)
    venta = Venta(request) 
    variants = Variant.objects.all().filter(stock__lte=3)
       
    
    if request.method == 'GET':
        context = {"carousel":carousel,'variants':variants,'venta':venta}
            
    if request.method == 'POST':
        carousel.delete()
        
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context) 



#---------------Proveedor--------------------------------------------
class ProveedorCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Proveedor
    template_name = "administracion/proveedor/proveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy("administracion:proveedor_listado")
    success_message = "Proveedor cargado exitosamente"
    error_message = "El proveedor que intenta agregar ya existe!"
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo proveedor'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

class ProveedorListView(LoginRequiredMixin,ListView):
    template_name = "administracion/proveedor/proveedores.html"
    model = Proveedor
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super(ProveedorListView,self).get_context_data(**kwargs)
        context['venta'] = Venta(self.request)
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        return context
    
class ProveedorUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Proveedor
    template_name = "administracion/proveedor/proveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy("administracion:proveedor_listado")
    success_message = "Registro modificado exitosamente!"
    login_url = 'users:administracion_login'
    def get_context_data(self,**kwargs):
        context = super(ProveedorUpdateView,self).get_context_data(**kwargs)
        context['venta'] = Venta(self.request)
        context['title'] = 'Editar datos de proveedor'
        context['boton'] = 'Editar'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        
        return context

@login_required(login_url='users:administracion_login')
def eliminar_proveedor(request,pk):
    template_name ="administracion/proveedor/delete.html"
    proveedor = get_object_or_404(Proveedor,pk=pk)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    if request.method == 'GET':
        context = {"proveedor":proveedor,'variants':variants,'venta':venta}
            
    if request.method == 'POST':
        proveedor.delete()
        
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)       

@login_required(login_url='users:administracion_login')
def editar_estado_proveedor(request,pk):
    template_name = 'administracion/proveedor/estado.html'
    proveedor = get_object_or_404(Proveedor,pk=pk)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    if request.method == 'GET':
        
        form = EstadoProveedorForm(instance=proveedor)
        
        context = {"proveedor":proveedor,"form":form,'variants':variants,'venta':venta}
        
    if request.method == "POST":
        proveedor.activo = request.POST.get('estado')
        
        form = EstadoProveedorForm(request.POST or None,request.FILES or None,instance=proveedor)
        
        if form.is_valid():
            
            print("El formulario es valido")
            form.save()
            messages.success(request,"Estado modificado exitosamente!")
        else:
            print("El formulario no es valido")
        return HttpResponse("ok")
    
        
    return render(request,template_name,context)

@login_required(login_url='users:administracion_login')
def pdf_proveedor(request,pk):
    template_path = 'administracion/proveedor/pdf.html'
    venta = Venta(request)
    proveedor = Proveedor.objects.get(pk=pk)
    context = {
        'proveedor':proveedor,
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

#----------- CATEGORÍA-------------------

class CategoriaListView(LoginRequiredMixin,ListView):
    template_name = "administracion/categorias/categoria_list.html"
    queryset= Categoria.objects.all().order_by('id')
    login_url = 'users:administracion_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

class CategoriaUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Categoria
    template_name = "administracion/categorias/categoria.html"
    form_class = CategoriaForm
    login_url = 'users:administracion_login'
    success_url = reverse_lazy("administracion:categorias")
    success_message = "Categoría modificada exitosamente"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoría'
        context['boton'] = 'Editar'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

class CategoriaCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Categoria
    template_name = "administracion/categorias/categoria.html"
    form_class = CategoriaForm
    login_url = 'users:administracion_login'
    success_url = reverse_lazy("administracion:categorias")
    success_message = "Categoría creada exitosamente"
    error_message = "La categoría que intenta agregar ya existe!"

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['title'] = 'Nueva Categoría'
        context['boton'] = 'Agregar'
        context['venta'] = Venta(self.request)
        return context


@login_required(login_url='users:administracion_login')
def eliminar_categoria(request,pk):
    template_name ="administracion/categorias/categoria_delete.html"
    categoria = get_object_or_404(Categoria,pk=pk)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    if request.method == 'GET':
        context = {"categoria":categoria,'variants':variants,'venta':venta}
            
    if request.method == 'POST':
        categoria.delete()
        
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context) 


#--------------SUBCATEGORIA---------------------

class SubcategoriaListView(LoginRequiredMixin,ListView):
    model = Subcategoria
    template_name = "administracion/subcategorias/subcategoria_list.html"
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class SubcategoriaUpdateView(LoginRequiredMixin,UpdateView):
    model = Subcategoria
    template_name = "administracion/subcategorias/subcategoria.html"
    form_class = SubcategoriaForm
    login_url = 'users:administracion_login'
    success_url = reverse_lazy("administracion:subcategorias")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Subcategoria'
        context['boton'] = 'Editar'
        return context

class SubcategoriaCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Subcategoria
    template_name = "administracion/subcategorias/subcategoria.html"
    form_class = SubcategoriaForm
    login_url = 'users:administracion_login'
    success_url = reverse_lazy("administracion:subcategorias")
    success_message = "Subcategoría creada exitosamente"
    error_message = "La subcategoría que intenta agregar ya existe!"

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Subcategoría'
        context['boton'] = 'Agregar'
        return context

@login_required(login_url='users:administracion_login')
def eliminar_subcategoria(request,pk):
    template_name ="administracion/subcategorias/subcategoria_delete.html"
    subcategoria = get_object_or_404(Subcategoria,pk=pk)
    
    
    if request.method == 'GET':
        context = {"subcategoria":subcategoria}
            
    if request.method == 'POST':
        subcategoria.delete()
        
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context) 

def alerta_stock(request):
    template_name = "administracion/productos/alerta_stock.html"
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    return render(request,template_name,{
        "variants":variants,
        "venta":venta
    })

def alerta_stock_menu(request):
    template_name = "administracion/productos/alerta_stock.html"
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)
    return render(request,template_name,{
        "variants":variants,
        "venta":venta
    })