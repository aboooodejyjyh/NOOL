from django.db import models
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    """
    Represents a customer.
    """
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    email = models.EmailField(_("Email"), max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, unique=True, null=True, blank=True)
    address = models.TextField(_("Address"), blank=True)
    loyalty_points = models.PositiveIntegerField(_("Loyalty Points"), default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ['last_name', 'first_name']
