from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
from django.conf import settings
import uuid

CHAPA_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/"

class listingViewSet(viewsets.ModelViewSet):
  queryset = Listing.objects.all()
  serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer

class PaymentViewSet(viewsets.ModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer

class InitiatePaymentView(APIView):
  def post(self, request):
    booking_id = request.data.get("booking_id")
    amount = request.data.get("amount")
    try:
      booking = Booking.objects.get(booking_id=1)
    except Booking.DoesNotExist:
      return Response({"error": "Booking not found"}, status = status.HTTP_404_NOT_FOUND) 

    tx_ref = str(uuid.uuid4()) #unique transaction reference  

    payload = {
      "amount":amount,
      "currency": "ETB",
      "email": booking.listing.owner.email,
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
    
class VerifyPaymentView(APIView):
  def post(self, request):
    tx_ref = request.data.get("tx_ref")
    try:
      payment = Payment.objects.get(tx_ref = tx_ref)    
    except Payment.DoesNotExist:
      return Response({"error": "Payment not found"}, status = status.HTTP_404_NOT_FOUND)  
    headers = {
      "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    #call chapa verify api
    response = request.get(f"{CHAPA_VERIFY_URL}{tx_ref}", headers = headers)
    if response.get("status") == "success":
      chapa_status = response["data"]["status"]

      #update payment status in our DB
      if chapa_status.lower() == "successful":
        payment.status = Payment.payment_status.CONFIRMED
      else:
        payment.status = Payment.PaymentStatus.PENDING

      payment.save()

      return Response({
        "tx_ref":tx_ref,
        "payment_status":payment.status,
        "chapa_status":chapa_status
      }, status=status.HTTP_200_OK)
    else:
      return Response({"error":response}, status = status.HTTP_400_BAD_REQUEST)    