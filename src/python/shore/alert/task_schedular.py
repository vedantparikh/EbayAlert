import json
from datetime import datetime

from django_celery_beat.models import (
    PeriodicTask,
    IntervalSchedule,
)

from alert.views.utils import UUIDEncoder


class TaskSchedular:
    def __init__(self, subscription_id, user_id):
        self.subscription_id = subscription_id
        self.user_id = user_id
        self.basename = f'{str(subscription_id)}_{str(user_id)}'

    def schedule_subscription(
            self, frequency: int, task_name: str, start_time: datetime = datetime.utcnow(), args=None, kwargs=None
    ) -> None:
        """ Creates a Scheduled Tasks for subscription. """

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=frequency, period=IntervalSchedule.MINUTES
        )
        subscription_name = self.basename + '_subscription'

        subscription_task = PeriodicTask(
            interval=schedule, name=subscription_name, task=task_name, start_time=start_time,
        )
        if args:
            subscription_task.args = json.dumps(args, cls=UUIDEncoder)
        if kwargs:
            subscription_task.kwargs = json.dumps(kwargs, cls=UUIDEncoder)

        subscription_task.save()

    def schedule_price_update(
            self, task_name: str, days: int = 2, start_time: datetime = datetime.utcnow(), args=None, kwargs=None
    ) -> None:
        """ Creates a Scheduled Tasks for price update. """

        schedule, created = IntervalSchedule.objects.get_or_create(every=days, period=IntervalSchedule.DAYS)

        price_decrease_change_name = self.basename + '_price_decrease_or_no_change'
        price_decrease_change_task = PeriodicTask(
            interval=schedule, name=price_decrease_change_name, task=task_name,
            start_time=start_time
        )
        if args:
            price_decrease_change_task.args = json.dumps(args, cls=UUIDEncoder)
        if kwargs:
            price_decrease_change_task.kwargs = json.dumps(kwargs, cls=UUIDEncoder)

        price_decrease_change_task.save()
