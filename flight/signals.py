# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bus, Seat


@receiver(post_save, sender=Bus)
def create_seats_for_bus(sender, instance, created, **kwargs):
    if created:
        # Define seat layouts for different classes
        seat_layouts = {
            "ECONOMY": [
                "A1",
                "A2",
                "A3",
                "A4",
                "B1",
                "B2",
                "B3",
                "B4",
                "C1",
                "C2",
                "C3",
                "C4",
                "D1",
                "D2",
                "D3",
                "D4",
                "E1",
                "E2",
                "E3",
                "E4",
                "F1",
                "F2",
                "F3",
                "F4",
                "G1",
                "G2",
                "G3",
                "G4",
                "H1",
                "H2",
                "H3",
                "H4",
                "I1",
                "I2",
                "I3",
                "I4",
                "J1",
                "J2",
                "J3",
                "J4",
                "K1",
                "K2",
                "K3",
                "K4",
                "K5",
            ],
            "FIRST": [
                "A1",
                "A2",
                "B1",
                "B2",
                "C1",
                "C2",
                "D1",
                "D2",
                "E1",
                "E2",
                "F1",
                "F2",
                "G1",
                "G2",
                "H1",
                "H2",
            ],
            "SLEEPER": [
                "A1",
                "A2",
                "A3",
                "B1",
                "B2",
                "B3",
                "C1",
                "C2",
                "C3",
                "D1",
                "D2",
                "D3",
                "E1",
                "E2",
                "E3",
                "F1",
                "F2",
                "F3",
            ],
        }

        # Get the layout based on seat_class
        seat_codes = seat_layouts.get(instance.seat_class, [])

        # Create seats for the bus
        for seat_code in seat_codes:
            Seat.objects.create(bus_id=instance, seat_code=seat_code)
