from django.http import HttpRequest
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status, generics

from apps.outdoor.serializers import NewEventSerializer
from apps.outdoor.models import OutdoorActivity

# Create your views here.
def index(request: HttpRequest):
    return render(request, 'outdoor/index.html')


def create_event(request: HttpRequest):
    return render(request, "outdoor/new_event.html")


class NewEventAPIView(generics.ListCreateAPIView):
    queryset = OutdoorActivity.objects.all().order_by("-created_at")
    serializer_class = NewEventSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)