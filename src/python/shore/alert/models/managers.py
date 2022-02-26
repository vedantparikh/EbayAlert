from django.db import models

from alert.models.querysets import SoftDeleteQuerySet


class DefaultSoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """ Default soft delete manager for all objects. By default is using SoftDeleteQuerySet. """
    pass


class DeletedSoftDeleteManager(DefaultSoftDeleteManager):
    """ Manager for all deleted objects. """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class NotDeletedSoftDeleteManager(DefaultSoftDeleteManager):
    """ Manager for all not deleted objects. """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModelMixin(models.Model):
    """ Base model for soft delete. """

    is_deleted = models.BooleanField(default=False)

    objects = NotDeletedSoftDeleteManager()
    all_objects = DefaultSoftDeleteManager()
    deleted_objects = DeletedSoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwds):
        """ Don't actually delete but just switch this flag. """

        self.is_deleted = True
        self.save(update_fields={'is_deleted'})
