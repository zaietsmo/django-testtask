from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from .models import Event, EventRegistration


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_event_creation(self):
        event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            date="2025-06-01T12:00:00Z",
            location="Test Location",
            organizer=self.user,
            capacity=50,
        )
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.organizer, self.user)

    def test_event_string_representation(self):
        event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            date="2025-06-01T12:00:00Z",
            location="Test Location",
            organizer=self.user,
        )
        self.assertEqual(str(event), "Test Event")


class EventRegistrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            date="2025-06-01T12:00:00Z",
            location="Test Location",
            organizer=self.user,
        )

    def test_event_registration(self):
        registration = EventRegistration.objects.create(
            event=self.event, user=self.user
        )
        self.assertEqual(registration.event, self.event)
        self.assertEqual(registration.user, self.user)

    def test_duplicate_registration_prevention(self):
        # First registration should be successful
        EventRegistration.objects.create(event=self.event, user=self.user)

        # Second registration should fail
        with self.assertRaises(IntegrityError):
            EventRegistration.objects.create(event=self.event, user=self.user)
