from apps.menu.models import MenuItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .models import Order, OrderItem, TimeSlot
from .utils import generate_order_qr


def _build_cart_context(request):
  cart = request.session.get('cart', {})
  cart_items = []
  total = 0
  for item_id, qty in list(cart.items()):
    try:
      item = MenuItem.objects.get(id=item_id, is_available=True)
      subtotal = item.price * qty
      total += subtotal
      cart_items.append({'item': item, 'qty': qty, 'subtotal': subtotal})
    except MenuItem.DoesNotExist:
      del cart[item_id]
      request.session.modified = True
  return cart_items, total


@login_required
def cart_view(request):
  cart_items, total = _build_cart_context(request)
  slots = TimeSlot.objects.filter(is_active=True)
  return render(
      request,
      'orders/cart.html',
      {
          'cart_items': cart_items,
          'total': total,
          'slots': slots,
      },
  )


@login_required
def add_to_cart(request, item_id):
  item = get_object_or_404(MenuItem, id=item_id)
  cart = request.session.get('cart', {})
  current_qty = cart.get(str(item_id), 0)

  if current_qty + 1 > item.stock_quantity:
    messages.error(
        request,
        f"Cannot add more '{item.name}'. Only {item.stock_quantity} left in"
        ' stock.',
    )
  else:
    cart[str(item_id)] = current_qty + 1
    request.session['cart'] = cart
    messages.success(request, f'Added {item.name} to your tray!')
  return redirect(request.META.get('HTTP_REFERER', 'live_menu'))


@login_required
def update_cart_item(request, item_id, action):
  cart = request.session.get('cart', {})
  key = str(item_id)
  if key in cart:
    if action == 'inc':
      item = get_object_or_404(MenuItem, id=item_id)
      if cart[key] + 1 <= item.stock_quantity:
        cart[key] += 1
      else:
        messages.error(
            request, f'Maximum available stock ({item.stock_quantity}) reached.'
        )
    elif action == 'dec':
      cart[key] -= 1
      if cart[key] <= 0:
        del cart[key]
    elif action == 'remove':
      del cart[key]
    request.session['cart'] = cart
  return redirect('cart')


@login_required
@transaction.atomic
def checkout_view(request):
  cart_items, total = _build_cart_context(request)
  if not cart_items:
    messages.error(request, 'Your tray is empty.')
    return redirect('live_menu')

  slots = TimeSlot.objects.filter(is_active=True)

  if request.method == 'POST':
    slot_id = request.POST.get('slot_id')
    payment_method = request.POST.get('payment_method', 'WALLET')

    slot = get_object_or_404(TimeSlot.objects.select_for_update(), id=slot_id)
    if not slot.is_available():
      messages.error(
          request, 'This time slot just filled up! Please pick another slot.'
      )
      return redirect('checkout')

    locked_items = []
    for entry in cart_items:
      item = MenuItem.objects.select_for_update().get(id=entry['item'].id)
      if item.stock_quantity < entry['qty']:
        messages.error(
            request,
            f"Sorry! '{item.name}' only has {item.stock_quantity} left in"
            ' stock.',
        )
        return redirect('cart')
      locked_items.append((item, entry['qty']))

    if payment_method == 'WALLET':
      if request.user.wallet_balance < total:
        messages.error(
            request,
            'Insufficient Campus Wallet balance'
            f' (₹{request.user.wallet_balance}). Please top up or select UPI.',
        )
        return redirect('checkout')
      request.user.wallet_balance -= total
      request.user.save()

    last_order = Order.objects.order_by('-id').first()
    seq = (last_order.id + 1) if last_order else 1
    token_str = f'CG-{seq:03d}'

    order = Order.objects.create(
        user=request.user,
        slot=slot,
        token_number=token_str,
        total_amount=total,
        payment_method=payment_method,
        payment_status=True,
        status='PLACED',
    )

    for item, qty in locked_items:
      OrderItem.objects.create(
          order=order, item=item, quantity=qty, unit_price=item.price
      )
      item.stock_quantity -= qty
      item.save()

    slot.current_bookings += 1
    slot.save()

    generate_order_qr(order)
    order.save()

    request.session['cart'] = {}
    messages.success(
        request,
        f'Order Confirmed! Digital Token {order.token_number} generated.',
    )
    return redirect('token_view', order_id=order.id)

  return render(
      request,
      'orders/checkout.html',
      {
          'cart_items': cart_items,
          'total': total,
          'slots': slots,
      },
  )


@login_required
def token_view(request, order_id):
  order = get_object_or_404(Order, id=order_id)
  if order.user != request.user and not request.user.is_canteen_staff():
    messages.error(request, 'Unauthorized access.')
    return redirect('live_menu')
  return render(request, 'orders/token_view.html', {'order': order})


@login_required
def order_history(request):
  orders = (
      Order.objects.filter(user=request.user)
      .select_related('slot')
      .prefetch_related('items__item')
      .order_by('-created_at')
  )
  return render(request, 'orders/order_history.html', {'orders': orders})