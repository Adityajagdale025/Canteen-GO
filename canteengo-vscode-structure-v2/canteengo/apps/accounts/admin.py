from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
  fieldsets = UserAdmin.fieldsets + (
      (
          'CanteenGo Profile',
          {'fields': ('role', 'roll_number', 'phone_number', 'wallet_balance')},
      ),
  )
  list_display = (
      'username',
      'email',
      'roll_number',
      'role',
      'wallet_balance',
      'is_staff',
  )
  list_filter = ('role', 'is_staff', 'is_active')