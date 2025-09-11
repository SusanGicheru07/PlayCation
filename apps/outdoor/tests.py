from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import OutdoorActivity


class OutdoorActivityModelTest(TestCase):
    def test_create_outdoor_activity(self):
        """Test creating an OutdoorActivity instance with valid data."""
        activity = OutdoorActivity.objects.create(
            title="Hiking in the Mountains",
            category="hiking",
            latitude=40.7128,
            longitude=-74.0060,
            description="A great hike with scenic views."
        )
        self.assertEqual(activity.title, "Hiking in the Mountains")
        self.assertEqual(activity.category, "hiking")
        self.assertEqual(activity.latitude, 40.7128)
        self.assertEqual(activity.longitude, -74.0060)
        self.assertEqual(activity.description, "A great hike with scenic views.")
        self.assertIsNotNone(activity.created_at)

    def test_str_method(self):
        """Test the __str__ method returns the title."""
        activity = OutdoorActivity.objects.create(
            title="Beach Volleyball",
            category="sports",
            latitude=34.0522,
            longitude=-118.2437
        )
        self.assertEqual(str(activity), "Beach Volleyball")

    def test_meta_ordering(self):
        """Test that activities are ordered by title."""
        activity1 = OutdoorActivity.objects.create(
            title="Zulu Dance",
            category="cultural",
            latitude=0.0,
            longitude=0.0
        )
        activity2 = OutdoorActivity.objects.create(
            title="Adventure Park",
            category="adventure",
            latitude=1.0,
            longitude=1.0
        )
        activities = list(OutdoorActivity.objects.all())
        self.assertEqual(activities[0].title, "Adventure Park")
        self.assertEqual(activities[1].title, "Zulu Dance")

    def test_title_max_length(self):
        """Test that title cannot exceed max_length."""
        long_title = "A" * 151  # Exceeds 150
        activity = OutdoorActivity(
            title=long_title,
            category="other",
            latitude=0.0,
            longitude=0.0
        )
        with self.assertRaises(ValidationError):
            activity.full_clean()

    def test_required_fields(self):
        """Test that required fields are enforced."""
        # Missing title
        with self.assertRaises(ValidationError):
            activity = OutdoorActivity(
                category="other",
                latitude=0.0,
                longitude=0.0
            )
            activity.full_clean()

        # Missing latitude
        with self.assertRaises(ValidationError):
            activity = OutdoorActivity(
                title="Test",
                category="other",
                longitude=0.0
            )
            activity.full_clean()

        # Missing longitude
        with self.assertRaises(ValidationError):
            activity = OutdoorActivity(
                title="Test",
                category="other",
                latitude=0.0
            )
            activity.full_clean()

    def test_default_values(self):
        """Test default values for category and created_at."""
        activity = OutdoorActivity.objects.create(
            title="Default Test",
            latitude=0.0,
            longitude=0.0
        )
        self.assertEqual(activity.category, "other")
        self.assertIsNotNone(activity.created_at)


class NewEventAPIViewTest(APITestCase):
    def setUp(self):
        """Set up test data."""
        self.url = reverse('events')
        self.valid_data = {
            'title': 'Test Event',
            'category': 'test',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'description': 'A test event.'
        }
        self.invalid_data = {
            'title': '',  # Invalid: empty title
            'category': 'test',
            'latitude': 40.7128,
            'longitude': -74.0060
        }

    def test_get_list_events(self):
        """Test GET request to list all events ordered by created_at descending."""
        # Create test activities
        activity1 = OutdoorActivity.objects.create(
            title='Event 1',
            category='category1',
            latitude=1.0,
            longitude=1.0
        )
        activity2 = OutdoorActivity.objects.create(
            title='Event 2',
            category='category2',
            latitude=2.0,
            longitude=2.0
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Check ordering: latest first
        self.assertEqual(response.data[0]['title'], 'Event 2')
        self.assertEqual(response.data[1]['title'], 'Event 1')

    def test_post_create_event_valid(self):
        """Test POST request to create a new event with valid data."""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Event')
        self.assertEqual(response.data['category'], 'test')
        # Check that it was saved
        self.assertEqual(OutdoorActivity.objects.count(), 1)
        activity = OutdoorActivity.objects.first()
        self.assertEqual(activity.title, 'Test Event')

    def test_post_create_event_invalid(self):
        """Test POST request to create a new event with invalid data."""
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that no activity was created
        self.assertEqual(OutdoorActivity.objects.count(), 0)

