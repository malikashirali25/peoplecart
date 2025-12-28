from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.dispatch import receiver
from .models import Order, Customer, Product
from django.contrib.auth.models import User
import json

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    """
    Handle successful PayPal payment
    Create orders when payment is verified
    """
    ipn_obj = sender
    
    if ipn_obj.payment_status == 'Completed':
        try:
            # Get custom data from PayPal
            custom_data = json.loads(ipn_obj.custom) if ipn_obj.custom else {}
            user_id = custom_data.get('user_id')
            cart_items = custom_data.get('cart_items', [])
            
            if not user_id or not cart_items:
                return
            
            # Get user
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return
            
            # Get or create customer
            customer, created = Customer.objects.get_or_create(
                email=user.email,
                defaults={
                    'first_name': user.first_name or user.username,
                    'last_name': user.last_name or '',
                    'phone': '',
                    'password': ''  # Not storing password here
                }
            )
            
            # Create orders for each item
            for item in cart_items:
                try:
                    product = Product.objects.get(id=int(item['id']))
                    quantity = int(item.get('quantity', 1))
                    
                    # Create order
                    order = Order.objects.create(
                        product=product,
                        customer=customer,
                        quantity=quantity,
                        address=ipn_obj.address_street or '',
                        phone=ipn_obj.contact_phone or '',
                        status=True,  # Mark as paid
                    )
                except (Product.DoesNotExist, ValueError, KeyError):
                    continue
                    
        except Exception as e:
            # Log error in production
            print(f"Error processing PayPal IPN: {e}")


@receiver(invalid_ipn_received)
def paypal_payment_failed(sender, **kwargs):
    """
    Handle invalid PayPal payment
    """
    ipn_obj = sender
    # Log failed payment attempts
    print(f"Invalid PayPal IPN received: {ipn_obj}")

