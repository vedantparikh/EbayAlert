from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from alert.models import (
    Product,
    Subscription,
)
from alert.serializers import (
    SubscriptionSerializer,
    SubscriptionQuerySerializer,
    SubscriptionUpdateSerializer,
)
from alert.serializers.base import ErrorResponseSerializer
from alert.task_utils import create_product

from alert.views.base import BaseViewSet
from alert.views.utils import (
    create_task,
    delete_periodic_task,
    get_frequency,
)


class SubscriptionViewSet(BaseViewSet):
    serializer_class = SubscriptionSerializer
    model = Subscription

    @swagger_auto_schema(
        query_serializer=SubscriptionQuerySerializer(),
        responses={
            status.HTTP_200_OK: SubscriptionSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        query_serializer = SubscriptionQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        query = query_serializer.data
        search_phrase = query.get('search_phrase')
        if search_phrase:
            subscriptions = Subscription.objects.filter_by_search_phrase(search_phrase=search_phrase)
        else:
            subscriptions = Subscription.objects.all()

        serializer = self.serializer_class(subscriptions, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: SubscriptionSerializer(),
        status.HTTP_404_NOT_FOUND: 'Subscription not found.',
    })
    def retrieve(self, request, *args, **kwargs):
        id_ = self.kwargs['uuid']

        try:
            instance = self.model.objects.get(id=id_)
            serializer = self.serializer_class(instance)
        except ObjectDoesNotExist as err:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'retrieve_failed',
                    'title': 'Subscription not found.',
                    'details': f'{str(err)}'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=SubscriptionSerializer(),
        responses={
            status.HTTP_201_CREATED: SubscriptionSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Subscription not created.',
        })
    def create(self, request, *args, **kwargs):

        create_serializer = SubscriptionSerializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)

        data = create_serializer.data
        search_phrase = data.get('search_phrase')
        user = data.get('user')

        subscription_exists = Subscription.objects.subscription_exists(
            search_phrase=search_phrase, user=user
        )
        if subscription_exists:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'create_failed',
                    'title': 'Subscription Exists.',
                    'details': f'Subscription with '
                               f'search_phrase: {search_phrase} and user: {user} already exists.'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data
        create_product(data)
        create_task(data=data)

        return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=SubscriptionUpdateSerializer(),
        responses={
            status.HTTP_200_OK: SubscriptionSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Subscription not updated.',
        })
    def update(self, request, *args, **kwargs):

        update_serializer = SubscriptionUpdateSerializer(data=request.data)
        update_serializer.is_valid(raise_exception=True)

        data = update_serializer.data
        frequency = data.get('frequency')
        frequency_int = get_frequency(frequency) if frequency else None
        search_phrase = data.get('search_phrase')
        try:
            instance = Subscription.objects.get(id=self.kwargs['uuid'])
        except ObjectDoesNotExist as err:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'update_failed',
                    'title': 'Subscription not found.',
                    'details': f'{str(err)}'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        if frequency_int:
            instance.frequency = frequency_int
        if search_phrase:
            instance.search_phrase = search_phrase

        instance.save()
        # deleting previously created periodic task
        delete_periodic_task(subscription_id=instance.id, user_id=instance.user.pk)
        serializer = self.serializer_class(instance)
        data = serializer.data
        if search_phrase:
            # if subscription search phrase is changed then we need to unlink it from the products and
            # add new products in our database with the results of the new phrase.
            _ = Product.objects.filter(subscription=instance.pk).delete()
            create_product(data)

        # adding new periodic task
        create_task(data)

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: SubscriptionSerializer(),
        status.HTTP_400_BAD_REQUEST: 'Subscription deletion failed.',
    })
    def destroy(self, request, *args, **kwargs):
        try:
            instance = Subscription.objects.get(id=self.kwargs['uuid'])
        except ObjectDoesNotExist as err:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'delete_failed',
                    'title': 'Subscription not found.',
                    'details': f'{str(err)}'
                }
            })

            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        # deleting the periodic task along with it.
        delete_periodic_task(subscription_id=instance.id, user_id=instance.user)
        instance.delete()

        return Response(status=status.HTTP_200_OK)
