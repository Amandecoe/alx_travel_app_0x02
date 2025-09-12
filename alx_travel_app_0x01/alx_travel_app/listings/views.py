from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ExampleSerializer
from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

class listingViewSet(viewsets.ModelViewset):
  queryset = Listing.Objects.all()
  serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewset):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer