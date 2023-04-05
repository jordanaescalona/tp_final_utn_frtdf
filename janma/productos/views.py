from django.shortcuts import render, redirect
#mensajes
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#vistas basadas en clase
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView,DeleteView
)
#formularios
from .forms import (
    ProductForm, VariantFormSet, ImageFormSet,EstadoProductoForm
)
#modelos
from .models import (
    Image,
    Product,
    Variant
)

#decoradores
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#buscar objetos
from django.shortcuts import get_object_or_404
#respuesta
from django.http import HttpResponse

from ventas.venta import Venta

#--------------------producto----------------------------
#clase padre producto
class ProductInline():
    form_class = ProductForm
    model = Product
    template_name = "productos/product_create_or_update.html"
    
    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('products:list_products')

    def formset_variants_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        variants = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in variants:
            variant.product = self.object
            variant.save()

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        images = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.product = self.object
            image.save()
    
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)        
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['venta'] = Venta(self.request)
        return context

class ProductCreate(LoginRequiredMixin,SuccessMessageMixin,ProductInline,CreateView):
    login_url = 'users:administracion_login'
    success_message = "Producto cargado exitosamente!"

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['title'] = "Agregar nuevo producto"       
        ctx['variants'] = Variant.objects.all().filter(stock__lte=3)
        ctx['venta'] = Venta(self.request)

        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': VariantFormSet(prefix='variants'),
                'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
                'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }


class ProductUpdate(ProductInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx["title"] = "Editar producto"
        ctx['variants'] = Variant.objects.all().filter(stock__lte=3)
        ctx['venta'] = Venta(self.request)
        return ctx

    def get_named_formsets(self):
        return {
            'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }

class ProductList(ListView):
    model = Product
    template_name = "productos/product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        ctx = super(ProductList, self).get_context_data(**kwargs)
        ctx['variants'] = Variant.objects.all().filter(stock__lte=3)
        ctx['venta'] = Venta(self.request)
        return ctx

def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('products:update_product', pk=image.product.id)

    image.delete()
    messages.success(
            request, 'Imagen eliminada exitosamente!'
            )
    return redirect('products:update_product', pk=image.product.id)


def delete_variant(request, pk):
    try:
        variant = Variant.objects.get(id=pk)
    except Variant.DoesNotExist:
        messages.success(
            request, 'El detalle de producto no existe!'
            )
        return redirect('products:update_product', pk=variant.product.id)

    variant.delete()
    messages.success(
            request, 'Detalle de producto eliminado exitosamente!'
            )
    return redirect('products:update_product', pk=variant.product.id)

@login_required(login_url='users:administracion_login')
def producto_editar_estado(request,pk):
    template_name = 'productos/estado.html'
    producto = get_object_or_404(Product,id=pk)
    variants = Variant.objects.all().filter(stock__lte=3)
    venta = Venta(request)

    if request.method == 'GET':
        
        form = EstadoProductoForm(instance=producto)
        
        context = {"producto":producto,"form":form,'variants':variants,'venta':venta}
        
    if request.method == "POST":
        producto.disponible = request.POST.get('id_disponible')
        
        form = EstadoProductoForm(request.POST or None,request.FILES or None,instance=producto)
        
        if form.is_valid():
            
            print("El formulario es valido")
            form.save()
            messages.success(request,"Estado modificado exitosamente!")
        else:
            print("El formulario no es valido")
        return HttpResponse("ok")
    
        
    return render(request,template_name,context)

@login_required(login_url='users:administracion_login')
def producto_delete(request,pk):
    template_name ="productos/eliminar/delete.html"
    producto = get_object_or_404(Product,id=pk)
    venta = Venta(request)
    imagenes = Image.objects.all().filter(product=producto)
    variant = Variant.objects.all().filter(product=producto)
    if request.method == 'GET':
        context = {"producto":producto,'venta':venta}
            
    if request.method == 'POST':
        print("imagenes:"+str(imagenes))
        for i in imagenes:
            i.image.delete()
        for v in variant:
            v.delete()    
            
        producto.delete()
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)


    