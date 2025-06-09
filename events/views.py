from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, EventRegistration
from .permissions import IsOrganizerOrReadOnly
from .serializers import EventRegistrationSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing events.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["date", "location"]
    search_fields = ["title", "description"]
    ordering_fields = ["date", "title"]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if already registered
        if EventRegistration.objects.filter(event=event, user=user).exists():
            return Response(
                {"detail": "Already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check capacity
        if event.capacity and event.registrations.count() >= event.capacity:
            return Response(
                {"detail": "Event has reached capacity."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create registration
        registration = EventRegistration.objects.create(event=event, user=user)
        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def unregister(self, request, pk=None):
        event = self.get_object()
        user = request.user

        try:
            registration = EventRegistration.objects.get(event=event, user=user)
            registration.delete()
            return Response(
                {"detail": "Successfully unregistered from event."},
                status=status.HTTP_200_OK,
            )
        except EventRegistration.DoesNotExist:
            return Response(
                {"detail": "Not registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"])
    def registrations(self, request, pk=None):
        """
        List all registrations for this event.
        Only accessible by the event organizer.
        """
        event = self.get_object()

        # Check if user is organizer
        if request.user != event.organizer and not request.user.is_staff:
            return Response(
                {"detail": "Only the event organizer can view registrations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        registrations = event.registrations.all()
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class EventRegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing event registrations.
    Users can only see their own registrations.
    """

    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventRegistration.objects.filter(user=self.request.user)
