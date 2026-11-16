from django.contrib import admin
from .models import Order, OrderItem, TimeSlot


class OrderItemInline(admin.TabularInline):
  model = OrderItem
  extra = 0


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
  list_display = (
      'start_time',
      'end_time',
      'current_bookings',
      'max_capacity',
      'is_active',
  )
  list_editable = ('max_capacity', 'current_bookings', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = (
      'token_number',
      'user',
      'slot',
      'total_amount',
      'payment_method',
      'status',
      'created_at',
  )
  list_filter = ('status', 'payment_method', 'slot')
  search_fields = ('token_number', 'user__username', 'user__roll_number')
  inlines = [OrderItemInline]