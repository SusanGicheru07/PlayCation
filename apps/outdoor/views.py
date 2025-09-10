from django.http import HttpRequest
from django.shortcuts import render
from typing import Dict, Any

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.request import Request

from apps.outdoor.serializers import NewEventSerializer
from apps.outdoor.models import OutdoorActivity

# Create your views here.
def index(request: HttpRequest):
    return render(request, 'outdoor/index.html')


def create_event(request: HttpRequest):
    return render(request, "outdoor/new_event.html")


class NewEventAPIView(generics.ListCreateAPIView):
    """
    API view to handle listing and creating new outdoor activity events.

    - GET: Retrieve a list of all events ordered by creation date (latest first).
    - POST: Create a new event with the provided details.
    """

    queryset = OutdoorActivity.objects.all().order_by("-created_at")
    serializer_class = NewEventSerializer
    def post(self, request: Request, *args: Dict[Any, Any], **kwargs: Dict[Any, Any]):
        """
        Handle the creation of a new event.

        Args:
            request (Request): The HTTP request object containing event data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Body:
            - title: str
            - category: str
            - description: str
            - latitude: float
            - longitude: float
            - created_at: datetime

        Returns:
            Response: 
                - 201 Created with serialized event data if successful.
                - 400 Bad Request with validation errors if input is invalid.
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
