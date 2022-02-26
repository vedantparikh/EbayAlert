from typing import Optional
import json
from uuid import UUID

from django_celery_beat.models import PeriodicTask

from alert import get_task_schedular
from alert.models.subscription import Frequency


def get_frequency(frequency_text: str) -> Optional[int]:
    frequencies = Frequency.choices
    for frequency in frequencies:
        if frequency[1] == frequency_text:
            return frequency[0]


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def create_task(data: dict):
    """ Creates Schedular Tasks. """

    subscription_id = data['id']
    user_id = data['user']
    frequency = get_frequency(data['frequency'])
    search_phrase = data['search_phrase']

    schedular = get_task_schedular()
    task_schedular = schedular(subscription_id=subscription_id, user_id=user_id)

    task_schedular.schedule_subscription(frequency=frequency, task_name='alert.tasks.subscription_mail',
                                         args=(subscription_id, user_id, search_phrase,))
    task_schedular.schedule_price_update(task_name='alert.tasks.price_update_mail',
                                         args=(subscription_id, user_id, search_phrase,))
    return task_schedular


def delete_periodic_task(subscription_id=None, user_id=None) -> None:
    basename = ''
    if subscription_id:
        basename = f'{str(subscription_id)}_'
    if user_id:
        basename = basename + f'{str(user_id)}'
    if basename:
        PeriodicTask.objects.filter(name__icontains=basename).delete()
