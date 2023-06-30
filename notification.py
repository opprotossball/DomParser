import json
import random
import smtplib
import time
from email.message import EmailMessage
import ssl

with open("./settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)

with open(settings["emailPasswdPath"], "r") as f:
    passwd = f.read()


def send_to_all(offer_name, offer_description, street, link):
    subject, body = build_mail(offer_name, offer_description, street, link)
    sender = settings["sender"]
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, passwd)
        for client in settings["clients"]:
            time.sleep(0.3 * random.random())
            email = EmailMessage()
            email["From"] = sender
            email["To"] = client
            email["Subject"] = subject
            email.set_content(body)
            smtp.sendmail(sender, client, email.as_string())


def build_mail(offer_name, offer_description, street, link):
    subject = f"Ciekawa oferta - ulica {street}"
    body = "\n".join([offer_name, offer_description, link])
    return subject, body
