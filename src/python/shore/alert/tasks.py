from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from json2html import json2html

from alert.models import Product
from alert.task_utils import (
    get_decrease_price_products,
    get_matching_and_distinct_product,
    get_new_products,
    get_response,
    NEW_PRODUCT,
    NO_PRICE_CHANGE,
    NO_PRICE_CHANGE_MESSAGE,
    PRICE_DECREASE,
)

User = get_user_model()


@shared_task(bind=True)
def subscription_mail(self, subscription_id, user_id, search_phrase):
    user = User.objects.get(id=user_id)
    response_data = get_response(search_phrase)
    data = [{
        'name': d['name'],
        'height': d['height'],
    } for d in response_data]

    mail_subject = 'Ebay Subscription Alert'
    message = json2html.convert(json=data)
    # for email in users:
    to_email = user.email
    send_mail(
        subject=mail_subject,
        message='test message see attachment.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
        html_message=message,
    )

    print(f'Sent Subscription mail to {user.email}.')


@shared_task(bind=True)
def price_update_mail(self, subscription_id, user_id, search_phrase):
    user = User.objects.get(id=user_id)
    to_email = user.email
    products = Product.objects.filter(subscription=subscription_id)

    response_data = get_response(search_phrase)
    new_product_ids, common_products = get_matching_and_distinct_product(products, response_data)
    decreased_products = get_decrease_price_products(products, common_products, response_data)
    new_products = get_new_products(new_product_ids, response_data)

    if new_products:
        message = json2html.convert(json=new_products)
        send_mail(
            subject=NEW_PRODUCT,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
            html_message=message,
        )
        print(f'Sent New Product mail to {to_email}.')
    if decreased_products:
        message = json2html.convert(json=decreased_products)
        send_mail(
            subject=PRICE_DECREASE,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
            html_message=message,
        )
        print(f'Sent Reduced Price Product mail to {to_email}.')
    else:
        send_mail(
            subject=NO_PRICE_CHANGE,
            message=NO_PRICE_CHANGE_MESSAGE,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
        print(f'Sent No Product Price mail to {to_email}.')
