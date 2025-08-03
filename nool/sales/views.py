import json
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Sale, SaleItem
from inventory.models import Product
from customers.models import Customer

@csrf_exempt
@require_POST
def finalize_sale_view(request):
    try:
        data = json.loads(request.body)
        cart = data.get('cart', {})
        payment_method = data.get('payment_method', 'cash')
        customer_id = data.get('customer_id')

        if not cart:
            return JsonResponse({'success': False, 'error': 'Cart is empty'}, status=400)

        with transaction.atomic():
            # Calculate total amount and check product availability
            total_amount = 0
            products_to_update = []
            sale_item_data = []

            for product_id, item_data in cart.items():
                try:
                    product = Product.objects.select_for_update().get(pk=product_id)
                    quantity = item_data['quantity']
                    if product.quantity < quantity:
                        return JsonResponse({'success': False, 'error': f'Not enough stock for {product.name}'}, status=400)

                    price_at_sale = product.price
                    total_amount += price_at_sale * quantity

                    product.quantity -= quantity
                    products_to_update.append(product)

                    sale_item_data.append({
                        'product': product,
                        'quantity': quantity,
                        'price_at_sale': price_at_sale
                    })

                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'error': f'Product with id {product_id} not found'}, status=400)

            # Get customer if provided
            customer = None
            if customer_id:
                try:
                    customer = Customer.objects.get(pk=customer_id)
                except Customer.DoesNotExist:
                    # Depending on requirements, you might want to handle this differently
                    pass

            # Create the sale
            sale = Sale.objects.create(
                customer=customer,
                total_amount=total_amount,
                payment_method=payment_method
            )

            # Create sale items
            sale_items_to_create = [
                SaleItem(
                    sale=sale,
                    product=item['product'],
                    quantity=item['quantity'],
                    price_at_sale=item['price_at_sale']
                ) for item in sale_item_data
            ]
            SaleItem.objects.bulk_create(sale_items_to_create)

            # Update product quantities
            Product.objects.bulk_update(products_to_update, ['quantity'])

        return JsonResponse({'success': True, 'sale_id': sale.id})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        # For production, you'd want to log this error
        return JsonResponse({'success': False, 'error': f'An unexpected error occurred: {str(e)}'}, status=500)
