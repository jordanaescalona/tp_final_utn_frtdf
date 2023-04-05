from import_export import resources  
from .models import Producto

class ProductoResource(resources.ModelResource):  
   class Meta:  
     model = Producto   
 