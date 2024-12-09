from django.db import models
from django.contrib.auth.models import User

class Subdomain(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('pending', 'Pending Approval'),
    ]

    name = models.CharField(max_length=50, unique=True, help_text="Subdomain name, e.g., 'blog'")
    purpose = models.TextField(help_text="Describe the purpose of this subdomain.")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Status of the subdomain."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subdomains',
        help_text="The user who requested this subdomain."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the subdomain was requested.")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the subdomain was last updated.")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subdomain'
        verbose_name_plural = 'Subdomains'

    def __str__(self):
        return f"{self.name}.dovuchcha.uz ({self.status})"