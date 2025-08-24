from django.urls import path, include
from .views import listingViewSet, BookingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#an object for the default router class
router.register('listingviewset', listingViewSet, basename= 'listing')
router.register ('bookingviewset', BookingViewSet, basename= 'Booking')


urlpatterns = [
    path('api/', include(router.urls)),   # 👈 include router-generated routes
]