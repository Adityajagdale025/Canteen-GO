from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  ROLE_CHOICES = (
      ('STUDENT', 'Student'),
      ('STAFF', 'Canteen Staff'),
      ('ADMIN', 'College Admin'),
  )
  role = models.CharField(
      max_length=10, choices=ROLE_CHOICES, default='STUDENT'
  )
  roll_number = models.CharField(
      max_length=30, blank=True, null=True, unique=True
  )
  phone_number = models.CharField(max_length=15, blank=True, null=True)
  wallet_balance = models.DecimalField(
      max_digits=8, decimal_places=2, default=250.00
  )

  def is_canteen_staff(self):
    return (
        self.role in ('STAFF', 'ADMIN') or self.is_staff or self.is_superuser
    )

  def __str__(self):
    return f'{self.username} ({self.get_role_display()})'