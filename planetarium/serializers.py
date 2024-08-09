from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ['id', 'title', 'description']


class AstronomyShowSerializer(serializers.ModelSerializer):
    show_theme = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "show_theme")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ['id', 'name', 'rows', 'seats_in_row']


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowSerializer(read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)

    class Meta:
        model = ShowSession
        fields = ['id', 'astronomy_show', 'planetarium_dome', 'show_time']


class AstronomyShowRetrieveSerializer(AstronomyShowSerializer):
    class Meta:
        model = AstronomyShow
        fields = AstronomyShowSerializer.Meta.fields + ("description",)


class ReservationSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ("id", "created_at")

    def get_created_at(self, obj):
        return obj.formatted_created_at


class TicketSerializer(serializers.ModelSerializer):
    show = ShowSessionSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'row', 'seats', 'show', 'reservation']


class TicketRetrieveSerializer(TicketSerializer):
    show_session = ShowSessionSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)


class ShowSessionTicketSerializer(serializers.ModelSerializer):
    show_title = serializers.SlugRelatedField(
        source="astronomy_show",
        many=False,
        read_only=True,
        slug_field="title",
    )
    planetarium_dome = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = ShowSession
        fields = ("show_title", "planetarium_dome")
