from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from alert.models import Product
from alert.serializers import (
    ProductSerializer,
    ProductQuerySerializer,
    ProductUpdateSerializer,
)
from alert.serializers.base import ErrorResponseSerializer
from alert.views.base import BaseViewSet


class ProductViewSet(BaseViewSet):
    serializer_class = ProductSerializer
    model = Product

    def _parse_serializer_query(self, query) -> Tuple:
        return query.get('subscription_id'), query.get('name')

    def _filter_products(self, query) -> QuerySet:
        subscription_id, name = self._parse_serializer_query(query)

        products = self.model.objects.all()
        if subscription_id:
            products = products.filter(subscription=subscription_id)

        if name:
            products = products.filter_by_name(name)

        return products

    @swagger_auto_schema(
        query_serializer=ProductQuerySerializer(),
        responses={
            status.HTTP_200_OK: ProductSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        query_serializer = ProductQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        products = self._filter_products(query_serializer.data)
        serializer = self.serializer_class(products, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: ProductSerializer(),
        status.HTTP_404_NOT_FOUND: 'Product not found.',
    })
    def retrieve(self, request, *args, **kwargs):
        id_ = self.kwargs['uuid']

        try:
            queryset = self.model.objects.get(id=id_)
            serializer = self.serializer_class(queryset)
        except ObjectDoesNotExist as err:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'retrieve_failed',
                    'title': 'Product not found.',
                    'details': f'{str(err)}'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer(),
        responses={
            status.HTTP_201_CREATED: ProductSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Product not created.',
        })
    def create(self, request, *args, **kwargs):

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ProductUpdateSerializer(),
        responses={
            status.HTTP_200_OK: ProductSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Product is not updated.',
        })
    def update(self, request, *args, **kwargs):
        update_serializer = ProductUpdateSerializer(data=request.data)
        update_serializer.is_valid(raise_exception=True)

        data = update_serializer.data
        product_id = data.get('product_id')
        name = data.get('name')
        price = data.get('price')

        try:
            instance = Product.objects.get(id=self.kwargs['uuid'])
        except ObjectDoesNotExist as err:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'update_failed',
                    'title': 'Product not found.',
                    'details': f'{str(err)}'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        if product_id:
            instance.product_id = product_id
        if name:
            instance.name = name
        if price:
            instance.price = price

        instance.save()
        serializer = self.serializer_class(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: ProductSerializer(),
        status.HTTP_400_BAD_REQUEST: 'Product deletion failed.',
    })
    def destroy(self, request, *args, **kwargs):
        try:
            instance = Product.objects.get(id=self.kwargs['uuid'])
            instance.delete()
        except ObjectDoesNotExist as err:
            serializer = ErrorResponseSerializer({
                'error': {
                    'code': 'delete_failed',
                    'title': 'Product not found.',
                    'details': f'{str(err)}'
                }
            })
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
