from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from api.managers import UserManager
from django.core.mail import send_mail
from django.db import models

# -----------------------
# User model
# -----------------------
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user','User'),
        ('admin','Admin'),
    )
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    role = models.CharField(_('role'), max_length=30, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField(_('avatar'), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

# -----------------------
# Date model (for booking schedule)
# -----------------------
class Date(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(_('date'))
    time = models.TimeField(_('time'))
    status = models.CharField(max_length=15, choices=STATUS, default='pending')
    created_at = models.DateField(_('created at'), auto_now_add=True)

    objects = models.Manager()

    class Meta:
        unique_together = ('date', 'time')

    def __str__(self):
        return f"{self.date} - {self.time}"

# -----------------------
# Appointment model
# -----------------------
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    service = models.CharField(max_length=100)
    date = models.DateField()
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=[("pending", "pending"), ("approved", "approved"), ("rejected", "rejected")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
