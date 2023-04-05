from django import forms
#from django.contrib.auth.models import User
from users.models import User,Administrador
from .models import Proveedor
from .models import Categoria,Subcategoria
from tienda.models import Tienda,Carousel
from django.utils.html import format_html


#-----------Categoria-----------------------
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
    
        widgets ={
                    'nombre': forms.TextInput(attrs={
                        'name':'nombre',
                        'id':'nombre',
                        'class':'form-control'
                    }),
                    'ganancia': forms.NumberInput(attrs={
                        'name':'ganancia',
                        'id':'ganancia',
                        'class':'form-control'
                    }),
                    'activo':forms.CheckboxInput(attrs={
                        'name':'activo',
                        'id':'activo',
                        'class':'form-check-input'
                    }),
                }
    

    def clean(self):
        valor = self.cleaned_data["nombre"]
        try:
            
            if Categoria.objects.filter(nombre=valor).exists() and Categoria.activo == True:
            
                print("Registro ya existe")
                
                raise forms.ValidationError(format_html('<h2 style="color:white;background:red;list-style:none">{}</h2>',"El registro ya existe."))

            elif self.instance.pk != Categoria.objects.get(nombre=valor).pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio no permitido.")
            
            
        except Categoria.DoesNotExist:
            pass
        return self.cleaned_data

#--------------Subcategoria---------------------------
class SubcategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.filter(activo=True).order_by('nombre'))
    class Meta:
        model = Subcategoria
        fields = '__all__'

        widgets ={
                     
                    'activo':forms.CheckboxInput(attrs={
                        'name':'activo',
                        'id':'activo',
                        'class':'form-check-input'
                    })
                }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
       
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        
        #agregamos valor por default
        self.fields['categoria'].empty_label = "---Seleccione Categoría---"


#---------------------Usuario--------------------------------------------
class RegistroForm(forms.Form):
    #definimos atributos(inputs del formulario)
    username = forms.CharField(required=True,min_length=4,max_length=100, label="Nombre de Usuario",
                widget=forms.TextInput(attrs={
                    'class':'form-control',
                    'id':'username',
                    'placeholder':'Ingrese un nombre de usuario',
                    
                }))
    email = forms.EmailField(required=True,label="Correo electrónico",
                widget=forms.EmailInput(attrs={
                    'class':'form-control',
                    'id':'email',
                    'placeholder':'Ingrese su correo electrónico',
                    
                }))
    password = forms.CharField(required=True,label="Contraseña",
                widget=forms.PasswordInput(attrs={
                    'class':'form-control',
                    'id':'password',
                    'placeholder':'Ingrese una contraseña',
                    
                }))
    password2 = forms.CharField(required=True,label="Confirmar contraseña",
                widget=forms.PasswordInput(attrs={
                    'class':'form-control',
                    'id':'password2',
                    'placeholder':'Repita la contraseña',
                    
                }))

    #validamos
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya existe!')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya se encuentra en uso!")
        return email

    #validamos campo que depende de otro
    def clean(self):
        #obtenemos todos los datos del formulario
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            #Agregamos error al campo psw2(1 argumento:campo,2 argumento:error)
            self.add_error('password2','Las contraseñas no coinciden')
    
    #delegamos la responsabilidad de crear nuevos usuarios a nuestro formulario
    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )


#--------------------Tienda---------------------------
class TiendaForm(forms.ModelForm):
    class Meta:
        model = Tienda
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for fiel in iter(self.fields):
            self.fields[fiel].widget.attrs.update({
                'class':'form-control'
            })



    
#------------------PROVEEDORES----------
class ProveedorForm(forms.ModelForm):
    class Meta: 
        model = Proveedor
        fields = '__all__'

        widgets ={
                    'nombre': forms.TextInput(attrs={
                        'name':'nombre',
                        'id':'nombre',
                        'class':'form-control'
                    }),
                    'telefono':forms.TextInput(attrs={
                        'name':'telefono',
                        'id':'telefono',
                        'class':'form-control'
                    }),
                    'direccion':forms.TextInput(attrs={
                        'name':'direccion',
                        'id':'direccion',
                        'class':'form-control'
                    }),
                    'cp':forms.TextInput(attrs={
                        'name':'cp',
                        'id':'cp',
                        'class':'form-control'
                    }),
                    'email':forms.TextInput(attrs={
                        'name':'email',
                        'id':'email',
                        'class':'form-control'
                    }),
                    'web':forms.TextInput(attrs={
                        'name':'web',
                        'id':'web',
                        'class':'form-control'
                    }),
                    'observaciones':forms.Textarea(attrs={
                        'name':'observaciones',
                        'id':'observaciones',
                        'class':'form-control'
                    }),
                    'activo':forms.CheckboxInput(attrs={
                        'name':'activo',
                        'id':'activo',
                        'class':'form-check-input'
                    }),
                }

class EstadoProveedorForm(forms.ModelForm):
    class Meta: 
        model = Proveedor
        fields = ['activo',] 

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

