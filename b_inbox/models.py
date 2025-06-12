from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

class SubmittedForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    interest = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("name", read_only=True),
            FieldPanel("email", read_only=True),
            FieldPanel("phone", read_only=True),
            FieldPanel("interest", read_only=True),
            FieldPanel("message", read_only=True),
            FieldPanel("date_created", read_only=True),
        ], heading="Submitted Form (Read-Only)")
    ]

    def __str__(self):
        return f"{self.name} - {self.email}"
