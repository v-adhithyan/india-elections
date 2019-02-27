from django.contrib import messages
import requests

from .constants import GOOGLE_RECAPTCHA_VERIFY_URL, GOOGLE_RECAPTCHA_SITE_KEY


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def verify_recaptcha(request):
    recaptcha_response = request.POST['g-recaptcha-response']
    if not recaptcha_response:
        messages.error(request, "Complete reCAPTCHA to save your opinion.")
        return False

    data = {
        'secret': GOOGLE_RECAPTCHA_SITE_KEY,
        'response': recaptcha_response,
        'remoteip': get_ip_address(request)
    }
    response = requests.post(url=GOOGLE_RECAPTCHA_VERIFY_URL, data=data)
    if response.ok:
        return True

    messages.error(request, "Unable to contact Google to verify reCAPTCHA. Please try again later.")
    return False
