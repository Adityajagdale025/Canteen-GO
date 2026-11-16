from datetime import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteengo_core.settings')
django.setup()

from apps.accounts.models import User
from apps.menu.models import Category, MenuItem
from apps.orders.models import TimeSlot


def run_seed():
  print('Seeding CanteenGo initial data with expanded menu...')

  # 1. Create Staff/Admin and Student Users
  if not User.objects.filter(username='staff').exists():
    User.objects.create_superuser(
        username='staff',
        email='staff@canteengo.edu',
        password='password123',
        role='STAFF',
        phone_number='9876543210',
        wallet_balance=500.00,
    )
    print('Created Staff/Admin user -> username: staff | password: password123')

  if not User.objects.filter(username='student').exists():
    User.objects.create_user(
        username='student',
        email='student@mitadt.edu.in',
        password='password123',
        role='STUDENT',
        roll_number='SY26-BCAIA-01',
        phone_number='9123456780',
        wallet_balance=350.00,
    )
    print('Created Student user -> username: student | password: password123')

  # 2. Create Categories
  snacks_cat, _ = Category.objects.get_or_create(name='Quick Snacks')
  meals_cat, _ = Category.objects.get_or_create(name='Meals & Combos')
  beverages_cat, _ = Category.objects.get_or_create(name='Beverages')
  fastfood_cat, _ = Category.objects.get_or_create(name='Fast Food & Burgers')
  desserts_cat, _ = Category.objects.get_or_create(name='Desserts & Bakery')

  # 3. Expanded Menu Items
  sample_items = [
      # Quick Snacks
      (
          snacks_cat,
          'Vada Pav (2 pcs)',
          'Hot Mumbai-style vada pav with spicy dry garlic chutney',
          30.00,
          40,
      ),
      (
          snacks_cat,
          'Samosa Plate (2 pcs)',
          'Crispy Punjabi samosas served with tangy tamarind & mint chutney',
          35.00,
          30,
      ),
      (
          snacks_cat,
          'Misal Pav',
          'Spicy sprouted moth bean curry topped with farsan, onions, and pav',
          60.00,
          25,
      ),
      (
          snacks_cat,
          'Bread Pattice',
          'Deep-fried bread pockets stuffed with spiced mashed potatoes',
          25.00,
          20,
      ),
      # Fast Food & Burgers
      (
          fastfood_cat,
          'Cheese Grilled Sandwich',
          'Three-layer vegetable & cheddar cheese grilled sandwich',
          65.00,
          20,
      ),
      (
          fastfood_cat,
          'Crispy Veg Burger',
          'Crunchy potato & vegetable patty with lettuce and mayo',
          75.00,
          25,
      ),
      (
          fastfood_cat,
          'Peri Peri French Fries',
          'Golden french fries tossed in spicy peri peri seasoning',
          60.00,
          30,
      ),
      (
          fastfood_cat,
          'Veg Hakka Noodles',
          'Wok-tossed Indo-Chinese noodles with fresh crunchy veggies',
          80.00,
          25,
      ),
      # Meals & Combos
      (
          meals_cat,
          'Mini Executive Thali',
          '2 Chapati, Paneer Butter Masala, Dal Fry, Jeera Rice & Salad',
          110.00,
          15,
      ),
      (
          meals_cat,
          'Masala Dosa',
          'Crispy rice crepe stuffed with spiced potato mash, sambar & chutney',
          70.00,
          20,
      ),
      (
          meals_cat,
          'Chole Bhature (2 pcs)',
          'Fluffy fried bread served with spicy chickpea curry and pickles',
          90.00,
          18,
      ),
      (
          meals_cat,
          'Fried Rice & Manchurian Bowl',
          'Classic vegetable fried rice paired with dry vegetable manchurian balls',
          95.00,
          22,
      ),
      # Beverages
      (
          beverages_cat,
          'Cold Coffee',
          'Chilled creamy blended coffee topped with cocoa powder',
          50.00,
          35,
      ),
      (
          beverages_cat,
          'Masala Chai',
          'Freshly brewed ginger & cardamom Indian milk tea',
          15.00,
          50,
      ),
      (
          beverages_cat,
          'Fresh Lime Soda',
          'Refreshing sweet and salty lemon soda',
          30.00,
          40,
      ),
      (
          beverages_cat,
          'Mango Milkshake',
          'Thick and creamy seasonal mango milkshake',
          60.00,
          25,
      ),
      # Desserts & Bakery
      (
          desserts_cat,
          'Chocolate Brownie',
          'Fudgy chocolate brownie with chocolate drizzle',
          50.00,
          20,
      ),
      (
          desserts_cat,
          'Gulab Jamun (2 pcs)',
          'Warm, soft milk-solid sweet dumplings in rose sugar syrup',
          35.00,
          30,
      ),
  ]

  for cat, name, desc, price, stock in sample_items:
    MenuItem.objects.get_or_create(
        name=name,
        defaults={
            'category': cat,
            'description': desc,
            'price': price,
            'stock_quantity': stock,
            'is_available': True,
        },
    )

  # 4. Pickup Time Slots
  slots_data = [
      (time(10, 15), time(10, 30), 20),
      (time(10, 30), time(10, 45), 20),
      (time(12, 30), time(12, 45), 30),
      (time(12, 45), time(13, 0), 30),
      (time(13, 0), time(13, 15), 30),
      (time(15, 30), time(15, 45), 25),
  ]
  for start, end, cap in slots_data:
    TimeSlot.objects.get_or_create(
        start_time=start,
        end_time=end,
        defaults={
            'max_capacity': cap,
            'current_bookings': 0,
            'is_active': True,
        },
    )

  print('Successfully seeded expanded canteen menu and time slots!')


if __name__ == '__main__':
  run_seed()