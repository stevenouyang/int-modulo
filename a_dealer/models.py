from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from django.urls import reverse
from autoslug import AutoSlugField
from imagekit.processors import Resize
from wagtail.contrib.table_block.blocks import TableBlock

# Create your models here.
class Car(index.Indexed, ClusterableModel):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", blank=True, null=True)
    is_coming_soon = models.BooleanField(default=False)
    image = models.ImageField(upload_to='car/single')
    small_description = models.TextField(blank=True, null=True)
    overview = StreamField(
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
            (
                "table",
                TableBlock(label="Table"),
            ),
            ("blockquote_1", blocks.CharBlock()),
            ("url", blocks.URLBlock()),
            ("spacer", blocks.StaticBlock(label="Spacer")),
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )
    youtube_embed = models.TextField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    pdf_catalogue = models.FileField(upload_to='products/pdf_catalogues', blank=True, null=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("is_coming_soon"),
            FieldPanel("image"),
        ], heading="Basic Info"),

        MultiFieldPanel([
            FieldPanel("small_description"),
            FieldPanel("overview"),
        ], heading="Description"),

        MultiFieldPanel([
            FieldPanel("youtube_url"),
            FieldPanel("youtube_embed"),
            FieldPanel("pdf_catalogue"),
        ], heading="Media & Downloads"),

        MultiFieldPanel([
            InlinePanel("car_color_variants", label="Color Variants"),
            InlinePanel("car_gallery", label="Gallery"),
            InlinePanel("car_spec", label="Specifications"),
        ], heading="Car Details"),
    ]

    search_fields = [
        index.SearchField("title"),
    ]

    def __str__(self):
        return self.title


    def get_url(self):
        return reverse(
            "core:product_detail",
            kwargs={"slug": self.slug},
        )

    def get_absolute_url(self):
        return self.get_url()

# inline
class ProductGallery(models.Model):
    product = ParentalKey(Car, related_name='car_gallery')
    image = models.ImageField(upload_to='car/gallery')
    title = models.CharField(max_length=40, blank=True, null=True)


# inline
class ProductColorVariant(models.Model):
    product = ParentalKey(Car, related_name='car_color_variants', on_delete=models.CASCADE)
    color = models.CharField(max_length=255)
    color_hex = models.CharField(max_length=6)
    image = models.ImageField(upload_to='products/color_variants')


class CarSpecCategory(index.Indexed, models.Model):
    title = models.CharField(max_length=255)

    panels = [
        FieldPanel("title"),
    ]

    search_fields = [
        index.SearchField("title"),
    ]


    def __str__(self):
        return self.title


class Specification(index.Indexed, models.Model):
    title = models.CharField(max_length=255)
    carspec_category = models.ForeignKey(CarSpecCategory, on_delete=models.CASCADE, related_name="car_specs_category")
    icon = models.CharField(max_length=255)

    panels = [
        FieldPanel("carspec_category"),
        FieldPanel("title"),
        FieldPanel("icon"),
    ]

    search_fields = [
        index.SearchField("title"),
    ]

    def __str__(self):
        return f"{self.title} - {self.carspec_category.title}"


# inline
class CarSpec(models.Model):
    product = ParentalKey(Car, related_name='car_spec', on_delete=models.CASCADE)
    carspec = models.ForeignKey(Specification, related_name='spec_car', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
