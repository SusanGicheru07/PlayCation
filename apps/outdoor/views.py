from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import OutdoorLocation, OutdoorActivity
import math


def map_view(request):
    return render(request, "outdoor/map.html")


def locations_json(request):
    return JsonResponse(list(
        OutdoorLocation.objects.values("id", "name", "description", "lat", "lng")
    ), safe=False)


def activities_json(request):
    data = []
    for act in OutdoorActivity.objects.select_related("location"):
        data.append({
            "id": act.id,
            "name": act.name,
            "activity": act.activity,
            "lat": act.lat,
            "lng": act.lng,
            "notes": act.notes,
            "location": act.location.name if act.location else "Unlinked"
        })
    return JsonResponse(data, safe=False)


def haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two lat/lng points."""
    R = 6371
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))


@require_POST
@csrf_exempt
def add_activity(request):
    lat, lng = float(request.POST["lat"]), float(request.POST["lng"])

    # find nearest location
    locations = OutdoorLocation.objects.all()
    nearest = min(locations, key=lambda loc: haversine(lat, lng, loc.lat, loc.lng), default=None)

    if not nearest:
        return JsonResponse({"error": "No Outdoor Locations defined!"}, status=400)

    act = OutdoorActivity.objects.create(
        name=request.POST["name"],
        activity=request.POST.get("activity", "other"),
        lat=lat,
        lng=lng,
        notes=request.POST.get("notes", ""),
        location=nearest
    )

    return JsonResponse({
        "id": act.id,
        "name": act.name,
        "activity": act.activity,
        "lat": act.lat,
        "lng": act.lng,
        "notes": act.notes,
        "location": nearest.name
    })
