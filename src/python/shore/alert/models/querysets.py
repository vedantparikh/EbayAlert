from django.db.models import QuerySet


class SoftDeleteQuerySet(QuerySet):
    """ Queryset for soft deleting. """

    def delete(self, *args, **kwds):
        """ Don't actually delete but just switch this flag. """

        self.update(is_deleted=True)
