from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ExampleSerializer

class ExampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello from Listings API!"})
