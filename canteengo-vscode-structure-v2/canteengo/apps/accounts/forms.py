from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class StudentRegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True)
  roll_number = forms.CharField(
      max_length=30, required=True, help_text='e.g., SY26-BCAIA-05'
  )
  phone_number = forms.CharField(max_length=15, required=True)

  class Meta(UserCreationForm.Meta):
    model = User
    fields = ('username', 'email', 'roll_number', 'phone_number')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = (
          'w-full border border-gray-300 rounded-lg px-3 py-2'
          ' focus:outline-none focus:ring-2 focus:ring-indigo-500'
      )

  def save(self, commit=True):
    user = super().save(commit=False)
    user.role = 'STUDENT'
    user.wallet_balance = 250.00
    if commit:
      user.save()
    return user