from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    TitleFieldPanel,
)
from modelcluster.models import ClusterableModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from wagtail import blocks
from wagtail.fields import StreamField
from colorfield.fields import ColorField
from autoslug import AutoSlugField
from wagtail.images.blocks import ImageChooserBlock


class ProductCategory(models.Model):
    title = models.CharField(max_length=30, blank=False)
    slug = AutoSlugField(populate_from="title", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
            ],
            heading="Category Information",
        ),
    ]

    def __str__(self):
        return self.title


class Product(ClusterableModel):
    title = models.CharField(max_length=30, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    small_description = models.TextField(max_length=500, blank=True)
    description = StreamField(
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
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_highlight = models.BooleanField(default=False)

    meta_key = models.TextField(max_length=255, blank=True, null=True)
    meta_desc = models.TextField(max_length=160, blank=True, null=True)

    views = models.IntegerField(default=0)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
            ],
            heading="Product Information",
        ),
        MultiFieldPanel(
            [
                FieldPanel("small_description"),
                FieldPanel("description"),
                FieldPanel("category"),
                FieldPanel("is_highlight"),
            ],
            heading="Description and Category",
        ),
        InlinePanel("product_gallery", label="Product Gallery"),
        InlinePanel("product_spec", label="Product Spec"),
        InlinePanel("product_marketplace", label="Product Marketplace"),
        MultiFieldPanel(
            [
                FieldPanel("meta_key"),
                FieldPanel("meta_desc"),
            ],
            heading="SEO Information",
        ),
    ]

    def __str__(self):
        return self.title


# inline
class ProductGallery(models.Model):
    product = ParentalKey(
        Product, related_name="product_gallery", blank=True, null=True
    )
    image = models.ImageField(upload_to="product/gallery", null=True, default=None)
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(400, 400)],
        format="webP",
        options={"quality": 80},
    )
    image_processed = ImageSpecField(
        source="image",
        processors=[ResizeToFill(1000, 1000)],
        format="webP",
        options={"quality": 90},
    )

    panels = [
        FieldPanel("image"),
    ]

    class Meta:
        verbose_name = "Product Gallery"
        verbose_name_plural = "Product Galleries"


class Specification(models.Model):
    title = models.CharField(max_length=50, unique=True)
    order = models.IntegerField(blank=True, null=True, default=0)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("order"),
            ],
            heading="Specification Table Information",
        ),
    ]

    def __str__(self):
        return self.title


# inline
class ProductSpecification(models.Model):
    product = ParentalKey(Product, related_name="product_spec", blank=True, null=True)
    table = models.ForeignKey(Specification, on_delete=models.CASCADE)
    value = models.CharField(max_length=200, blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("table"),
                FieldPanel("value"),
            ],
            heading="Product Specification",
        ),
    ]


# admin:
class MarketPlace(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="marketplace/logo", null=False, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("link"),
                FieldPanel("image"),
            ],
            heading="Marketplace Information",
        ),
    ]

    def __str__(self):
        return self.title


# inline
class ProductMarketplace(models.Model):
    product = ParentalKey(
        Product, related_name="product_marketplace", blank=True, null=True
    )
    marketplace = models.ForeignKey(MarketPlace, on_delete=models.CASCADE)
    additional_text = models.CharField(max_length=50, blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("marketplace"),
                FieldPanel("additional_text"),
                FieldPanel("link"),
            ],
            heading="Product Marketplace",
        ),
    ]
