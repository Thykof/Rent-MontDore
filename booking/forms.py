import datetime

from django import forms

from booking.data import MONTHS

class BookingForm(forms.Form):
    last_name = forms.CharField(label='Votre nom', max_length=42, error_messages={'required': 'Entrer votre Nom.'})
    first_name = forms.CharField(label='Votre prénom', max_length=42, error_messages={'required': 'Entrer votre prénom.'})

    date_widget = forms.SelectDateWidget(months=MONTHS)
    coming_date = forms.DateField(label="Date d'arrivée ", widget=date_widget, help_text='Date de début du séjour')
    leaving_date = forms.DateField(label='Date de départ ', widget=date_widget, help_text='Date de fin du séjour')

    email_address = forms.EmailField(label='Votre adresse e-mail', error_messages={'required': 'Entrer votre adresse mail.', 'invalid':'Entrer une adresse mail valide.'})
    therapy = forms.BooleanField(label='Allez-vous en cure ?', required=False)

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        coming_date = cleaned_data.get('coming_date')
        leaving_date = cleaned_data.get('leaving_date')
        email_address = cleaned_data.get('email_address')

        if coming_date and leaving_date:  # coming_date and leaving_date are valid
            if coming_date <= datetime.date.today():
                msg = 'Date invalide'
                self.add_error('coming_date', msg)
            elif not coming_date < leaving_date:
                msg = 'Date invalide'
                self.add_error("leaving_date", msg)

        if email_address == '':
            self.add_error('email_address', 'Entrer votre adresse e-mail')

        return cleaned_data
