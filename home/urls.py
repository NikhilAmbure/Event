from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'private/event', PrivateEventViewSet, basename="private-event")
router.register(r'public/event', PublicEventViewSet, basename="public-event")
router.register(r'booking', BookViewSet, basename="booking")


urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('', include(router.urls))
]