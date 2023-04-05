from django import forms
from .models import Catalogo,Producto,Pedido,DetallePedido

class CatalogoForm(forms.ModelForm):
    class Meta:
        model = Catalogo
        fields = ('proveedor','archivo')

        widgets ={
                    'proveedor': forms.Select(attrs={
                        
                        'class':'form-control'
                    }),
                    'archivo': forms.FileInput(attrs={
                        
                        'class':'form-control',
                        'accept':".xlsx"
                    })
                }
        
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            
            for field in iter(self.fields):
                self.fields[field].widget.attrs.update({
                    'class':'form-control'
                })

class CatalogoListForm(forms.ModelForm):
    class Meta:
        model = Catalogo
        fields = '__all__'

        widgets ={
                    'proveedor': forms.Select(attrs={
                        
                        'class':'form-control'
                    }),
                    'archivo': forms.FileInput(attrs={
                        
                        'class':'form-control'
                    })
                }
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class PedidoNewForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

        widgets ={
                    'fecha_pedido': forms.DateInput(attrs={
                        'class':'form-control',
                        'readonly':'readonly',
                        'id':'fecha_pedido'
                    }),
                    'observaciones':forms.Textarea(attrs={
                         'class':'form-control'
                    }),
                    'catalogo':forms.TextInput(attrs={
                        'readonly':'readonly',    
                        'class':'form-control'
                    }),
                    'factura': forms.FileInput(attrs={                        
                        'class':'form-control'
                    }),'fecha_factura': forms.DateInput(attrs={
                        'class':'form-control',
                        'readonly':'readonly',
                        'id':'fecha_factura'
                    }),
                    'recibido':forms.CheckboxInput(attrs={
                        'class':'h1 text-danger form-control border border-danger'
                    }),
                    'total':forms.NumberInput(attrs={
                        'readonly':'readonly',
                        'class':'form-control'
                    }),
                    'envio':forms.NumberInput(attrs={
                        
                        'class':'form-control'
                    }),
                    'pagar':forms.NumberInput(attrs={
                        'readonly':'readonly',
                        'class':'form-control'
                    }),
                }
    
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('observaciones','catalogo','total','recibido','envio','pagar')

        widgets ={                    
                    'observaciones':forms.Textarea(attrs={
                         'class':'form-control'
                    }),
                    'catalogo':forms.TextInput(attrs={
                        'readonly':'readonly',    
                        'class':'form-control'
                    }),
                    
                    'recibido':forms.CheckboxInput(attrs={
                        'class':'h1 text-danger form-control border border-danger'
                    }),
                    'total':forms.NumberInput(attrs={
                        'readonly':'readonly',
                        'class':'form-control'
                    }),
                    'envio':forms.NumberInput(attrs={
                        
                        'class':'form-control'
                    }),
                    'pagar':forms.NumberInput(attrs={
                        'readonly':'readonly',
                        'class':'form-control'
                    }),
                }
    