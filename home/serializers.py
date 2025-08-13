from rest_framework import serializers
from home.models import Event, Booking, Ticket
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = '__all__'



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class BookingSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Booking
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['event'] = EventSerializer(instance.ticket.event).data
        response['ticket'] = TicketSerializer(instance.ticket).data
        return response
    

class TicketSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Ticket
        fields = '__all__'

    

class TickerBookingSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    ticket_type = serializers.CharField()
    total_person = serializers.IntegerField()
    user = serializers.IntegerField()

    def validate_event(self, value):
        if not Event.objects.filter(id=value, status="Happening").exists():
            raise serializers.ValidationError("Event does not exist.")
        return value

    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value
    
    # creating tickets and booking
    def create(self, validated_data):
        print("=== DEBUG CREATE METHOD ===")
        print(f"validated_data: {validated_data}")
        
        event = Event.objects.get(id=validated_data['event'])
        user = User.objects.get(id=validated_data['user'])
        total_person = validated_data['total_person']
        ticket_type = validated_data['ticket_type']
        
        print(f"event: {event}")
        print(f"user: {user}")
        print(f"total_person: {total_person} (type: {type(total_person)})")
        print(f"ticket_type: {ticket_type}")
        
        # Check if total_person is None
        if total_person is None:
            print("❌ total_person is None!")
            raise serializers.ValidationError("total_person cannot be None")
        
        ticket = Ticket.objects.create(
            event=event,
            ticket_type=ticket_type,
            total_person=total_person
        )
        
        total_price = event.ticket_price * total_person
        booking = Booking.objects.create(
            ticket=ticket,
            user=user,
            status="Paid",
            total_price=total_price
        )
        
        return {
            "event": event.id,
            "user": user.id,
            "ticket_type": ticket_type,
            "total_person": total_person
        }
    
    
    def validate(self, data):
        event = Event.objects.get(id=data['event'])
        requested_persons = data['total_person']  # Use the input value
        
        # Check if booking exceeds reasonable limits
        if requested_persons > 30:
            raise serializers.ValidationError("You can only book maximum 30 tickets")
        
        # Check if event has enough capacity
        if requested_persons > event.capacity:
            raise serializers.ValidationError(f"Event capacity is {event.capacity}. You requested {requested_persons} tickets.")
        
        return data