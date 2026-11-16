from apps.menu.models import MenuItem
from apps.orders.models import Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


def staff_check(user):
  return user.is_authenticated and user.is_canteen_staff()


@login_required
@user_passes_test(staff_check)
def kitchen_dashboard(request):
  active_orders = (
      Order.objects.filter(status__in=['PLACED', 'PREPARING', 'READY'])
      .select_related('user', 'slot')
      .prefetch_related('items__item')
      .order_by('slot__start_time', 'created_at')
  )

  completed_today = Order.objects.filter(status='COMPLETED').count()
  menu_items = MenuItem.objects.all().order_by('category__name', 'name')

  return render(
      request,
      'kitchen/dashboard.html',
      {
          'orders': active_orders,
          'completed_count': completed_today,
          'menu_items': menu_items,
      },
  )


@login_required
@user_passes_test(staff_check)
def update_order_status(request, order_id):
  if request.method == 'POST':
    new_status = request.POST.get('status')
    order = get_object_or_404(Order, id=order_id)
    if new_status in dict(Order.STATUS_CHOICES):
      order.status = new_status
      order.save()
      messages.success(
          request,
          f'Token {order.token_number} status updated to'
          f' {order.get_status_display()}.',
      )
  return redirect('kitchen_dashboard')


@login_required
@user_passes_test(staff_check)
def restock_item(request, item_id):
  if request.method == 'POST':
    add_qty = int(request.POST.get('add_qty', 10))
    item = get_object_or_404(MenuItem, id=item_id)
    item.stock_quantity = max(0, item.stock_quantity + add_qty)
    item.save()
    messages.success(
        request, f'Updated stock for {item.name} to {item.stock_quantity}.'
    )
  return redirect('kitchen_dashboard')


@login_required
@user_passes_test(staff_check)
def scan_token_view(request):
  return render(request, 'kitchen/scan_token.html')


@login_required
@user_passes_test(staff_check)
def verify_scanned_token(request):
  qr_data = request.GET.get('qr_data', '').strip()
  token_manual = request.GET.get('token_number', '').strip().upper()

  order = None
  if qr_data.startswith('CANTEENGO:'):
    parts = qr_data.split(':')
    if len(parts) >= 3:
      order = Order.objects.filter(
          token_number=parts[1], order_uuid=parts[2]
      ).first()
  elif token_manual:
    order = Order.objects.filter(token_number=token_manual).first()

  if not order:
    return JsonResponse(
        {'valid': False, 'message': 'Invalid QR Code or Token Not Found!'}
    )

  if order.status == 'COMPLETED':
    return JsonResponse({
        'valid': False,
        'message': (
            f'Token {order.token_number} was ALREADY collected by'
            f' {order.user.username}!'
        ),
    })

  order.status = 'COMPLETED'
  order.save()

  items_summary = [f'{i.quantity}x {i.item.name}' for i in order.items.all()]
  return JsonResponse({
      'valid': True,
      'token': order.token_number,
      'student': (
          f"{order.user.username} ({order.user.roll_number or 'Student'})"
      ),
      'slot': (
          f"{order.slot.start_time.strftime('%I:%M %p')} -"
          f" {order.slot.end_time.strftime('%I:%M %p')}"
      ),
      'items': items_summary,
  })