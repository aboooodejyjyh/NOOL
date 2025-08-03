from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    """
    Represents a product in the grocery store inventory.
    """
    name = models.CharField(_("Product Name"), max_length=255)
    barcode = models.CharField(_("Barcode"), max_length=100, unique=True, help_text=_("Unique barcode for the product."))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)
    reorder_threshold = models.PositiveIntegerField(
        _("Reorder Threshold"),
        default=10,
        help_text=_("The quantity at which to trigger a low stock alert.")
    )

    UNIT_CHOICES = [
        ('piece', _('Piece')),
        ('kg', _('Kilogram')),
        ('g', _('Gram')),
        ('l', _('Liter')),
        ('ml', _('Milliliter')),
    ]
    unit = models.CharField(_("Unit"), max_length=10, choices=UNIT_CHOICES, default='piece')

    expiration_date = models.DateField(_("Expiration Date"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']
