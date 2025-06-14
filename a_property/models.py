import os
from urllib.parse import urlencode
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from autoslug import AutoSlugField
from django.conf import settings
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamBlock
from wagtail.fields import RichTextField, StreamField

class PropertyAgent(models.Model):
    name            = models.CharField(max_length=100, blank=True, null=True)
    title           = models.CharField(max_length=100, blank=True, null=True)
    location        = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_url    = models.URLField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    image           = models.ImageField(upload_to="property/agents")
    proc_image      = ImageSpecField(
                        source="image",
                        processors=[ResizeToFill(240, 240)],
                        format="webP",
                        options={"quality": 90},
                    )

    panels = [
        FieldPanel("name"),
        FieldPanel("title"),
        FieldPanel("whatsapp_url"),
        FieldPanel("whatsapp_number"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.name
