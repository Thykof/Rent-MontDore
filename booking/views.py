from datetime import date

from django.shortcuts import render, redirect

# Create your views here.

from .forms import BookingForm
from booking.data import MONTHS
from .models import Booking
from rent_montdore.email import send_email

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            coming_date = form.cleaned_data['coming_date']
            leaving_date = form.cleaned_data['leaving_date']
            email_address = form.cleaned_data['email_address']
            therapy = form.cleaned_data['therapy']

            free = True
            for booking in Booking.objects.all():
                if booking.coming_date <= coming_date <= booking.leaving_date:
                    free = False
                if booking.coming_date <= leaving_date <= booking.leaving_date:
                    free = False
                if coming_date <= booking.coming_date <= leaving_date:
                    free = False

            duplicate = False
            for booking in Booking.objects.filter(last_name=last_name, first_name=first_name):  # Same names
                if coming_date == booking.coming_date:
                    duplicate = True
                elif not booking.leaving_date < coming_date:
                    duplicate = True
                if email_address != booking.email_address:
                    pass  # Costumer change it email address

            if not free and not duplicate:
                msg = "L'appartement n'est pas libre, désolé."
            elif duplicate:
                msg = 'Vous avez déjà réserver pour ces dates.'
            else:
                new_booking = Booking(
                    last_name=last_name,
                    first_name=first_name,
                    coming_date=coming_date,
                    leaving_date=leaving_date,
                    email_address=email_address,
                    therapy=therapy
                )
                new_booking.save()
                # Send email
                text = "Booking by {} {} | {}\n".format(first_name, last_name, email_address)
                text += "Coming date: " + str(coming_date) + '\n'
                text += "Leaving date: " + str(leaving_date) + '\n'
                text += "Therapy: " + str(therapy)
                send_email(text)
                msg = 'Votre réservation a été prise en compte !'
        else:
            msg = 'Le formulaire est invalide.'
    else:
        form = BookingForm()
        msg = "Pour envoyer une demande de réservation, remplissez le formulaire :"

    return render(request, 'booking/booking.html', locals())

def calendar(request, current_year):
    months = list(MONTHS.values())
    current_year = int(current_year)
    year = dict()
    for day in range(1, 32):
        year[day] = list()
        for month_number, month_name in MONTHS.items():
            try:
                current_date = date(current_year, month_number, day)
            except ValueError:
                year[day].append("")
            else:
                selected_bookings = Booking.objects.filter(coming_date__lte=current_date).filter(leaving_date__gte=current_date)
                if len(selected_bookings) != 0:
                    year[day].append("reserved")
                else:
                    year[day].append("available")
    return render(request, 'booking/calendar.html', locals())
