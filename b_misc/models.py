from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    is_show = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("company"),
            FieldPanel("content"),
            FieldPanel("is_show"),
        ], heading="Testimonial Details"),
    ]

    def __str__(self):
        return f"{self.name} ({self.company})"


class ClientLogo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='client_logos/')
    is_show = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("image"),
            FieldPanel("is_show"),
        ], heading="Client Logo Details"),
    ]

    def __str__(self):
        return self.name
