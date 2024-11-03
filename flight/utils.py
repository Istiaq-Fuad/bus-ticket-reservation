from datetime import timedelta, datetime
from .models import *
from .models import Week, Place, Bus


def get_number_of_lines(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def createWeekDays():
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    for i, day in enumerate(days):
        Week.objects.create(number=i, name=day)
