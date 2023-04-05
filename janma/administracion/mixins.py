from django.shortcuts import redirect

class SuperUsuarioMixin(object):
    def dispath(self,request,*args,**kwargs):
        if request.user.is_superuser:
            return super().dispatch(request,*args,**kwargs)
        return redirect('administracion:index')

