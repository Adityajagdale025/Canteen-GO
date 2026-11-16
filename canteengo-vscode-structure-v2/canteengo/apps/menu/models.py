from django.db import models
from django.db.models import Avg


class Category(models.Model):
  name = models.CharField(max_length=60, unique=True)

  class Meta:
    verbose_name_plural = 'Categories'

  def __str__(self):
    return self.name


class MenuItem(models.Model):
  category = models.ForeignKey(
      Category, on_delete=models.CASCADE, related_name='items'
  )
  name = models.CharField(max_length=120)
  description = models.TextField(blank=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  stock_quantity = models.PositiveIntegerField(default=0)
  is_available = models.BooleanField(default=True)
  image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

  def is_in_stock(self):
    return self.is_available and self.stock_quantity > 0

  def average_rating(self):
    from apps.feedback.models import Feedback

    avg = Feedback.objects.filter(order__items__item=self).aggregate(
        Avg('rating')
    )['rating__avg']
    return round(avg, 1) if avg else None

  def __str__(self):
    return f'{self.name} (₹{self.price}) - Stock: {self.stock_quantity}'