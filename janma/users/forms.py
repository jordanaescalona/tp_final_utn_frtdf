from django import forms

from .models import Cliente,Administrador,User

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

    
class RegistroForm(forms.ModelForm):

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
    
    class Meta:
        model = User
        fields = ('username','email','fecha_nacimiento','password')
        widgets ={
            'username':forms.TextInput(attrs={
                    'class':'form-control',
                    'id':'username',
                    'placeholder':'Ingrese un nombre de usuario',
                    'autocomplete':'off'
                    
            }),
            'email':forms.EmailInput(attrs={
                    'class':'form-control',
                    'id':'email',
                    'placeholder':'Ingrese su correo electrónico',
                    
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                        'class':'form-control',
                        'readonly':'readonly',
                        'id':'fecha_nacimiento',
                        'placeholder':'Ingrese fecha de nacimiento'
            })
        }
    
    def clean(self):
        cleaned_data = super(RegistroForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            self.add_error('password2','Las contraseñas no coinciden')
            
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

            
    
    
class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['last_login','username','date_joined','first_name','last_name','email',]

        widgets ={
                    'last_login': forms.DateTimeInput(attrs={
                        'readonly':'readonly',
                        'class':'form-control'
                    }),
                    'username': forms.TextInput(attrs={
                        'readonly':'readonly',
                        'class':'form-control'
                    }),
                    'date_joined': forms.DateTimeInput(attrs={
                        'readonly':'readonly',
                        'class':'form-control'
                    }),
                    'first_name': forms.TextInput(attrs={
                        'class':'form-control'
                    }),
                    'last_name': forms.TextInput(attrs={
                        'class':'form-control'
                    }),
                    'email': forms.EmailInput(attrs={
                        'class':'form-control'
                    })
                    
        }

        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            for field in iter(self.fields):
                self.fields[field].widget.attrs.update({
                    'class':'form-control'
                })

class CambiarPasswordForm(forms.Form):
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Ingrese nueva contraseña...',
        'id': 'password1',
        'required':'required'
    }))
    password2 = forms.CharField(label="Confirmar contraseña",widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Repetir contraseña...',
        'id': 'password2',
        'required':'required'
    }))

    def clean_password2(self):
        #validamos contraseñas
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')

        if pass1 != pass2:
            raise forms.ValidationError('Las contraseñas no coinciden!')
        return pass2