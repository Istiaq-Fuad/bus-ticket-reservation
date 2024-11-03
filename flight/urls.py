from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("query/places/<str:q>", views.query, name="query"),
    path("bus", views.flight, name="flight"),
    path("review", views.review, name="review"),
    path("bus/ticket/book", views.book, name="book"),
    path("bus/ticket/payment", views.payment, name="payment"),
    path("bus/ticket/api/<str:ref>", views.ticket_data, name="ticketdata"),
    path("bus/ticket/print", views.get_ticket, name="getticket"),
    path("bus/bookings", views.bookings, name="bookings"),
    path("bus/ticket/cancel", views.cancel_ticket, name="cancelticket"),
    path("bus/ticket/resume", views.resume_booking, name="resumebooking"),
    path("apply-coupon/<str:coupon_code>", views.apply_coupon, name="applycoupon"),
]
