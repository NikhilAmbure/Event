from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    data = models.DateField()
    capacity = models.IntegerField()
    ticket_price = models.FloatField(default=100)
    status = models.CharField(max_length=100, choices=(('Upcoming', 'Upcoming'), ('Cancelled', 'Cancelled'), ('Happening', 'Happening')), default="Upcoming")
    image = models.ImageField(upload_to='event_images', blank=True, null=True)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=255, choices=(('VIP', 'VIP'), ('Regular', 'Regular')))
    total_person = models.IntegerField(default=1)

class Booking(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='Pending')
    total_price = models.FloatField()
