from django.contrib import admin
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
  list_display = (
      'name',
      'category',
      'price',
      'stock_quantity',
      'is_available',
  )
  list_filter = ('category', 'is_available')
  list_editable = ('price', 'stock_quantity', 'is_available')
  search_fields = ('name', 'description')