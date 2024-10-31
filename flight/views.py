from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
import math
from .models import *
from capstone.utils import render_to_pdf, createticket


# Fee and Surcharge variable
from .constant import FEE
from .utils import (
    createWeekDays,
    addPlaces,
    addDomesticFlights,
    addInternationalFlights,
)

try:
    if len(Week.objects.all()) == 0:
        createWeekDays()

    if len(Place.objects.all()) == 0:
        addPlaces()

    if len(Bus.objects.all()) == 0:
        print("Do you want to add flights in the Database? (y/n)")
        if input().lower() in ["y", "yes"]:
            addDomesticFlights()
            addInternationalFlights()
except:
    pass

# Create your views here.


def index(request):
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == "POST":
        origin = request.POST.get("Origin")
        destination = request.POST.get("Destination")
        depart_date = request.POST.get("DepartDate")
        seat = request.POST.get("SeatClass")
        return render(
            request,
            "flight/index.html",
            {
                "origin": origin,
                "destination": destination,
                "depart_date": depart_date,
                "seat": seat.lower(),
            },
        )
    else:
        return render(
            request, "flight/index.html", {"min_date": min_date, "max_date": max_date}
        )


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(
                request,
                "flight/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "flight/login.html")


def register_view(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensuring password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "flight/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(
                request, "flight/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flight/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def query(request, q):
    places = Place.objects.all()
    filters = []
    q = q.lower()
    for place in places:
        if (
            (q in place.city.lower())
            or (q in place.airport.lower())
            or (q in place.code.lower())
            or (q in place.country.lower())
        ):
            filters.append(place)
    return JsonResponse(
        [
            {"code": place.code, "city": place.city, "country": place.country}
            for place in filters
        ],
        safe=False,
    )


@csrf_exempt
def flight(request):
    o_place = request.GET.get("Origin")
    d_place = request.GET.get("Destination")
    departdate = request.GET.get("DepartDate")
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    seat_class = request.GET.get("SeatClass")

    destination = Place.objects.get(code=d_place.upper())
    origin = Place.objects.get(code=o_place.upper())

    bus = Bus.objects.filter(origin=origin, destination=destination).first()

    return render(
        request,
        "flight/search.html",
        {
            "busID": bus.id,
            "origin": origin,
            "seatClass": seat_class.capitalize(),
            "depart_date": depart_date,
        },
    )


def review(request):
    busID = request.GET.get("busID")
    date1 = request.GET.get("date")
    seat_class = request.GET.get("seatClass")
    selected_seats = request.GET.get("selectedSeats")
    passenger_count = request.GET.get("selectedSeatsCount")

    if request.user.is_authenticated:
        bus = Bus.objects.get(id=busID)
        bus_date = datetime(
            int(date1.split("-")[2]),
            int(date1.split("-")[1]),
            int(date1.split("-")[0]),
            bus.depart_time.hour,
            bus.depart_time.minute,
        )

        return render(
            request,
            "flight/book.html",
            {
                "bus": bus,
                "busDate": bus_date,
                "seatClass": seat_class,
                "selectedSeats": selected_seats,
                "passengerCount": passenger_count,
                "fee": FEE,
            },
        )
    else:
        return HttpResponseRedirect(reverse("login"))


def book(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            bus_id = request.POST.get("busID")
            bus_date = request.POST.get("date")
            seat_class = request.POST.get("seatClass")
            passenger_count = request.POST.get("passengerCount")
            selected_seats = request.POST.get("selectedSeats")

            selected_seats_list = selected_seats.split("-")

            seats = []

            mobile = request.POST["mobile"]
            email = request.POST["email"]

            bus = Bus.objects.get(id=bus_id)

            coupon = request.POST.get("coupon")

            try:
                for seat_code in selected_seats_list:
                    seat = Seat.objects.create()
                    seat.bus_id = bus
                    seat.seat_code = seat_code
                    seat.save()
                    seats.append(seat)

                ticket = createticket(
                    request.user,
                    int(passenger_count),
                    bus,
                    seats,
                    bus_date,
                    seat_class,
                    mobile,
                    email,
                    coupon,
                )
            except Exception as e:
                print(e)
                return HttpResponse(e)

            return render(
                request,
                "flight/payment.html",
                {"fare": ticket.total_fare, "ticket": ticket.id},
            )
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")


def payment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            ticket_id = request.POST["ticket"]
            t2 = False
            if request.POST.get("ticket2"):
                ticket2_id = request.POST["ticket2"]
                t2 = True
            fare = request.POST.get("fare")
            card_number = request.POST["cardNumber"]
            card_holder_name = request.POST["cardHolderName"]
            exp_month = request.POST["expMonth"]
            exp_year = request.POST["expYear"]
            cvv = request.POST["cvv"]

            try:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.status = "CONFIRMED"
                ticket.booking_date = datetime.now()
                ticket.save()
                if t2:
                    ticket2 = Ticket.objects.get(id=ticket2_id)
                    ticket2.status = "CONFIRMED"
                    ticket2.save()
                    return render(
                        request,
                        "flight/payment_process.html",
                        {"ticket1": ticket, "ticket2": ticket2},
                    )
                return render(
                    request,
                    "flight/payment_process.html",
                    {"ticket1": ticket, "ticket2": ""},
                )
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse("login"))


def ticket_data(request, ref):
    ticket = Ticket.objects.get(ref_no=ref)
    return JsonResponse(
        {
            "ref": ticket.ref_no,
            "from": ticket.flight.origin.code,
            "to": ticket.flight.destination.code,
            "flight_date": ticket.flight_ddate,
            "status": ticket.status,
        }
    )


@csrf_exempt
def get_ticket(request):
    ref = request.GET.get("ref")
    ticket1 = Ticket.objects.get(ref_no=ref)
    data = {"ticket1": ticket1, "current_year": datetime.now().year}
    pdf = render_to_pdf("flight/ticket.html", data)
    return HttpResponse(pdf, content_type="application/pdf")


def bookings(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user).order_by("-booking_date")
        return render(
            request, "flight/bookings.html", {"page": "bookings", "tickets": tickets}
        )
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def cancel_ticket(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            ref = request.POST["ref"]
            try:
                ticket = Ticket.objects.get(ref_no=ref)
                if ticket.user == request.user:
                    ticket.status = "CANCELLED"
                    ticket.save()
                    return JsonResponse({"success": True})
                else:
                    return JsonResponse(
                        {"success": False, "error": "User unauthorised"}
                    )
            except Exception as e:
                return JsonResponse({"success": False, "error": e})
        else:
            return HttpResponse("User unauthorised")
    else:
        return HttpResponse("Method must be POST.")


def resume_booking(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            ref = request.POST["ref"]
            ticket = Ticket.objects.get(ref_no=ref)
            if ticket.user == request.user:
                return render(
                    request,
                    "flight/payment.html",
                    {"fare": ticket.total_fare, "ticket": ticket.id},
                )
            else:
                return HttpResponse("User unauthorised")
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")


def contact(request):
    return render(request, "flight/contact.html")


def privacy_policy(request):
    return render(request, "flight/privacy-policy.html")


def terms_and_conditions(request):
    return render(request, "flight/terms.html")


def about_us(request):
    return render(request, "flight/about.html")
