from django.apps import AppConfig


class FlightConfig(AppConfig):
    name = "flight"

    def ready(self):
        import flight.signals
