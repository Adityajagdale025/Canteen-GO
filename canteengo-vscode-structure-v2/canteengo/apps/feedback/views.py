from apps.orders.models import Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Feedback


@login_required
def submit_feedback(request, order_id):
  order = get_object_or_404(Order, id=order_id, user=request.user)
  existing = Feedback.objects.filter(order=order).first()

  if request.method == 'POST':
    rating = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '').strip()
    Feedback.objects.update_or_create(
        order=order,
        defaults={'user': request.user, 'rating': rating, 'comment': comment},
    )
    messages.success(request, f'Thank you for rating Order {order.token_number}!')
    return redirect('order_history')

  return render(
      request,
      'feedback/submit_feedback.html',
      {'order': order, 'existing': existing},
  )