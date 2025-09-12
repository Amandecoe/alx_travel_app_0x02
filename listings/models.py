from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Booking(models.Model):
  booking_id = models.PositiveIntegerField(primary_key=True, unique = True)
  start_date = models.DateTimeField(auto_now_add=True)
  end_date = models.DateTimeField(null= False)
  total_price = models.PositiveIntegerField()
  class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    ADMIN = 'admin', 'Admin'

  status = models.CharField(max_length=10, choices = Status.choices, default = Status.PENDING )

class Review(models.Model):
  review_id = models.PositiveIntegerField(primary_key=True)
  rating = models.PositiveSmallIntegerField(null = False)
  comment = models.CharField(max_length= 200,null = False)   

class Listing(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
  title = models.CharField(max_length=255)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  currency = models.CharField(max_length=10, default="USD")
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
  transaction_id = models.BigAutoField(primary_key=True)
  class payment_status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'

  amount = models.PositiveIntegerField()
  booking = models.ForeignKey(Booking, on_delete = models.CASCADE, related_name="payments")
  tx_ref = models.CharField(max_length = 255, null = True, blank = True) #stores the unique transaction reference sent to chapa
  chapa_txn_id = models.CharField(max_length=255, null= True, blank = True) #stores the checkout URL or chapa transaction ID
  status = models.CharField(max_length = 10, choices = payment_status.choices, default = payment_status.PENDING)
  created_at = models.DateTimeField(auto_now_add=True)
 
