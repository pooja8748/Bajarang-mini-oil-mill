from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order, Payment
from .serializers import OrderSerializer, CreateOrderSerializer, PaymentSerializer

# Razorpay client disabled for demo

class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]  # Allow anonymous orders
    
    def get_queryset(self):
        return Order.objects.all().prefetch_related('items__product')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    queryset = Order.objects.all().prefetch_related('items__product')

@api_view(['POST'])
@permission_classes([AllowAny])
def create_razorpay_order(request):
    try:
        amount = int(float(request.data.get('amount')) * 100)  # Convert to paise
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': f'order_{request.data.get("order_id")}',
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        return Response({
            'razorpay_order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency']
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_payment(request):
    try:
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')
        order_id = request.data.get('order_id')
        
        # Verify signature
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature == razorpay_signature:
            # Payment successful
            order = Order.objects.get(id=order_id)
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_signature': razorpay_signature,
                    'amount': order.total_amount,
                    'status': 'success'
                }
            )
            order.status = 'confirmed'
            order.save()
            
            return Response({'status': 'success', 'message': 'Payment verified successfully'})
        else:
            return Response({'status': 'failed', 'message': 'Payment verification failed'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
@permission_classes([AllowAny])
def razorpay_webhook(request):
    try:
        webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
        webhook_body = request.body
        
        # Verify webhook signature
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            webhook_body,
            hashlib.sha256
        ).hexdigest()
        
        if webhook_signature == expected_signature:
            # Process webhook data
            return Response({'status': 'success'})
        else:
            return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Admin views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_orders(request):
    if not request.user.is_staff:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    orders = Order.objects.all().prefetch_related('items__product', 'payment')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_payments(request):
    if not request.user.is_staff:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    payments = Payment.objects.all().select_related('order')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)