from django.urls import reverse

def breadcrumb(datos=True,products=False,confirmacion=False):
    return [
        {'title':'Datos','active':datos,'url':('ventas:confirmar_venta')},
        {'title':'Productos','active':products,'url':('ventas:confirmar_productos')},
        {'title':'Confirmación','active':confirmacion,'url':('ventas:confirmacion')}
    ]