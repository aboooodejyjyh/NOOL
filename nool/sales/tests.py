import json
from django.test import TestCase, Client
from django.urls import reverse
from inventory.models import Product
from .models import Sale, SaleItem

class SaleFinalizationAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(name="Apple", barcode="123", price="1.00", quantity=10)
        self.product2 = Product.objects.create(name="Banana", barcode="456", price="0.50", quantity=20)
        self.api_url = reverse('sales:finalize_sale_api')

    def test_finalize_sale_success(self):
        cart_data = {
            str(self.product1.id): {'quantity': 2},
            str(self.product2.id): {'quantity': 5},
        }
        sale_data = {'cart': cart_data}

        response = self.client.post(
            self.api_url,
            data=json.dumps(sale_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertTrue(Sale.objects.filter(id=response_data['sale_id']).exists())

        # Check that product quantities were updated
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.quantity, 8)
        self.assertEqual(self.product2.quantity, 15)

        # Check that SaleItems were created
        sale = Sale.objects.get(id=response_data['sale_id'])
        self.assertEqual(sale.items.count(), 2)
        self.assertEqual(sale.total_amount, (2 * 1.00) + (5 * 0.50))

    def test_finalize_sale_insufficient_stock(self):
        cart_data = {
            str(self.product1.id): {'quantity': 11}, # More than available
        }
        sale_data = {'cart': cart_data}

        response = self.client.post(
            self.api_url,
            data=json.dumps(sale_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data.get('success', True))
        self.assertIn('error', response_data)
        self.assertIn('Not enough stock', response_data['error'])

        # Check that product quantity was not changed
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.quantity, 10)
        self.assertEqual(Sale.objects.count(), 0)
        self.assertEqual(SaleItem.objects.count(), 0)
