from django.urls import path
from . import views

urlpatterns = [
    path('', views.live_menu_view, name='live_menu'),
]