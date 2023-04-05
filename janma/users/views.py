from django.shortcuts import render
from .models import Cliente,Administrador,User
from django.views.generic import CreateView, DeleteView, UpdateView, View, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse
from productos.models import Variant,Product
from tienda.models import Tienda
from .forms import ClienteForm,RegistroForm,AdministradorForm,CambiarPasswordForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
# Create your views here.

class ClienteCreateView(SuccessMessageMixin,CreateView):
    model = Cliente
    template_name = "users/administracion/registro.html"
    form_class = ClienteForm
    success_url = reverse_lazy("users:clientes")
    success_message = "Cliente cargado exitosamente"
    error_message = "El cliente que intenta agregar ya existe!"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo cliente'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['button'] = 'Registrar'
        return context
    
class VolverClienteVentaView(SuccessMessageMixin,CreateView):
    model = Cliente   
    template_name = "users/administracion/registro.html" 
    form_class = ClienteForm
    
    success_message = "Cliente cargado exitosamente"
    error_message = "El cliente que intenta agregar ya existe!"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo cliente'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['button'] = 'Registrar'
        return context
    
    def get_success_url(self):
        return reverse('ventas:confirmar_venta',)
    
class ClienteListView(SuccessMessageMixin,ListView):
    model = Cliente
    template_name = "users/administracion/listado_clientes.html"
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        return context

class ClienteUpdateView(SuccessMessageMixin,UpdateView):
    model = Cliente
    template_name = "users/administracion/registro.html"
    form_class = ClienteForm
    success_url = reverse_lazy("users:clientes")
    success_message = "Cliente modificado exitosamente"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar/Ver cliente'
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        context['button'] = 'Modificar'
        return context

@login_required(login_url='users:administracion_login')
def eliminar_cliente(request,pk):
    template_name ="users/administracion/delete.html"
    cliente = get_object_or_404(Cliente,pk=pk)
    variants = Variant.objects.all().filter(stock__lte=3)
    
    if request.method == 'GET':
        context = {"cliente":cliente,'variants':variants}
            
    if request.method == 'POST':
        cliente.delete()
        
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)   


# -------------- usuario administración ---------------------

#Editar datos de administrador
class AdministradorUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Administrador
    template_name = "users/administracion/perfil.html"
    form_class = AdministradorForm
    success_url = reverse_lazy("administracion:index")
    success_message = "Registro modificado exitosamente!"
    login_url = 'users:administracion_login'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        return context

#Login
def administracion_login(request):
    template_name = "users/administracion/login.html"
    variants = Variant.objects.all().filter(stock__lte=3)
    if request.user.is_authenticated :
        return redirect('administracion:index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        
        if user:
            login(request,user)
            messages.success(request,'¡Bienvenido {}!'.format(user.username))
            return redirect('administracion:index')
        else:
            messages.error(request,'Usuario o contraseña no validos.')
            return redirect('users:administracion_login')
    return render(request,template_name,{
        'variants':variants
    })

#logout usuario
def administracion_logout(request):
    logout(request)
    messages.success(request,'Sesión cerrada exitosamente!')
    return redirect('users:administracion_login')

#Cambiar contraseña de administrador
class CambiarPasswordView(LoginRequiredMixin,SuccessMessageMixin,View):
    template_name = 'users/administracion/cambiar_password.html'
    form_class = CambiarPasswordForm
    success_url = reverse_lazy('administracion:index')
    login_url = 'users:administracion_login'
    success_message = "Contraseña modificada exitosamente"

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{'form':self.form_class})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(id=request.user.id).first()
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            logout(request)
            messages.success(request,'Contraseña cambiada exitosamente!')
            return redirect(self.success_url)
        else:
            form = self.form_class(request.POST)
            return render(request,self.template_name,{'form':form})
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        context['variants'] = Variant.objects.all().filter(stock__lte=3)
        return context
    

#----------------------------usuarios de la tienda -----------------------------   
def nuevo_cliente(request):
    template_name = "users/tienda/registro.html"
    
    #Con RegistroForm(request.POST or None) indicamos:
    #Si la peticion es por el metodo POST genere un formulario con los datos del cliente
    #Si la peticion no es por el metodo POST que genere un fomulario vacio
    form = RegistroForm(request.POST or None)
    tienda = Tienda.objects.get(id=1)

    #---------MUJERES------------------
    producto_mujeres = Product.objects.all().filter(genero="MUJER")
    categoria_mujeres = []
    for pm in producto_mujeres:
        if pm not in categoria_mujeres:
            categoria_mujeres.append(pm.categoria.nombre)
    categorias_mujeres = categoria_mujeres
    #-------HOMBRES-------------------
    producto_hombres = Product.objects.all().filter(genero="HOMBRE")
    categoria_hombres = []
    for ph in producto_hombres:
        if ph not in categoria_hombres:
            categoria_hombres.append(ph.categoria.nombre)
    categorias_hombres = categoria_hombres
    #--------Unisex------------------
    producto_unisex = Product.objects.all().filter(genero="UNISEX")
    categoria_unisex = []
    for pu in producto_unisex:
        if pu not in categoria_unisex:
            categoria_unisex.append(pu.categoria.nombre)
    categorias_unisex= categoria_unisex
    #------------------------------------------
    if request.method == "POST" and form.is_valid():

        user = form.save(commit=False)
            #delegamos la responsabilidad de crear nuevos usuarios a nuestro formulario
       
        user.set_password(form.cleaned_data['password'])
        user.save()

        if user:
            login(request,user)
            messages.success(request,'Usuario creado exitosamente')
            return redirect('tienda:index')

    return render(request,template_name,{
        'form':form,
        'tienda':tienda,
        "categorias_mujeres":categorias_mujeres,
        "categorias_hombres":categorias_hombres,
        "categorias_unisex":categorias_unisex 
    })

def tienda_logout(request):
    logout(request)
    messages.success(request,'Sesión cerrada exitosamente!')
    return redirect('tienda:index')

def tienda_login(request):
    template_name = 'users/tienda/login.html'
    tienda = Tienda.objects.get(id=1)

    #---------MUJERES------------------
    producto_mujeres = Product.objects.all().filter(genero="MUJER")
    categoria_mujeres = []
    for pm in producto_mujeres:
        if pm not in categoria_mujeres:
            categoria_mujeres.append(pm.categoria.nombre)
    categorias_mujeres = categoria_mujeres
    #-------HOMBRES-------------------
    producto_hombres = Product.objects.all().filter(genero="HOMBRE")
    categoria_hombres = []
    for ph in producto_hombres:
        if ph not in categoria_hombres:
            categoria_hombres.append(ph.categoria.nombre)
    categorias_hombres = categoria_hombres
    #--------Unisex------------------
    producto_unisex = Product.objects.all().filter(genero="UNISEX")
    categoria_unisex = []
    for pu in producto_unisex:
        if pu not in categoria_unisex:
            categoria_unisex.append(pu.categoria.nombre)
    categorias_unisex= categoria_unisex
    #------------------------------------------
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user=authenticate(username=username,password=password)
        print(user)
        if user:
            login(request,user)
            messages.success(request,'Bienvenido {}'.format(user.username))
            return redirect('tienda:index')
        else:
            messages.error(request,'Usuario o contraseña no validos!')
    return render(request,template_name,{
        "tienda":tienda,
        "categorias_mujeres":categorias_mujeres,
        "categorias_hombres":categorias_hombres,
        "categorias_unisex":categorias_unisex 

        })