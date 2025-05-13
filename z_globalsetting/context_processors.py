from.models import BrandingSetting

def branding_context_processor(request):
    ctx_branding = BrandingSetting.objects.first()
    return {'ctx_branding': ctx_branding}