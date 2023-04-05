from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ProductoSerializer,ClienteSerializer,VariantSerializer
from productos.models import Product,Variant,Image
from users.models import Cliente

from django.db.models import Q

class ProductoList(APIView):
    def get(self,request):
        producto = Product.objects.all()
        data = ProductoSerializer(producto,many=True).data
        return Response(data)

class ProductoDetalle(APIView):
    def get(self,request, codigo):
        producto = get_object_or_404(Product,Q(id=codigo)|Q(codigo_barras=codigo))
        data = ProductoSerializer(producto).data
        return Response(data)

class VariantList(APIView):
    def get(self,request,codigo):
        variant = Variant.objects.all().filter(Q(product__id=codigo)|Q(product__codigo_barras=codigo))
        data = VariantSerializer(variant,many=True).data
        return Response(data)
    
class ClienteList(APIView):
    def get(self,request):
        obj = Cliente.objects.all()
        data = ClienteSerializer(obj,many=True).data
        return Response(data)