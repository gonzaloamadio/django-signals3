from email.utils import formataddr
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from signals.libs.models import AuditedModel, PersistentModel

class CompanyModel(AuditedModel):
    """
        Abstract model with basic info of a company
    """
    name = models.CharField(max_length=64, db_index=True, verbose_name='Name', null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def full_name(self):
        if self.name:
            return self.name
        return ""

    def __str__(self):
        return self.full_name

    def clean(self):
        # Strip whitespaces
        fields = ['name']
        for field in fields:
            value = getattr(self, field, None)
            if value:
                setattr(self, field, value.strip())

class PersonModel(AuditedModel):
    """
        Abstract model with basic info of a person type user
    """
    # Basic info, location
    name = models.CharField(max_length=64, db_index=True, verbose_name='Name', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Person(PersonModel):
    """
        Model of a Person
    """
    # Link with user
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='%(class)s_user')
    last_name = models.CharField(max_length=64, verbose_name='Name', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'persons'

    @property
    def full_name(self):
        return "{} {}".format(self.user.email or "", self.last_name or "").strip()

    def __str__(self):
        return self.full_name

class Company(CompanyModel,PersistentModel):
    """
        Model of a company
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='%(class)s_user')

    class Meta:
        verbose_name_plural = 'companies'

