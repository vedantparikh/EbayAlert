from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from alert.models import User
from alert.serializers import UserSerializer
from alert.serializers.base import ErrorResponseSerializer

from alert.views.base import BaseViewSet


class ProductViewSet(BaseViewSet):
    serializer_class = UserSerializer
    model = User

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: UserSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        users = self.model.objects.all()
        serializer = self.serializer_class(users, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: UserSerializer(),
        status.HTTP_404_NOT_FOUND: 'User not found.',
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
                    'title': 'User not found.',
                    'details': f'{str(err)}'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer(),
        responses={
            status.HTTP_201_CREATED: User(),
            status.HTTP_400_BAD_REQUEST: 'User not created.',
        })
    def create(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=UserSerializer(),
        responses={
            status.HTTP_200_OK: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: 'User not updated.',
        })
    def update(self, request, *args, **kwargs):

        instance = User.objects.get(id=self.kwargs['uuid'])
        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ObjectDoesNotExist as err:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'update_failed',
                    'title': 'User not found.',
                    'details': f'{str(err)}'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: UserSerializer(),
        status.HTTP_400_BAD_REQUEST: 'User deletion failed.',
    })
    def destroy(self, request, *args, **kwargs):
        try:
            instance = User.objects.get(id=self.kwargs['uuid'])
            instance.delete()
        except ObjectDoesNotExist as err:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'delete_failed',
                    'title': 'User not found.',
                    'details': f'{str(err)}'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
