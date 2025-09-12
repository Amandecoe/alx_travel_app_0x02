from rest_framework import serializers
from .models import Booking, Listing
class BookingSerializer(serializers.ModelSerializer):
  class meta:
    model = Booking
    field = (
      'booking_id',
      'start_date',
      'end_date',
      'total_price',
    )


class ListingSerializer(serializers.ModelSerializer):
  class meta:
    model = Listing 
    field = (
      'owner',
      'title',
      'description',
      'price',
      'currency',
      'created_at',
      'is_active',
      'updated_at'
    )

    