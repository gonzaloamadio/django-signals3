from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from signals.libs.models import AuditedModel
from django.utils import timezone

PERSON = 1
COMPANY = 2
USER_TYPE_CHOICES = (
    (1, 'Person'),
    (2, 'Company'),
)

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/signals.log',
                    filemode='w')
logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        logger.info('[authentication _create_user]')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular User with the given email ,password and user_type."""
        # As the user_type is required, check it
        logger.info('[authentication create_user]')
        if not 'user_type' in extra_fields:
            raise ValueError('User Type is required')
        else:
            try:
                ut = int(extra_fields.get('user_type'))
            except ValueError as err:
                # TODO : log to file
                raise ValueError('User Type format error')
            # Check if user_type is correct
            if not ut in [a for a,b in USER_TYPE_CHOICES]:
                raise ValueError('User Type unknown')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email field'),unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    bio = models.TextField(max_length=512, blank=True, default='')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # As we will not have much types of user, we define types of user in the
    # User model. Then we will do profiles for specific data of each user.
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)

    # Substitute this field to tell that email will be username.
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # Create index for the email field
        indexes = (
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),
        )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
