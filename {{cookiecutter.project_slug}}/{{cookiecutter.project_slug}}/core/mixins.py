# coding: utf8

from rest_framework import (mixins, status)
from rest_framework.response import Response


class BaseModelMixin(object):
    def get_response_data(self, data, *args, **kwargs):
        """
            Get the data to return as response data
            By default it returns `serializer.data`
            Override this method to return custom response data
        """
        return data


class CreateModelMixin(BaseModelMixin, mixins.CreateModelMixin):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = self.get_response_data(serializer.data)
        return Response(
            response_data, status=status.HTTP_201_CREATED)


class UpdateModelMixin(BaseModelMixin, mixins.UpdateModelMixin):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response_data = self.get_response_data(serializer.data)
        return Response(response_data)
