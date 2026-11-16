from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.kitchen_dashboard, name='kitchen_dashboard'),
    path(
        'update-status/<int:order_id>/',
        views.update_order_status,
        name='update_order_status',
    ),
    path('restock/<int:item_id>/', views.restock_item, name='restock_item'),
    path('scan/', views.scan_token_view, name='scan_token'),
    path('api/verify-token/', views.verify_scanned_token, name='verify_token'),
]