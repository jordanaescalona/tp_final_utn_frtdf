from decimal import Decimal
from django.conf import settings
from productos.models import Product,Variant
import copy

class Cart(object):
    #constructor init es el encargado de recibir la peticion
    # colocamos self porque es un metodo creado desde dentro de la clase 
    def __init__(self,request):
       #inicializamos la session del carrito
        self.session = request.session
        # obtenemos la peticion a la key del carrito
        cart = self.session.get(settings.CART_SESSION_ID) 

        #Verificamos el estado de la key si la session car existe
        #si no existe inicializamos
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {} #VA A SER UN DICCIONARIO VACIO

        #Si existe, simplemente vamos a retornar el cart
        self.cart = cart
    
    #metodo para agregar productos al carrito
    #la cantidad por defecto es 1
    #el 4 parametro nos va a permitir sobreescribir todas las cantidades que ya tengamos, es decir si ya tenemos el producto 
    #en el carrito solo le aumentamos 1 unidad, por defecto va a estar inicializado en falso
    def add(self,variant,cantidad=1,override_cantidad=False):
        #buscamos el producto
        #vamos a trabajar con str porque es la manera mas sencilla de mapear
        variant_id = str(variant.id)
        #verificamos si ya tenemos este elemento en la session del carrito de compras
        #si no existe lo inicializamos en nuestro carrito
        if variant_id not in self.cart:
            #Le pasamos el precio y la cantidad
            #por defecto la cantidad va a ser 0 y el precio lo almacenamos como string para eviar conflictos con los tipos de las variables
            self.cart[variant_id] = {
                'variant_id':variant_id,
                'cantidad':0,
                'precio':str(variant.product.precio_venta)}
        
        #preguntamos por el atributo override
        #si existe significa que queremos sobreescribir las cantidades
        if override_cantidad:
            #necesitamos inicializar la posicion de la cantidad que en el diccionario es 0
            #a la cantidad que por default es 1, para hacer acceder a la posicion cantidad de un diccionario 
            #lo hacemos como si fuera un array
            self.cart[variant_id]['cantidad'] = cantidad
        #el comportamiento habitual seria sumar en 1 las cantidades
        else:
            self.cart[variant_id]['cantidad'] += cantidad
        
        #llamamos al metodo que vamos a crear más abajo, llamado save para saber que hemos modificado la session
        self.save()
        return self.cart[variant_id]
    #lo que va a hacer la funcion save es indicar con un booleano una bandera que indica que hemos modificado la session
    def save(self):
        #para modificar la session utilizamos session.modified
        self.session.modified = True
    
    #creamos metodo que nos va a permitir remover un producto del carrito de compras
    #recibimos la referencia al elemento que queremos remover
    def remove(self,variant):
        variant_id = str(variant.id)
        #preguntamos si el producto se encuentra dentro de la session del carrito
        if variant_id in self.cart:
            #si existe utilizamos la funcion del para eliminar dentro de la session 
            del self.cart[variant_id]
        self.save()

    # metodo para eliminar todo nuestro carrito
    def clear(self):
        #a las sessions podemos acceder como si fueran arrays[] o como () pasandole de manera opcional el valor
        #En este caso a diferencia del init que lo colocamos entre parentesis lo hacemos con corchetes 
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    #creamos un iterable para la session del carrito
    #con esto vamos a poder iterar todos los elementos de nuestro carrito, ya sea desde el view o desde el template
    def __iter__(self):
        #lo primero que queremos hacer es obtener la referencia a todas las claves
        variant_ids = self.cart.keys()
        #obtenemos todos los elementos
        #como queremos obtener muchos ids vamos a colocar la clausula __in
        variants = Variant.objects.filter(id__in=variant_ids)
        #vamos a hacer una copia del carrito para mas adelante poder manipular o cambiar la estructura del carrito
        #no vamos a querer que sea permanente, solo queremos que sea para esta opcion
        cart = self.cart.copy()
        #cart = copy.deepcopy(self.cart)
        #ahora realizamos la operacion de iteracion
        for variant in variants:
            #va a ser el carrito en la posicion producto
            cart[str(variant.id)]['variant'] = variant
        
        #imprimimos el elemento
        for item in cart.values():
            #actualizacion del precio del producto en decimal
            item['precio'] = Decimal(item['precio'])
            #total del precio del producto (producto precio * cantidad)
            item['precio_total'] = item['precio'] * item['cantidad'] #Para ver el precio total vamos a llamar a esta variable (c.precio_total) 
            
            
            #hacemos un retorno parcial llamado yield
            #nos permite retornar un valor con el cual estamos operando en este punto
            #el yield recuerda la posicion exacta donde quedamos y una vez que muestre el primer elemento
            #va a continuar con el segundo elemento y asi sucesivamente
            yield item
    
    #metodo para calcular el precio total de todos los productos que tenemos en el carrito
    def get_total_price(self):
        #utilizamos la funcion sum para sumar todo
        #convertimos el precio en decimal ya que mas arriba lo estamos manipulando como str
        #la cantidad es un entero
        #iteramos todos los valores de el carrito (cart.values())todo en una misma linea de codigo
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.cart.values())
    
    def cart_total_price(self):
        total = 0.00
        for key,value in self.cart.items():
            total = total + (float(value['precio'])*value['cantidad'])
        return total


    #calcular la cantidad total de todos los productos
    #en python tenemos la funcion __len__ para realizar esto
    def __len__(self):
       #lo unico que nos interesa es sumar la cantidad de elementos
       return sum(item['cantidad'] for item in self.cart.values())


    def actualizar_cantidad(self,variant,cantidad):        
        
        variant_id = str(variant.id)
        if variant_id in self.cart:
            self.cart[variant_id]['cantidad'] = cantidad

        self.save()

            

    
    