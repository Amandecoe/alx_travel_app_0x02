from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ExampleSerializer
from rest_framework import viewsets, status
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
from django.conf import settings
import uuid

CHAPA_URL = "https://api.chapa.co/v1/transaction/initialize"
class listingViewSet(viewsets.ModelViewset):
  queryset = Listing.Objects.all()
  serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewset):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer

class PaymentViewSet(viewsets.ModelViewset):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer

class InitiatePaymentView(APIView):
  def post(self, request):
    booking_id = request.data.get("booking_id")
    amount = request.data.get("amount")
    try:
      booking = Booking.objects.get(id = booking_id)
    except Booking.DoesNotExist:
      return Response({"error": "Booking not found"}, status = status.HTTP_404_NOT_FOUND) 

    tx_ref = str(uuid.uuid4()) #unique transaction reference  

    payload = {
      "amount":amount,
      "currency": "ETB",
      "email": booking.owner.email,
      "first_name": booking.owner.first_name,
      "last_name" : booking.owner.last_name,
      "tx_ref": tx_ref
}
    headers = {
      "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
      "Content-Type" : "application/json",
    }

    #call chapa api
    response = request.post(CHAPA_URL, json=payload, headers = headers)

    if response.get("status") == "success":
      #save payment as pending
      Payment.objects.create(
        booking=booking,
        amount = amount,
        tx_ref = tx_ref,
        chapa_txn_id = response["data"]["checkout_url"], #chapa checkout url
        status= Payment.payment_status.PENDING
      )
      return Response(
        {"checkout_url":response["data"]["checkout_url"], "tx_ref":tx_ref}, status=status.HTTP_200_OK
      )
    else:
      return Response(response, status = status.HTTP_400_BAD_REQUEST)