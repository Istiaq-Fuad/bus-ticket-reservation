from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone
from django.db.models import UniqueConstraint


class User(AbstractUser):
    def __str__(self):
        return f"{self.id}: {self.username}"


class Place(models.Model):
    city = models.CharField(max_length=64)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Week(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} ({self.number})"


SEAT_CLASS = (
    ("ECONOMY", "Economy"),
    ("FIRST", "First"),
    ("SLEEPER", "Sleeper"),
)


class Bus(models.Model):
    origin = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="departures"
    )
    destination = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="arrivals"
    )
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    depart_day = models.ManyToManyField(Week, related_name="bus_of_the_day")
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    fare = models.FloatField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"


class Seat(models.Model):
    bus_id = models.ForeignKey(Bus, null=True, on_delete=models.CASCADE)
    seat_code = models.CharField(max_length=5)  # e.g., A1, B2, etc.
    is_available = models.BooleanField(default=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["bus_id", "seat_code"], name="unique_bus_seat_code"
            )
        ]

    def __str__(self):
        return f"{self.seat_code} on {self.bus_id}"


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    discount = models.FloatField()
    expiry = models.DateField()

    def __str__(self):
        return f"{self.code}: {self.discount}"


TICKET_STATUS = (
    ("PENDING", "Pending"),
    ("CONFIRMED", "Confirmed"),
    ("CANCELLED", "Cancelled"),
)


class Ticket(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings", blank=True, null=True
    )
    num_passenger = models.IntegerField(null=True)
    bus = models.ForeignKey(
        Bus, on_delete=models.CASCADE, related_name="buses", blank=True, null=True
    )
    ref_no = models.CharField(max_length=10, blank=True)
    seats = models.ManyToManyField(Seat, related_name="tickets")
    bus_date = models.DateTimeField(blank=True, null=True)
    bus_fare = models.FloatField(blank=True, null=True)
    other_charges = models.FloatField(blank=True, null=True)
    coupon_used = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="coupons", blank=True, null=True
    )
    total_fare = models.FloatField(blank=True, null=True)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=timezone.now)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)

    def __str__(self):
        return f"{self.id}: {self.status}"
