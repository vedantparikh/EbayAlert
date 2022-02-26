from uuid import UUID

from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    """ Base ViewSet for all ViewSets. """

    serializer_class = None
    permission_classes = ()
    model = None
    lookup_field = 'uuid'

    def __init_subclass__(cls, **kwargs):
        assert cls.model is not None

    @property
    def lookup_id(self) -> UUID:
        """ Get id from url. """

        return UUID(self.kwargs.get(self.lookup_field))
