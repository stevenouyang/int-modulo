from django.db import models
from django.urls import reverse
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from autoslug import AutoSlugField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TitleFieldPanel
from wagtail.search import index
from django.contrib.contenttypes.fields import GenericRelation
from wagtail.models import RevisionMixin
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from django.db.models.signals import pre_save
from django.dispatch import receiver
import math
import uuid
import os
from bs4 import BeautifulSoup
from wagtail.models import Page, Orderable
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from .utils import process_portfolio_content

class PortfolioIndex(Page):
    template            = "a_page/page/dummy.html"

    subpage_types       = ['a_portfolio.Portfolio']
    parent_page_types   = ['home.HomePage']
    max_count           = 1

    # Main listing page: /portfolio/
    def get_context(self, request):
        context             = super().get_context(request)
        context['posts']    = Portfolio.objects.live().descendant_of(self)
        return context


class PortfolioPageTag(TaggedItemBase):
    content_object = ParentalKey('a_portfolio.Portfolio', on_delete=models.CASCADE, related_name='tagged_items')


class Portfolio(Page):
    template                = "a_portfolio/page/details.html"
    parent_page_types       = ['a_portfolio.PortfolioIndex']
    subpage_types           = []

    tags                    = ClusterTaggableManager(through=PortfolioPageTag, blank=True)
    is_show                 = models.BooleanField(default=True)
    image                   = models.ImageField(upload_to="portfolio/main", null=True, default=None)

    client                  = models.CharField(max_length=255, blank=True, null=True)
    project_date            = models.DateField(blank=True, null=True)
    url                     = models.URLField(blank=True, null=True)

    image_processed         = ImageSpecField(
                                source="image",
                                processors=[ResizeToFill(1920, 1080)],
                                format="webP",
                                options={"quality": 90},
                            )

    overview                = models.TextField(blank=True, null=True)

    content                 = StreamField(
                                [
                                    (
                                        "paragraph",
                                        blocks.RichTextBlock(features=["p", "a"]),
                                    ),
                                    (
                                        "h4",
                                        blocks.CharBlock(features=["h4"]),
                                    ),
                                    (
                                        "h5",
                                        blocks.CharBlock(features=["h6"]),
                                    ),
                                    (
                                        "h6",
                                        blocks.CharBlock(features=["h6"]),
                                    ),
                                    (
                                        "ordered_list",
                                        blocks.RichTextBlock(
                                            features=["ol"],
                                        ),
                                    ),
                                    (
                                        "unordered_list",
                                        blocks.RichTextBlock(
                                            features=["ul"],
                                        ),
                                    ),
                                    ("blockquote_1", blocks.CharBlock()),
                                    (
                                        "image_1280x720",
                                        ImageChooserBlock(label="Image 1280x720", help_text="1280 x 720"),
                                    ),
                                    (
                                        "image_1280x1280",
                                        ImageChooserBlock(label="Image 1280x1280", help_text="1280 x 1280"),
                                    ),
                                    (
                                        "image_1280x800",
                                        ImageChooserBlock(label="Image 1280x800", help_text="1280 x 800"),
                                    ),
                                    ("url", blocks.URLBlock()),
                                    ('button', blocks.StructBlock([
                                        ('text', blocks.CharBlock(required=True)),
                                        ('url', blocks.URLBlock(required=True)),
                                    ], icon='plus')),
                                    ("spacer", blocks.StaticBlock(label="Spacer")),
                                    ("html", blocks.RawHTMLBlock(label="Raw HTML", icon="code")),
                                ],
                                use_json_field=True,
                                null=True,
                                blank=True,
                            )

    # seo
    meta_key                = models.TextField(max_length=100, blank=True, null=True)
    meta_desc               = models.TextField(max_length=160, blank=True, null=True)

    # date
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    content_panels = [
        TitleFieldPanel("title"),
        MultiFieldPanel([
            FieldPanel("tags"),
            FieldPanel("client"),
            FieldPanel("project_date"),
            FieldPanel("url"),
            FieldPanel("is_show"),
        ], heading="Project Information"),

        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("overview"),
            FieldPanel("content"),
        ], heading="Content"),

        MultiFieldPanel([
            InlinePanel("portfolio_highlight", label="Portfolio Highlight"),
            InlinePanel("portfolio_gallery", label="Portfolio Image"),
        ], heading="Portfolio Details"),

        MultiFieldPanel([
            FieldPanel("meta_key"),
            FieldPanel("meta_desc"),
        ], heading="SEO Settings"),
    ]

    def get_processed_content(self):
        """
        Returns a processed version of the StreamField content with
        resized image URLs and list items extracted.
        """
        from copy import deepcopy
        content_copy = deepcopy(self.content)
        process_portfolio_content(content_copy)

        print("processing blog content")
        return content_copy

    def __str__(self):
        return self.title



# inline: portfolio
class PortfolioHightlight(Orderable):
    portfolio       = ParentalKey(Portfolio, related_name="portfolio_highlight")
    title           = models.CharField(max_length=50)
    title_id        = models.CharField(max_length=50, blank=True, null=True)

# inline: portfolio
class PortfolioGallery(Orderable):
    portfolio       = ParentalKey(Portfolio, related_name='portfolio_gallery')
    title           = models.CharField(max_length=40, blank=True, null=True)
    image           = models.ImageField(upload_to='portfolio/gallery')