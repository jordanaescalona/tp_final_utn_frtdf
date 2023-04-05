from django import forms
from django.forms import inlineformset_factory

from .models import (
    Product, Image, Variant
)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                    'class': 'form-control',
                    }
                ),
            'proveedor': forms.Select(attrs={
                    'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={
                    'class': 'form-control'
            }),
            'descripcion': forms.TextInput(attrs={
                    'class': 'form-control'
            }),
            'slug': forms.TextInput(attrs={
                'class':'form-control',
                'readonly':'readonly'
            }),
            'codigo_barras': forms.TextInput(attrs={
                'class':'form-control'
            }),
            'genero': forms.Select(attrs={
                    'class': 'form-control'
            }),
            'precio_compra': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'precio_venta': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ),    
        }


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'


class VariantForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autocomplete':'off'
                    }
                ),
            'talle': forms.Select(
                attrs={
                    'class': 'form-control',
                    
                    }
                ),
            'genero': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                ),
            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    
                    }
                )
        }


VariantFormSet = inlineformset_factory(
    Product, Variant, form=VariantForm,
    extra=1, can_delete=True, can_delete_extra=True
)
ImageFormSet = inlineformset_factory(
    Product, Image, form=ImageForm,
    extra=1, can_delete=True, can_delete_extra=True
)

class EstadoProductoForm(forms.ModelForm):
    class Meta: 
        model = Product
        fields = ['disponible',] 

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })