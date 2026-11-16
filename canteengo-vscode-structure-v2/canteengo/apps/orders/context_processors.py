def cart_Counter(request):
  cart = request.session.get('cart', {})
  total_count = sum(cart.values()) if isinstance(cart, dict) else 0
  return {'cart_item_count': total_count}