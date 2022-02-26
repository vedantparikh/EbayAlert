from typing import (
    List,
    Tuple,
)
from decimal import (
    Decimal,
    getcontext,
)

import requests

from django.conf import settings
from django.db.models import QuerySet

from alert.models import (
    Product,
    Subscription,
)

result_limit = settings.RESULTS_LIMIT
url = settings.APP_URL

getcontext().prec = 2

NO_PRICE_CHANGE = 'Ebay No Price Change Alert'
NO_PRICE_CHANGE_MESSAGE = 'Your search results did not have price changes over the last 2 days' \
                          ', act now before prices change.'
PRICE_DECREASE = 'Ebay Price Decreased Alert'
NEW_PRODUCT = 'Ebay New Products Available Alert'


def get_response(search_phrase: str) -> List[dict]:
    """ Returns response data from the server. """
    parameter = {
        'district': search_phrase
    }
    with requests.Session() as http_session:
        response = http_session.get(url=url, params=parameter)
        if response.status_code < 300:
            data = response.json()
            response_data = data['data']

            return response_data[:result_limit] if len(response_data) > result_limit else response_data


def create_product(data: dict) -> None:
    """ Creates Products in Database. """
    search_phrase = data['search_phrase']
    response_data = get_response(search_phrase=search_phrase)
    subscription_id = data['id']
    subscription = Subscription.objects.get(id=subscription_id)

    products = [
        Product(
            product_id=d['id'],
            name=d.get('name', 'default'),
            price=d.get('height', 11),
            subscription=subscription,
        ) for d in response_data
    ]

    Product.objects.bulk_create(products)


def is_price_decrease(current_price, old_price, change: int = 2) -> bool:
    """ Returns the True if price more or equal to decreased by change. """
    diff = Decimal(100) * (Decimal(old_price) - Decimal(current_price)) / Decimal(old_price)
    if diff >= change:
        return True
    return False


def get_product_price_from_response(product_id, response_data) -> Decimal:
    """ Returns price. """
    for data in response_data:
        if data['id'] == product_id:
            return data['height']


def get_matching_and_distinct_product(products: QuerySet, response_data) -> Tuple:
    product_ids = set(products.values_list('product_id', flat=True))
    response_product_ids = set([data['id'] for data in response_data])

    new_product_ids = response_product_ids - product_ids
    common_products = product_ids & response_product_ids

    return new_product_ids, common_products


def get_decrease_price_products(products: QuerySet, common_products, response_data) -> list:
    """ Returns the products whose price is decreased. """
    product_price_list = []
    for product in products:
        if product.product_id in common_products:
            price = product.price
            latest_price = get_product_price_from_response(product_id=product.product_id, response_data=response_data)
            if is_price_decrease(latest_price, price):
                product_price_list.append({
                    product.name: latest_price
                })

    return product_price_list


def get_new_products(new_product_ids, response_data) -> list:
    """ Returns the new products. """
    new_product_list = []

    for data in response_data:
        if data['id'] in new_product_ids:
            new_product_list.append({
                data['name']: data['height']
            })

    return new_product_list
