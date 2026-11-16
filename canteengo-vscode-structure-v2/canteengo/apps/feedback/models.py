from apps.orders.models import Order
from django.conf import settings
from django.db import models


class Feedback(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  order = models.OneToOneField(
      Order, on_delete=models.CASCADE, related_name='feedback'
  )
  rating = models.PositiveSmallIntegerField(
      choices=[(i, f'{i} Stars') for i in range(1, 6)]
  )
  comment = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return (
        f'Token {self.order.token_number} - {self.rating}★ by'
        f' {self.user.username}'
    )