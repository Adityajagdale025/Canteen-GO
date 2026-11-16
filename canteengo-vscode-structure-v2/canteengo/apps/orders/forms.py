from django import forms
from .models import TimeSlot


class CheckoutSlotForm(forms.Form):
  slot_id = forms.ModelChoiceField(
      queryset=TimeSlot.objects.filter(is_active=True),
      empty_label='Select Pickup Time Slot',
      widget=forms.Select(attrs={'class': 'w-full border rounded-lg p-2.5'}),
  )
  payment_method = forms.ChoiceField(
      choices=[('WALLET', 'Campus Wallet'), ('UPI', 'UPI / QR Payment')],
      widget=forms.RadioSelect,
  )