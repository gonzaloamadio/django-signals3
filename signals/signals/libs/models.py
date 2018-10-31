from django.conf import settings
from django.db import models
from django.urls import reverse

from . import global_request


class AuditedModel(models.Model):
    """
    CHECK IF THIS IS TRUE

    CAVEAT 1:
    If using a custom user model, add the following line to the top:
    from api.models.user_profile import User  # noqa: F401
    It's needed for get_model in settings.
    CAVEAT 2:
    All api calls that add or edit a line to your database should be Authenticated.
    If you're not doing that then you are ASKING for trouble.
    """
    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='%(class)s_create',
                                    null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='%(class)s_update',
                                    null=True, blank=True)

    class Meta:
        abstract = True
        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-create_at', '-update_at']

    def save(self, *args, **kwargs):
        """
        Store create_user if it's not assigned yet (first time the object is
        saved() and overwrite the update_user
        """
        current_user = global_request.get_current_user()
        if not self.create_by:
            self.create_by = current_user
        self.update_by = current_user

        return super(AuditedModel, self).save(*args, **kwargs)


class PersistentModelQuerySet(models.QuerySet):
    """Model implementing QuerySet for PersistentModel: allows soft-deletion"""
    def delete(self):
        self.update(deleted=True)

class PersistentModelManager(models.Manager):
    """Model implementing default manager for PersistenModel: filters 'deleted' elements"""
    def inactive(self):
        return self.model.objects.filter(deleted=True)

    def active(self):
        return self.model.objects.filter(deleted=False)

    def filter(self, *args, **kwargs):
        active_only = kwargs.pop('active_only', True)
        qs = super().filter(*args, **kwargs)
        if active_only:
            return qs.filter(deleted=False)
        return qs

    def all(self, *args, **kwargs):
        active_only = kwargs.pop('active_only', True)
        qs = super().all(*args, **kwargs)
        if active_only:
            return qs.filter(deleted=False)
        return qs

    def get_queryset(self, **kwargs):
        return PersistentModelQuerySet(self.model, using=self._db)

class PersistentModel(models.Model):
    """Abstract class allowing soft-deletion"""
    deleted = models.BooleanField(default=False)
    objects = PersistentModelManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = True
        self.save()

class CodeModel(models.Model):
    """
        Agregamos esta variable solo para mostrar algun codigo, que lo formamos
        con el id del objeto.
        Entonces por ejemplo si tenemos una lista de objetos, y necesitamos nombrarlos
        podemos usar esto.
        Por ejemplo, tenemos una clase class Alumno que extiende esta clase y sobre
        escribimos esta variable como _CODE_FORMAT = 'AL-{id:06d}', y al imprimir
        una lista de alumnos mostramos el code, veremos algo como
        AL-000001, AL-000002,  . . .
    """
    _CODE_FORMAT = 'code-{id:06d}'

    class Meta:
        abstract = True

    @property
    def code(self):
        # provided the pk exists
        return self._CODE_FORMAT.format(id=self.pk)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
