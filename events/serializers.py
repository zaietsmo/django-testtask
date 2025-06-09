from rest_framework import serializers

from .models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source="organizer.username")
    is_registered = serializers.SerializerMethodField()
    registered_users_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "location",
            "organizer",
            "capacity",
            "is_registered",
            "registered_users_count",
        ]

    def get_is_registered(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            return EventRegistration.objects.filter(
                event=obj, user=request.user
            ).exists()
        return False

    def get_registered_users_count(self, obj):
        return obj.registrations.count()


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    event_title = serializers.ReadOnlyField(source="event.title")

    class Meta:
        model = EventRegistration
        fields = ["id", "user", "event", "event_title", "registered_at"]
        read_only_fields = ["registered_at"]
