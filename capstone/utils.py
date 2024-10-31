from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from flight.models import *
import secrets
from datetime import datetime, timedelta
from xhtml2pdf import pisa

from flight.constant import FEE


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def createticket(
    user,
    passengers_count,
    bus,
    seats,
    bus_date,
    seat_class,
    mobile,
    email,
    coupon=None,
):
    print(seat_class)
    ticket = Ticket.objects.create()
    ticket.user = user
    ticket.ref_no = secrets.token_hex(3).upper()
    ticket.bus = bus
    ticket.bus_fare = bus.fare
    ticket.num_passenger = passengers_count
    ticket.seat_class = seat_class.upper()

    ticket.bus_date = datetime(
        int(bus_date.split("-")[2]),
        int(bus_date.split("-")[1]),
        int(bus_date.split("-")[0]),
    )

    for seat in seats:
        ticket.seats.add(seat)
        seat.is_available = False
        seat.save()

    ticket.other_charges = FEE
    if coupon:
        ticket.coupon_used = coupon  ##########Coupon

    ticket.total_fare = bus.fare + FEE + 0.0  ##########Total(Including coupon)
    ticket.status = "PENDING"
    ticket.mobile = mobile
    ticket.email = email
    ticket.save()
    return ticket
