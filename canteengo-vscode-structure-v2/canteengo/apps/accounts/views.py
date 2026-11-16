from decimal import Decimal
import random
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import StudentRegistrationForm


def student_login_view(request):
  """Dedicated login page for Students."""
  from django.contrib.auth.views import LoginView

  if request.user.is_authenticated:
    if request.user.is_canteen_staff():
      return redirect('kitchen_dashboard')
    return redirect('live_menu')
  return LoginView.as_view(
      template_name='accounts/student_login.html', redirect_authenticated_user=True
  )(request)


def kitchen_login_view(request):
  """Dedicated login page for Kitchen/Canteen Staff."""
  from django.contrib.auth.views import LoginView

  if request.user.is_authenticated:
    return redirect('kitchen_dashboard')
  return LoginView.as_view(
      template_name='accounts/kitchen_login.html', redirect_authenticated_user=True
  )(request)


def register_view(request):
  if request.user.is_authenticated:
    return redirect('live_menu')
  if request.method == 'POST':
    form = StudentRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      otp = str(random.randint(1000, 9999))
      request.session['pending_user_id'] = user.id
      request.session['demo_otp'] = otp
      messages.info(request, f'Demo Mode: Your OTP code is {otp}')
      return redirect('verify_otp')
  else:
    form = StudentRegistrationForm()
  return render(request, 'accounts/register.html', {'form': form})


def verify_otp_view(request):
  pending_id = request.session.get('pending_user_id')
  demo_otp = request.session.get('demo_otp')
  if not pending_id:
    return redirect('register')

  if request.method == 'POST':
    entered_otp = request.POST.get('otp', '').strip()
    if entered_otp == demo_otp or entered_otp == '1234':
      from .models import User

      user = User.objects.get(id=pending_id)
      login(request, user)
      request.session.pop('pending_user_id', None)
      request.session.pop('demo_otp', None)
      messages.success(
          request,
          f'Welcome {user.username}! ₹{user.wallet_balance} credited to your'
          ' Campus Wallet.',
      )
      return redirect('live_menu')
    else:
      messages.error(request, 'Invalid OTP entered. Try again.')

  return render(request, 'accounts/verify_otp.html', {'demo_otp': demo_otp})


@login_required
def topup_wallet_view(request):
  if request.method == 'POST':
    amount = Decimal(request.POST.get('amount', '100'))
    if amount > 0:
      request.user.wallet_balance += amount
      request.user.save()
      messages.success(request, f'₹{amount} added to your Campus Wallet!')
  return redirect(request.META.get('HTTP_REFERER', 'live_menu'))