from rest_framework import serializers
from .models import Order, OrderItem, Payment
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name_english', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'package_size', 
                 'unit_type', 'price']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'razorpay_payment_id', 'razorpay_order_id', 'amount', 
                 'status', 'payment_date']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone', 
                 'order_date', 'status', 'total_amount', 'shipping_address', 
                 'notes', 'items', 'payment']
        read_only_fields = ['order_date']

class CreateOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 
                 'shipping_address', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total = sum(item['price'] * item['quantity'] for item in items_data)
        
        order = Order.objects.create(
            total_amount=total,
            **validated_data
        )
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order