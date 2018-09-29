import requests

from rent_montdore.settings import MAILGUN_PV_KEY

domain = "sandbox08f38220d335463c8069ec565b51ced0.mailgun.org"

def send_email(message):
    global domain
    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(domain),
        auth=("api", MAILGUN_PV_KEY),
        data={"from": "Excited User <mailgun@{}>".format(domain),
              "to": ["nathansava@hotmail.fr"],
              "subject": "Hello",
              "text": message})
