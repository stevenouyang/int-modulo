from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust


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

class HomeSlider(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    cta_button = models.BooleanField(default=True)
    cta_text = models.CharField(max_length=255, blank=True, null=True)
    cta_link = models.URLField(max_length=255, blank=True, null=True)
    cta_new_window = models.BooleanField(default=False)
    image = models.ImageField(upload_to="misc/slider")

    panels = [
        FieldPanel("title"),
        FieldPanel("is_active"),
        FieldPanel("description"),
        FieldPanel("cta_button"),
        FieldPanel("cta_text"),
        FieldPanel("cta_link"),
        FieldPanel("cta_new_window"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.title

class ImageGallery(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="misc/imagegallery")

    panels = [
        FieldPanel("title"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.title

class AnnouncementBar(models.Model):
    title = models.CharField(max_length=150)
    is_show = is_show = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("is_show"),
    ]

    def __str__(self):
        return self.title
