from django.db import models
from django.utils.translation import gettext_lazy as _
from inventory.models import Product
from customers.models import Customer

class Sale(models.Model):
    """
    Represents a single sales transaction.
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Customer"))
    total_amount = models.DecimalField(_("Total Amount"), max_digits=10, decimal_places=2)

    PAYMENT_METHOD_CHOICES = [
        ('cash', _('Cash')),
        ('card', _('Card')),
        ('online', _('Online')),
    ]
    payment_method = models.CharField(_("Payment Method"), max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cash')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")
        ordering = ['-created_at']

class SaleItem(models.Model):
    """
    Represents a single item within a sale.
    """
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE, verbose_name=_("Sale"))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(_("Quantity"))
    price_at_sale = models.DecimalField(_("Price at Sale"), max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.price_at_sale}"

    class Meta:
        verbose_name = _("Sale Item")
        verbose_name_plural = _("Sale Items")
