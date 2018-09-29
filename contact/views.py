from django.shortcuts import render

from contact.forms import ContactForm
from contact.models import Message
from rent_montdore.email import send_email


# Create your views here.

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            new_message = Message(
                name = form.cleaned_data['name'],
                subject = form.cleaned_data['subject'],
                email_address = form.cleaned_data['email_address'],
                message = form.cleaned_data['message']
            )
            new_message.save()
            # Send email
            text = "Message from {} | {}\n".format(form.cleaned_data['name'], form.cleaned_data['email_address'])
            text += "Subject: " + form.cleaned_data['subject'] + '\n'
            text += "Text: " + form.cleaned_data['message']
            send_email(text, "New message")
            msg = 'Votre message a bien été envoyé, nous vous réponderons dans les plus bref delais.'

    else:
        form = ContactForm()
        msg = "Vous pouvez aussi remplir ce formulaire :"

    return render(request, 'contact/contact.html', locals())
