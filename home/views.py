from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from home.serializers import EventSerializer, Event, RegisterSerializer, LoginSerializer, Booking, BookingSerializer, TickerBookingSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .permission import IsAdminUser
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from django.db.models import Q


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Account created",
                "data": {}
            })
        
        return Response({
                "status": False,
                "message": "Account not created.",
                "data": serializer.errors
        })       


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            user = authenticate(
                username = serializer.validated_data['username'],
                password = serializer.validated_data['password']
            )

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                "status": True,
                "message": "Login successful",
                "data": {"token": token.key}
            })
            else:
                return Response({
                "status": False,
                "message": "Invalid Credentials",
                "data": {}
            })
        
    
        return Response({
                "status": False,
                "message": "Login failed",
                "data": serializer.errors
            })


class PublicEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # Method : 1 (To disable the other methods)
    # Disabling other methods (Only get will work)
    http_method_names = ['get']
    # OR
    # Method : 2
    # You can't create events (Only admin can)
    # Disable the method ->
    # def create(self, request, *args, **kwargs):
        # raise MethodNotAllowed('POST')


    # ?search=...
    @action(detail=False, methods=['GET'])
    def search_events(self, request):
        search = request.GET.get('search')
        event = Event.objects.all()
        if search:
            event = event.filter(Q(title__icontains=search) | Q(description__icontains=search))
        serializer = EventSerializer(event, many=True)

        return Response({
            "status": True,
            "message": "Events fetched",
            "data": serializer.data
        })
    


# Here, we can create, update, delete the events
# IsAuthenticated -> All the authenticated users can create the event but we want only admin can create the events.
# -> so, to do that we have to modify the "IsAuthenticated" permission class (permission.py) 
class PrivateEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [TokenAuthentication]

    # permission_classes = [IsAuthenticated]
    # Instead of above -> we will use the modified IsAuthenticated
    permission_classes = [IsAdminUser]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def get_bookings(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response({
            "status": True,
            "message": "Booking fetched",
            "data": serializer.data
        })
    

    @action(detail=False, methods=['POST'])
    def create_booking(self, request):
        data = request.data
        serializer = TickerBookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Booking created",
                "data": serializer.data
            })

        return Response({
            "status": False,
            "message": "Booking not created",
            "data": serializer.errors
        })