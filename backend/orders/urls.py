from django.urls import path
from .views import (
    OrderListCreateView, OrderDetailView, create_razorpay_order,
    verify_payment, razorpay_webhook, admin_orders, admin_payments
)

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('create-razorpay-order/', create_razorpay_order, name='create-razorpay-order'),
    path('verify-payment/', verify_payment, name='verify-payment'),
    path('webhook/', razorpay_webhook, name='razorpay-webhook'),
    path('admin/orders/', admin_orders, name='admin-orders'),
    path('admin/payments/', admin_payments, name='admin-payments'),
]