import uuid
from apps.menu.models import MenuItem
from django.conf import settings
from django.db import models


class TimeSlot(models.Model):
  start_time = models.TimeField()
  end_time = models.TimeField()
  max_capacity = models.PositiveIntegerField(default=25)
  current_bookings = models.PositiveIntegerField(default=0)
  is_active = models.BooleanField(default=True)

  class Meta:
    ordering = ['start_time']

  def is_available(self):
    return self.is_active and self.current_bookings < self.max_capacity

  @property
  def spots_left(self):
    return max(0, self.max_capacity - self.current_bookings)

  def __str__(self):
    return (
        f"{self.start_time.strftime('%I:%M %p')} -"
        f" {self.end_time.strftime('%I:%M %p')} ({self.spots_left} spots left)"
    )


class Order(models.Model):
  STATUS_CHOICES = (
      ('PLACED', 'Order Placed'),
      ('PREPARING', 'Preparing in Kitchen'),
      ('READY', 'Ready for Pickup'),
      ('COMPLETED', 'Collected'),
      ('CANCELLED', 'Cancelled'),
  )
  PAYMENT_CHOICES = (
      ('WALLET', 'Campus Wallet'),
      ('UPI', 'UPI Instant Pay'),
  )

  user = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
  )
  slot = models.ForeignKey(
      TimeSlot, on_delete=models.PROTECT, related_name='orders'
  )
  token_number = models.CharField(max_length=20, unique=True, editable=False)
  order_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  total_amount = models.DecimalField(
      max_digits=8, decimal_places=2, default=0.0
  )
  payment_method = models.CharField(
      max_length=15, choices=PAYMENT_CHOICES, default='WALLET'
  )
  payment_status = models.BooleanField(default=True)
  status = models.CharField(
      max_length=15, choices=STATUS_CHOICES, default='PLACED'
  )
  qr_code = models.ImageField(upload_to='order_qrs/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Token {self.token_number} | {self.user.username} | {self.status}'


class OrderItem(models.Model):
  order = models.ForeignKey(
      Order, on_delete=models.CASCADE, related_name='items'
  )
  item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
  quantity = models.PositiveIntegerField(default=1)
  unit_price = models.DecimalField(max_digits=6, decimal_places=2)

  @property
  def subtotal(self):
    return self.quantity * self.unit_price