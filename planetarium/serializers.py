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
    themes = ShowThemeSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ['id', 'title', 'themes', 'description']


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


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'created_at', 'user']


class TicketSerializer(serializers.ModelSerializer):
    show = ShowSessionSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'row', 'seats', 'show', 'reservation']
