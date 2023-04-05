from django.shortcuts import render
from .models import Carousel,Tienda
from administracion.models import Categoria
from django.views.generic import TemplateView
from django.db.models import Q
from django.views.generic import ListView,DetailView
from productos.models import Variant,Product,Image
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchHeadline
from django.shortcuts import get_object_or_404
#formularios
from users.models import User
#

from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from carritos.cart import Cart
from tienda.models import Tienda
# Create your views here.

class index(TemplateView):
    template_name = 'tienda/index.html'
    
    def get_context_data(self,**kwargs):
        context = super(index,self).get_context_data(**kwargs)
        context['productos'] = Product.objects.all().filter(disponible=True)
        context['categorias'] = Categoria.objects.all().filter(activo=True)
        context['carousel'] = Carousel.objects.all()
        context['tienda'] = Tienda.objects.get(id=1)
        context['cart'] = Cart(self.request)

        #------------MUJERES----------------------------
        producto_mujeres = Product.objects.all().filter(genero="MUJER")
        categoria_mujeres = []
        for pm in producto_mujeres:
            if pm.categoria.nombre not in categoria_mujeres:
                categoria_mujeres.append(pm.categoria.nombre)
        context['categorias_mujeres'] = categoria_mujeres
        #---------HOMBRE--------------------------------
        producto_hombres = Product.objects.all().filter(genero="HOMBRE")
        categoria_hombres = []
        for pm in producto_hombres:
            if pm.categoria.nombre not in categoria_hombres:
                categoria_hombres.append(pm.categoria.nombre)
        context['categorias_hombres'] = categoria_hombres
        #----------UNISEX-------------------------------
        producto_unisex = Product.objects.all().filter(genero="UNISEX")
        categoria_unisex = []
        for pm in producto_unisex:
            if pm.categoria.nombre not in categoria_unisex:
                categoria_unisex.append(pm.categoria.nombre)
        context['categorias_unisex'] = categoria_unisex
        #-----------------------------------------------
        return context

class BuscadorProductos(ListView):
    template_name = 'tienda/search.html'

    def get_queryset(self):
        filtros = Q(color__icontains=self.query()) | Q(talle__icontains=self.query()) | Q(genero__icontains=self.query()) | Q(product__title__icontains=self.query()) | Q(product__categoria__nombre__icontains=self.query()) | Q(product__descripcion__icontains=self.query()) 
        return Variant.objects.filter(filtros)
    
    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['variant_list'].count()
        context['productos'] = Product.objects.all().filter(disponible=True)
        context['categorias'] = Categoria.objects.all().filter(activo=True)
        context['tienda'] = Tienda.objects.get(id=1)
         #------------MUJERES----------------------------
        producto_mujeres = Product.objects.all().filter(genero="MUJER")
        categoria_mujeres = []
        for pm in producto_mujeres:
            if pm.categoria.nombre not in categoria_mujeres:
                categoria_mujeres.append(pm.categoria.nombre)
        context['categorias_mujeres'] = categoria_mujeres
        #---------HOMBRE--------------------------------
        producto_hombres = Product.objects.all().filter(genero="HOMBRE")
        categoria_hombres = []
        for pm in producto_hombres:
            if pm.categoria.nombre not in categoria_hombres:
                categoria_hombres.append(pm.categoria.nombre)
        context['categorias_hombres'] = categoria_hombres
        #----------UNISEX-------------------------------
        producto_unisex = Product.objects.all().filter(genero="UNISEX")
        categoria_unisex = []
        for pm in producto_unisex:
            if pm.categoria.nombre not in categoria_unisex:
                categoria_unisex.append(pm.categoria.nombre)
        context['categorias_unisex'] = categoria_unisex
        print(context)
        return context

def BuscadorProductos2(request):
    qs = Product.objects.all()
    query = request.GET.get("query")
    tienda = Tienda.objects.get(id=1)
    productos = Product.objects.all().filter(disponible=True)
    categorias = Categoria.objects.all().filter(activo=True)
    cart = Cart(request)
    #------------MUJERES----------------------------
    producto_mujeres = Product.objects.all().filter(genero="MUJER")
    categoria_mujeres = []
    for pm in producto_mujeres:
        if pm.categoria.nombre not in categoria_mujeres:
            categoria_mujeres.append(pm.categoria.nombre)
    categorias_mujeres = categoria_mujeres
    #---------HOMBRE--------------------------------
    producto_hombres = Product.objects.all().filter(genero="HOMBRE")
    categoria_hombres = []
    for pm in producto_hombres:
        if pm.categoria.nombre not in categoria_hombres:
            categoria_hombres.append(pm.categoria.nombre)
    categorias_hombres = categoria_hombres
    #----------UNISEX-------------------------------
    producto_unisex = Product.objects.all().filter(genero="UNISEX")
    categoria_unisex = []
    for pm in producto_unisex:
        if pm.categoria.nombre not in categoria_unisex:
            categoria_unisex.append(pm.categoria.nombre)
    categorias_unisex = categoria_unisex
    #-----------------------------------------------
    if query:
        """ qs = Variant.objects.annotate(
            headline=SearchHeadline(
                "product__descripcion",
                #"genero",
                SearchQuery(query),
                start_sel="<b><u><i>",
                stop_sel="</i></u></b>",
            )
        ) """
        qs = Product.objects.annotate(search=SearchVector("title", "descripcion","categoria","variant__color","variant__talle","genero")).filter(search=SearchQuery(query))
        consulta = []
        for q in qs:
            if q not in consulta:
                consulta.append(q)

    count = 0
    for c in consulta:
        count = count + 1    

        
    return render(request,'tienda/busqueda.html',context={
        "cart":cart,
        "queryset":consulta,
        "query":query,
        "count":count,
        "tienda": tienda,
        "productos":productos,
        "categorias":categorias,
        "categorias_mujeres":categorias_mujeres,
        "categorias_hombres":categorias_hombres,
        "categorias_unisex":categorias_unisex 
        })

def producto_categoria_genero(request,genero,categoria):
    template_name = "tienda/categoria_genero.html"
    productos = Product.objects.all().filter(disponible=True)
    productoss = Product.objects.all().filter(genero=genero,categoria__nombre=categoria,disponible=True)    
    tienda = Tienda.objects.get(id=1)
    categorias = Categoria.objects.all().filter(activo=True)
    cart = Cart(request)
    #------------MUJERES----------------------------
    producto_mujeres = Product.objects.all().filter(genero="MUJER")
    categoria_mujeres = []
    for pm in producto_mujeres:
        if pm.categoria.nombre not in categoria_mujeres:
            categoria_mujeres.append(pm.categoria.nombre)
    categorias_mujeres = categoria_mujeres
    #---------HOMBRE--------------------------------
    producto_hombres = Product.objects.all().filter(genero="HOMBRE")
    categoria_hombres = []
    for pm in producto_hombres:
        if pm.categoria.nombre not in categoria_hombres:
            categoria_hombres.append(pm.categoria.nombre)
    categorias_hombres = categoria_hombres
    #----------UNISEX-------------------------------
    producto_unisex = Product.objects.all().filter(genero="UNISEX")
    categoria_unisex = []
    for pm in producto_unisex:
        if pm.categoria.nombre not in categoria_unisex:
            categoria_unisex.append(pm.categoria.nombre)
    categorias_unisex = categoria_unisex
    #-----------------------------------------------
    return render(request,template_name,{
        "cart":cart,
        'productos':productos,
        'productoss':productoss,
        'tienda':tienda,
        'categorias':categorias,
        "categorias_mujeres":categorias_mujeres,
        "categorias_hombres":categorias_hombres,
        "categorias_unisex":categorias_unisex,
        "genero":genero,
        "categoria":categoria 
    })

def producto_detalle(request,pk):
    template_name = 'tienda/productos/producto_detalle.html'
    producto = get_object_or_404(Product,id=pk)    
    productos = Product.objects.all().filter(disponible=True)
    v_talles = Variant.objects.all().filter(product_id=pk)
    images = Image.objects.all().filter(product_id=pk)
    cart = Cart(request)
    talles = []
    colores = []
    for t in v_talles:
        if t.talle not in talles:
            talles.append(t.talle)
    
    for c in v_talles:
        if c.color not in colores:
            colores.append(c.color)

    tienda = Tienda.objects.get(id=1)
    #------------MUJERES----------------------------
    producto_mujeres = Product.objects.all().filter(genero="MUJER")
    categoria_mujeres = []
    for pm in producto_mujeres:
        if pm.categoria.nombre not in categoria_mujeres:
            categoria_mujeres.append(pm.categoria.nombre)
    categorias_mujeres = categoria_mujeres
    #---------HOMBRE--------------------------------
    producto_hombres = Product.objects.all().filter(genero="HOMBRE")
    categoria_hombres = []
    for pm in producto_hombres:
        if pm.categoria.nombre not in categoria_hombres:
            categoria_hombres.append(pm.categoria.nombre)
    categorias_hombres = categoria_hombres
    #----------UNISEX-------------------------------
    producto_unisex = Product.objects.all().filter(genero="UNISEX")
    categoria_unisex = []
    for pm in producto_unisex:
        if pm.categoria.nombre not in categoria_unisex:
            categoria_unisex.append(pm.categoria.nombre)
    categorias_unisex = categoria_unisex
    #-----------------------------------------------
    
    if request.method == 'GET' and request.GET.get('cantidad') and request.GET.get('talle') and request.GET.get('color'):
       
        color = request.GET.get('color')           
        objs = Variant.objects.all().filter(id=color)        
        if len(objs) == 1:
            variant = objs[0]    
        else:
           pass       
        
        cart = Cart(request)
        cart.add(variant,int(request.GET.get('cantidad')))
        if cart:
            messages.success(request,"Producto agregado exitosamente al carrito!")
        else:
            messages.error(request,"NO se pudo agregar el producto")
        return redirect('tienda:producto_detalle',pk=pk)
    
    return render(request,template_name,{
        'producto':producto,
        'productos':productos,
        'talles':talles,
        'colores':colores,
        "variants":v_talles,
        "images":images,
        "categorias_mujeres":categorias_mujeres,
        "categorias_hombres":categorias_hombres,
        "categorias_unisex":categorias_unisex,
        'cart':cart 

    })
def get_products(request):
    products = list(Product.objects.values())
    if(len(products)>0):
        data = {'message':'success','products':products}
    else:
        data = {'message':'Not fount'}
    print(data)
    return JsonResponse(data)

def get_variants(request,talle):
    variants = list(Variant.objects.filter(talle=talle).values())
    if(len(variants)>0):
        data = {'message':'success','variants':variants}
    else:
        data = {'message':'Not fount'}
    print(data)
    return JsonResponse(data)
