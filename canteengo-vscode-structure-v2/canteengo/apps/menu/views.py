from django.shortcuts import render
from .models import Category, MenuItem


def live_menu_view(request):
  category_id = request.GET.get('category')
  search_query = request.GET.get('q', '').strip()

  categories = Category.objects.all()
  items = MenuItem.objects.filter(is_available=True).select_related('category')

  if category_id:
    items = items.filter(category_id=category_id)
  if search_query:
    items = items.filter(name__icontains=search_query)

  context = {
      'categories': categories,
      'items': items,
      'selected_category': (
          int(category_id) if category_id and category_id.isdigit() else None
      ),
      'search_query': search_query,
  }
  return render(request, 'menu/live_menu.html', context)