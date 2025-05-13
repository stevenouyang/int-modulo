import boto3
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
import re
from django.conf import settings
from urllib.parse import urlparse

parsed_endpoint = urlparse(settings.AWS_S3_ENDPOINT_URL)
secure_scheme = 'https' if parsed_endpoint.scheme == 'http' else parsed_endpoint.scheme
secure_endpoint_url = parsed_endpoint._replace(scheme=secure_scheme).geturl()

s3_client = boto3.client(
    "s3",
    endpoint_url=secure_endpoint_url,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

S3_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
S3_BASE_UPLOAD_URL = secure_endpoint_url
S3_BASE_ACCESS_URL = secure_endpoint_url.replace("http://", "https://")

def extract_list_items(rich_text):
    """Extracts list items from a Wagtail RichText field."""
    soup = BeautifulSoup(rich_text, "html.parser")
    return [li.get_text(strip=True) for li in soup.find_all("li")]

def extract_dimensions_from_block_type(block_type):
    """
    Extracts dimensions from a block type like 'image_1280x720'.
    Returns (width, height, suffix) if valid, else None.
    """
    match = re.search(r'image_(\d+)x(\d+)', block_type)
    if match:
        width, height = int(match.group(1)), int(match.group(2))
        suffix = f"{width}x{height}"
        return width, height, suffix
    return None

def resize_image(image_data, max_width, max_height, quality=90):
    img = Image.open(BytesIO(image_data))
    aspect_ratio = img.width / img.height

    if aspect_ratio > max_width / max_height:
        new_width = int(img.height * (max_width / max_height))
        left_margin = (img.width - new_width) / 2
        top_margin = 0
        right_margin = left_margin + new_width
        bottom_margin = img.height
    else:
        new_height = int(img.width * (max_height / max_width))
        left_margin = 0
        top_margin = (img.height - new_height) / 2
        right_margin = img.width
        bottom_margin = top_margin + new_height

    img_cropped = img.crop((left_margin, top_margin, right_margin, bottom_margin))
    img_resized = img_cropped.resize((max_width, max_height), Image.LANCZOS)

    output_io = BytesIO()
    img_resized.save(output_io, "WebP", quality=quality)
    output_io.seek(0)

    print("resizing image...")

    return output_io


def process_image_block(item, width, height, suffix):
    original_url = item.value.file.url
    image_filename = original_url.split("/")[-1]
    base_name, ext = image_filename.rsplit('.', 1)
    new_filename = f"{base_name}_{suffix}.webp"

    s3_resized_path = f"dev1/portfolio_utils/resized_images/{new_filename}"

    try:
        s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=s3_resized_path)
        print(f"{new_filename} already exists on S3.")
    except:
        print(f"Resizing and uploading {new_filename}...")
        response = requests.get(original_url, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download image: {original_url}")

        resized_image = resize_image(response.content, width, height, 90)

        s3_client.upload_fileobj(
            resized_image,
            S3_BUCKET_NAME,
            s3_resized_path,
            ExtraArgs={"ContentType": "image/webp", "ACL": "public-read"},
        )

    item.normalized_type = "image"
    item.processed_image_url = f"{S3_BASE_ACCESS_URL}/{S3_BUCKET_NAME}/{s3_resized_path}"


def process_portfolio_content(portfolio_content):
    for item in portfolio_content:
        dimensions = extract_dimensions_from_block_type(item.block_type)
        if dimensions:
            width, height, suffix = dimensions
            process_image_block(item, width, height, suffix)

        elif item.block_type in ["unordered_list", "ordered_list"]:
            item.list_items = extract_list_items(item.value.source)