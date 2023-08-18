from smtplib import SMTPRecipientsRefused

from django.core.mail import send_mail

from link.exceptions.account import EmailVerificationException
from link.settings import EMAIL_HOST_USER


def send_email_user(subject, email_plaintext_message, user_email):
    try:
        send_mail(
            subject,
            email_plaintext_message,
            EMAIL_HOST_USER,
            [user_email],
        )
    except SMTPRecipientsRefused:
        raise EmailVerificationException