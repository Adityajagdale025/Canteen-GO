from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/student/', views.student_login_view, name='student_login'),
    path('login/kitchen/', views.kitchen_login_view, name='kitchen_login'),
    path(
        'logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'
    ),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('wallet/topup/', views.topup_wallet_view, name='topup_wallet'),
]