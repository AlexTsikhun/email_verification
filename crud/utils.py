import environ
import requests
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_email_for_veiry(request, user):
    current_site = get_current_site(request)
    context = {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    message = render_to_string(
        'registration/verify_email.html',
        context=context,
    )
    email = EmailMessage(
        'Verify email',
        message,
        to=[user.email],
    )
    email.send()

def is_verify_email(email):
    env = environ.Env()
    HUNTER_API_KEY = env('HUNTER_API_KEY')
    url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}'
    response = requests.get(url)
    try:
        if response.status_code != 200:
            raise Exception(f'Unenspected status code {response.status_code}')
        if response.json()['data']['status'] != 'valid':
            raise Exception(f'Not valid! status: {response.json()["data"]["status"]}')
    except Exception:
        return False
    return True

