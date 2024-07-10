from django.core.mail import send_mail

from good_reads.celery import app


@app.task()
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        "davronbekatadjanov111@gmail.com",
        recipient_list
    )