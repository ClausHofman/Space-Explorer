from .models import System, CelestialBody, MiningSpot, BodyComment, MiningSpotComment

def global_counts(request):
    return {
        "system_count": System.objects.count(),
        "body_count": CelestialBody.objects.count(),
        "spot_count": MiningSpot.objects.count(),
        "body_comment_count": BodyComment.objects.count(),
        "spot_comment_count": MiningSpotComment.objects.count(),
    }
