from .base import *

DEBUG = False

SECRET_KEY = "django-insecure-n)i+ufgod+!f*ouq7%k(45imfs%%#z)^lk27ta8m%bnx##&qm3"

AWS_S3_ENDPOINT_URL = "http://nos.wjv-1.neo.id"


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "default_acl": "public-read",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "static/",
            "default_acl": "public-read",
            "endpoint_url": "https://nos.wjv-1.neo.id",
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
