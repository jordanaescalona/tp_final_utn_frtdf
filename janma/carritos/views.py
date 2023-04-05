from django.shortcuts import render
from carritos.cart import Cart
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from productos.models import Product,Variant
from tienda.models import Tienda
from django.contrib import messages 
# Create your views here.

def cart(request):
    template_name = "carritos/cart.html"
    """ user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.get(cart_id=cart_id)
    else:
        cart = Cart.objects.create(user=user)
    request.session['cart_id'] = cart.cart_id """
    variants = Variant.objects.all().filter(product__disponible=True)    
    productos = Product.objects.all().filter(disponible=True)
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
    cart = Cart(request)
    """ 
    if request.method == "GET" and request.GET.get('cantidad') and request.GET.get('variantId'):
        cantidad = request.GET.get('cantidad')        
        variantId = request.GET.get('variantId')        
        if not variantId == 'None':           
            
            variant = get_object_or_404(Variant,id=variantId)
            if variant:
                cart.actualizar_cantidad(variant,int(cantidad))
                
        else:
            pass
      """   

       
    return render(request,template_name,{
        'productos':productos,
        'variants':variants,
        'cart':cart,
        'tienda':tienda,
        "categorias_mujeres":categorias_mujeres,
        "categorias_hombres":categorias_hombres,
        "categorias_unisex":categorias_unisex 
    })
    
def vaciar_carrito(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request,'Carrito vaciado exitosamente!')
    return redirect('cart:cart')

def eliminar_producto_carrito(request,id):
    cart = Cart(request)
    variant = get_object_or_404(Variant,id=id)
    cart.remove(variant)
    messages.success(request,'Producto eliminado')
    return redirect('cart:cart')

def agregar_producto(request,variant_id,cantidad):
    cart = Cart(request)
    variant = get_object_or_404(Variant,id=variant_id)
    cart.add(variant=variant,cantidad=cantidad)

    return redirect('tienda:producto_detalle',pk=variant.product.id)

def actualizar_carrito(request,variant_id,cantidad):
    cart = Cart(request)
    variant = get_object_or_404(Variant,id=variant_id)
    cart.actualizar_cantidad(variant,cantidad)

    return redirect('cart:cart')
