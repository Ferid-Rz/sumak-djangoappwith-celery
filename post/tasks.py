from celery import shared_task 
from django.core.mail import send_mail
from time import sleep
import requests

# @shared_task
# def send_email_task():
#     sleep(10)
#     send_mail('Celery Task Worked!',
#     'This is proof the task worked!',
#     'support@prettyprinted.com',
#     ['ferid_7003@mail.ru'])

#     return None

@shared_task
def send_email_task(to, text):
    return requests.post(
            "https://api.mailgun.net/v3/sandbox65d4b5421cfb40c888c9cddcdf78371a.mailgun.org/messages",
            auth=("api", "2691bdf9b432a2c07b5b89cca961e981-2dfb0afe-9631f2b4"),
            data={
                "from": "Hi from <mailgun@sandbox65d4b5421cfb40c888c9cddcdf78371a.mailgun.org>",
                "to": [to],
                "subject": "Kategoriaya yeni koment elave olundu",
                "text": f"Kategoriyaniza yazilan koment - {text}"})