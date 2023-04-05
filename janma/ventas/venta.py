from decimal import Decimal
from django.conf import settings
from productos.models import Product,Variant

from django.shortcuts import get_object_or_404
from django.contrib import messages 


class Venta(object):
    
    def __init__(self,request):
        self.session = request.session
        venta = self.session.get(settings.VENTA_SESSION_ID)
        if not venta:
            venta = self.session[settings.VENTA_SESSION_ID] = {} #VA A SER UN DICCIONARIO VACIO
        self.venta = venta
    #creamos un iterable para la session de ventas
    #con esto vamos a poder iterar todos los elementos de la venta, ya sea desde el view o desde el template
    def __iter__(self):
        #lo primero que queremos hacer es obtener la referencia a todas las claves
        variant_ids = self.venta.keys()
        #obtenemos todos los elementos
        #como queremos obtener muchos ids vamos a colocar la clausula __in
        variants = Variant.objects.filter(id__in=variant_ids)
        
        venta = self.venta.copy()
        
        #ahora realizamos la operacion de iteracion
        for variant in variants:
            #va a ser la venta en la posicion producto
            venta[str(variant.id)]['variant'] = variant
        
        #imprimimos el elemento
        for item in venta.values():
            #actualizacion del precio del producto en decimal
            item['precio'] = Decimal(item['precio'])
            #total del precio del producto (producto precio * cantidad)
            item['precio_total'] = item['precio'] * item['cantidad'] #Para ver el precio total vamos a llamar a esta variable (c.precio_total) 
                        
            #hacemos un retorno parcial llamado yield
            #nos permite retornar un valor con el cual estamos operando en este punto
            #el yield recuerda la posicion exacta donde quedamos y una vez que muestre el primer elemento
            #va a continuar con el segundo elemento y asi sucesivamente
            yield item

    #calcular la cantidad total de todos los productos
    #en python tenemos la funcion __len__ para realizar esto
    def __len__(self):
       #lo unico que nos interesa es sumar la cantidad de elementos
       return sum(item['cantidad'] for item in self.venta.values())
    
    def add(self,variant,cantidad=1,override_cantidad=False):
        
        variant_id = str(variant.id)   
             
        if variant_id not in self.venta:
            
            self.venta[variant_id] = {
                'variant_id':variant_id,
                'cantidad':0,
                'precio':str(variant.product.precio_venta)}
           
        
        if override_cantidad:
            
            self.venta[variant_id]['cantidad'] = cantidad
            
        else:
            
            self.venta[variant_id]['cantidad'] += cantidad
           
        self.save()
    
        return self.venta[variant_id]
    
    def save(self):
        self.session.modified = True
    
    
    def remove(self,variant):
        variant_id = str(variant.id)
        
        if variant_id in self.venta:
           
            del self.venta[variant_id]
        self.save()

    #Borramos toda la venta
    def clear(self):
        #a las sessions podemos acceder como si fueran arrays[] o como () pasandole de manera opcional el valor
        #En este caso a diferencia del init que lo colocamos entre parentesis lo hacemos con corchetes 
        del self.session[settings.VENTA_SESSION_ID]
        self.save()
    
    
    
    #metodo para calcular el precio total de todos los productos que tenemos en la venta
    def get_total_price(self):
        #utilizamos la funcion sum para sumar todo
        #convertimos el precio en decimal ya que mas arriba lo estamos manipulando como str
        #la cantidad es un entero        
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.venta.values())
    
    def venta_total_price(self):
        total = 0.00
        for key,value in self.venta.items():
            total = total + (float(value['precio'])*value['cantidad'])
        return total


    


            

    
    